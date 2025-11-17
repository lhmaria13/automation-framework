"""
Gerenciador abstrato de WebDriver
Implementa padrão Strategy para suportar múltiplos navegadores
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from automation_framework.web.driver_utils import ensure_driver_installed
from pathlib import Path

from automation_framework.core.logger import Logger
from automation_framework.core.config import ConfigManager
from automation_framework.core.exceptions import (
    InvalidBrowserType,
    BrowserException,
    ElementNotFound,
    TimeoutException
)


class BaseWebDriver(ABC):
    """Classe abstrata base para WebDrivers"""

    def __init__(self, config: dict):
        self.config = config
        self.driver: Optional[webdriver.Remote] = None
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.wait_timeout = config.get('implicit_wait', 10)

    @abstractmethod
    def _create_options(self):
        """Cria opções específicas do navegador"""
        pass

    @abstractmethod
    def _create_driver(self):
        """Cria instância do WebDriver"""
        pass

    def initialize(self) -> None:
        """Inicializa o navegador"""
        try:
            self._create_driver()
            if not self.config.get('headless', False):
                self.driver.maximize_window()
            self.driver.set_page_load_timeout(self.config.get('page_load_timeout', 30))
            self.logger.info(f"Navegador {self.__class__.__name__} inicializado com sucesso")
        except Exception as e:
            self.logger.error(f"Erro ao inicializar navegador: {str(e)}")
            raise BrowserException(f"Falha ao inicializar navegador: {str(e)}")

    def quit(self) -> None:
        """Encerra o navegador"""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("Navegador encerrado")
            except Exception as e:
                self.logger.warning(f"Erro ao encerrar navegador: {str(e)}")

    def get(self, url: str) -> None:
        """Navega para URL"""
        self.driver.get(url)
        self.logger.info(f"Navegou para: {url}")

    def find_element(self, by: By, value: str) -> WebElement:
        """Localiza um elemento"""
        try:
            wait = WebDriverWait(self.driver, self.wait_timeout)
            element = wait.until(EC.presence_of_element_located((by, value)))
            self.logger.debug(f"Elemento encontrado: {by}={value}")
            return element
        except Exception as e:
            self.logger.error(f"Elemento não encontrado: {by}={value}")
            raise ElementNotFound(f"Elemento não encontrado: {by}={value}")

    def find_elements(self, by: By, value: str) -> List[WebElement]:
        """Localiza múltiplos elementos"""
        try:
            wait = WebDriverWait(self.driver, self.wait_timeout)
            elements = wait.until(EC.presence_of_all_elements_located((by, value)))
            self.logger.debug(f"Encontrados {len(elements)} elementos: {by}={value}")
            return elements
        except Exception as e:
            self.logger.warning(f"Nenhum elemento encontrado: {by}={value}")
            return []

    def click(self, by: By, value: str) -> None:
        """Clica em um elemento"""
        try:
            element = self.find_element(by, value)
            WebDriverWait(self.driver, self.wait_timeout).until(EC.element_to_be_clickable((by, value)))
            element.click()
            self.logger.info(f"Clique realizado em: {by}={value}")
        except Exception as e:
            self.logger.error(f"Erro ao clicar: {str(e)}")
            raise

    def type_text(self, by: By, value: str, text: str, clear_first: bool = True) -> None:
        """Digita texto em um elemento"""
        try:
            element = self.find_element(by, value)
            if clear_first:
                element.clear()
            element.send_keys(text)
            self.logger.info(f"Texto digitado em {by}={value}: {text}")
        except Exception as e:
            self.logger.error(f"Erro ao digitar texto: {str(e)}")
            raise

    def get_text(self, by: By, value: str) -> str:
        """Obtém texto de um elemento"""
        element = self.find_element(by, value)
        text = element.text
        self.logger.debug(f"Texto obtido de {by}={value}: {text}")
        return text

    def get_attribute(self, by: By, value: str, attribute: str) -> str:
        """Obtém atributo de um elemento"""
        element = self.find_element(by, value)
        attr_value = element.get_attribute(attribute)
        self.logger.debug(f"Atributo '{attribute}' obtido de {by}={value}: {attr_value}")
        return attr_value

    def is_element_visible(self, by: By, value: str, timeout: int = 5) -> bool:
        """Verifica se elemento está visível"""
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, value)))
            return True
        except:
            return False

    def wait_for_element(self, by: By, value: str, timeout: Optional[int] = None) -> WebElement:
        """Aguarda um elemento aparecer"""
        timeout = timeout or self.wait_timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located((by, value)))
            self.logger.info(f"Elemento aguardado: {by}={value}")
            return element
        except Exception as e:
            self.logger.error(f"Timeout aguardando elemento: {by}={value}")
            raise TimeoutException(f"Timeout aguardando elemento: {by}={value}")

    def execute_script(self, script: str, *args):
        """Executa JavaScript"""
        result = self.driver.execute_script(script, *args)
        self.logger.debug("Script JavaScript executado")
        return result

    def take_screenshot(self, file_path: str) -> None:
        """Captura screenshot"""
        self.driver.save_screenshot(file_path)
        self.logger.info(f"Screenshot salvo em: {file_path}")

    def get_page_source(self) -> str:
        """Obtém código-fonte da página"""
        return self.driver.page_source

    def refresh(self) -> None:
        """Atualiza a página"""
        self.driver.refresh()
        self.logger.info("Página atualizada")

    def get_current_url(self) -> str:
        """Obtém URL atual"""
        return self.driver.current_url


class ChromeWebDriver(BaseWebDriver):
    """Implementação para Chrome"""

    def _create_options(self):
        """Cria opções do Chrome"""
        options = webdriver.ChromeOptions()

        if self.config.get('headless', False):
            options.add_argument('--headless=new')

        if proxy := self.config.get('proxy'):
            options.add_argument(f'--proxy-server={proxy}')

        if user_data_dir := self.config.get('user_data_dir'):
            options.add_argument(f'user-data-dir={user_data_dir}')

        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')

        # Configurar tamanho da janela se especificado
        if window_size := self.config.get('window_size'):
            options.add_argument(f'--window-size={window_size}')

        return options

    def _create_driver(self):
        """Cria WebDriver do Chrome"""
        options = self._create_options()

        # Baixa/garante driver no diretório `drivers/` do projeto
        drivers_dir = Path(__file__).resolve().parents[2] / "drivers"
        driver_path = ensure_driver_installed('chrome', target_dir=str(drivers_dir))
        service = ChromeService(driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)


class FirefoxWebDriver(BaseWebDriver):
    """Implementação para Firefox"""

    def _create_options(self):
        """Cria opções do Firefox"""
        options = webdriver.FirefoxOptions()

        if self.config.get('headless', False):
            options.add_argument('--headless')

        if proxy := self.config.get('proxy'):
            options.set_preference('network.proxy.type', 1)
            options.set_preference('network.proxy.http', proxy.split(':')[0])
            options.set_preference('network.proxy.http_port', int(proxy.split(':')[1]))

        if user_data_dir := self.config.get('user_data_dir'):
            options.add_argument(f'--profile={user_data_dir}')

        return options

    def _create_driver(self):
        """Cria WebDriver do Firefox"""
        options = self._create_options()

        drivers_dir = Path(__file__).resolve().parents[2] / "drivers"
        driver_path = ensure_driver_installed('firefox', target_dir=str(drivers_dir))
        service = FirefoxService(driver_path)
        self.driver = webdriver.Firefox(service=service, options=options)


class EdgeWebDriver(BaseWebDriver):
    """Implementação para Edge"""

    def _create_options(self):
        """Cria opções do Edge"""
        options = webdriver.EdgeOptions()

        if self.config.get('headless', False):
            options.add_argument('--headless=new')

        if proxy := self.config.get('proxy'):
            options.add_argument(f'--proxy-server={proxy}')

        if user_data_dir := self.config.get('user_data_dir'):
            options.add_argument(f'user-data-dir={user_data_dir}')

        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        return options

    def _create_driver(self):
        """Cria WebDriver do Edge"""
        options = self._create_options()

        drivers_dir = Path(__file__).resolve().parents[2] / "drivers"
        driver_path = ensure_driver_installed('edge', target_dir=str(drivers_dir))
        service = EdgeService(driver_path)
        self.driver = webdriver.Edge(service=service, options=options)


class DriverManager:
    """
    Gerenciador centralizado de drivers
    Implementa padrão Factory + Singleton
    """

    _instance: Optional['DriverManager'] = None
    _driver: Optional[BaseWebDriver] = None
    _browser_type: str = "chrome"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DriverManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.config_manager = ConfigManager()
        self.logger = Logger.get_logger(self.__class__.__name__)

    def initialize_browser(self, browser_type: Optional[str] = None) -> BaseWebDriver:
        """
        Inicializa navegador especificado

        Args:
            browser_type: Tipo de navegador (chrome, firefox, edge)

        Returns:
            BaseWebDriver: Instância do driver inicializado
        """
        if browser_type:
            self._browser_type = browser_type.lower()

        if self._driver:
            self._driver.quit()

        config = self.config_manager.get_browser_config().__dict__

        driver_class = self._get_driver_class(self._browser_type)
        self._driver = driver_class(config)
        self._driver.initialize()

        return self._driver

    def get_driver(self) -> BaseWebDriver:
        """Obtém driver atual ou inicializa o padrão"""
        if not self._driver:
            self.initialize_browser()
        return self._driver

    def switch_browser(self, browser_type: str) -> BaseWebDriver:
        """
        Troca de navegador

        Args:
            browser_type: Novo tipo de navegador

        Returns:
            BaseWebDriver: Novo driver inicializado
        """
        self.logger.info(f"Alternando para navegador: {browser_type}")
        return self.initialize_browser(browser_type)

    def quit_browser(self) -> None:
        """Encerra o navegador atual"""
        if self._driver:
            self._driver.quit()
            self._driver = None
            self.logger.info("Navegador encerrado")

    @staticmethod
    def _get_driver_class(browser_type: str):
        """Retorna classe appropriada do driver"""
        drivers = {
            'chrome': ChromeWebDriver,
            'firefox': FirefoxWebDriver,
            'edge': EdgeWebDriver,
        }

        if browser_type not in drivers:
            raise InvalidBrowserType(f"Tipo de navegador inválido: {browser_type}")

        return drivers[browser_type]

    def __enter__(self):
        """Context manager support"""
        return self.get_driver()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager support"""
        self.quit_browser()
