"""
Base Page Object Model
Classe base para criar page objects reutilizáveis
"""

from typing import Optional, List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from automation_framework.core.logger import Logger
from automation_framework.web.driver_manager import BaseWebDriver
from automation_framework.web.locators import Locator, ElementHelper, Table, Form


class BasePage:
    """
    Classe base para Page Objects
    Fornece métodos comuns para interação com páginas
    """

    def __init__(self, driver: BaseWebDriver):
        self.driver = driver
        self.logger = Logger.get_logger(self.__class__.__name__)

    def navigate_to(self, url: str) -> None:
        """Navega para URL"""
        self.driver.get(url)
        self.logger.info(f"Navegando para: {url}")

    def find_element(self, locator: Locator) -> WebElement:
        """Localiza elemento usando Locator"""
        return self.driver.find_element(locator.by, locator.value)

    def find_elements(self, locator: Locator) -> List[WebElement]:
        """Localiza múltiplos elementos usando Locator"""
        return self.driver.find_elements(locator.by, locator.value)

    def click(self, locator: Locator) -> None:
        """Clica em elemento"""
        self.driver.click(locator.by, locator.value)

    def type_text(self, locator: Locator, text: str, clear_first: bool = True) -> None:
        """Digita texto"""
        self.driver.type_text(locator.by, locator.value, text, clear_first)

    def get_text(self, locator: Locator) -> str:
        """Obtém texto do elemento"""
        return self.driver.get_text(locator.by, locator.value)

    def get_attribute(self, locator: Locator, attribute: str) -> str:
        """Obtém atributo do elemento"""
        return self.driver.get_attribute(locator.by, locator.value, attribute)

    def is_element_visible(self, locator: Locator, timeout: int = 5) -> bool:
        """Verifica se elemento está visível"""
        return self.driver.is_element_visible(locator.by, locator.value, timeout)

    def wait_for_element(self, locator: Locator, timeout: Optional[int] = None) -> WebElement:
        """Aguarda elemento aparecer"""
        return self.driver.wait_for_element(locator.by, locator.value, timeout)

    def execute_script(self, script: str, *args):
        """Executa JavaScript"""
        return self.driver.execute_script(script, *args)

    def take_screenshot(self, file_path: str) -> None:
        """Captura screenshot"""
        self.driver.take_screenshot(file_path)

    def get_page_title(self) -> str:
        """Obtém título da página"""
        return self.driver.driver.title

    def get_current_url(self) -> str:
        """Obtém URL atual"""
        return self.driver.get_current_url()

    def refresh(self) -> None:
        """Atualiza a página"""
        self.driver.refresh()

    def get_table(self, locator: Locator) -> Table:
        """Retorna helper para trabalhar com tabela"""
        element = self.find_element(locator)
        return Table(element)

    def get_form(self, locator: Locator) -> Form:
        """Retorna helper para trabalhar com formulário"""
        element = self.find_element(locator)
        return Form(element)

    def wait_for_url(self, partial_url: str, timeout: int = 10) -> bool:
        """Aguarda URL conter texto específico"""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        try:
            WebDriverWait(self.driver.driver, timeout).until(
                EC.url_contains(partial_url)
            )
            return True
        except:
            return False

    def wait_for_title(self, title: str, timeout: int = 10) -> bool:
        """Aguarda título da página"""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        try:
            WebDriverWait(self.driver.driver, timeout).until(
                EC.title_contains(title)
            )
            return True
        except:
            return False


class BaseComponent:
    """
    Classe base para Componentes reutilizáveis
    Usada para agrupar elementos e ações relacionadas
    """

    def __init__(self, driver: BaseWebDriver, root_locator: Locator):
        self.driver = driver
        self.root_locator = root_locator
        self.logger = Logger.get_logger(self.__class__.__name__)

    def get_root_element(self) -> WebElement:
        """Obtém elemento raiz do componente"""
        return self.driver.find_element(self.root_locator.by, self.root_locator.value)

    def find_child_element(self, locator: Locator) -> Optional[WebElement]:
        """Localiza elemento filho do componente"""
        root = self.get_root_element()
        return ElementHelper.find_child_element(root, locator.by, locator.value)

    def find_child_elements(self, locator: Locator) -> List[WebElement]:
        """Localiza múltiplos elementos filhos"""
        root = self.get_root_element()
        return ElementHelper.find_child_elements(root, locator.by, locator.value)

    def is_visible(self) -> bool:
        """Verifica se componente está visível"""
        try:
            element = self.get_root_element()
            return ElementHelper.is_displayed(element)
        except:
            return False

    def is_enabled(self) -> bool:
        """Verifica se componente está habilitado"""
        try:
            element = self.get_root_element()
            return ElementHelper.is_enabled(element)
        except:
            return False
