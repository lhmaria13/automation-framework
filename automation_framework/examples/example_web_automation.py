"""
Exemplo 1: Automação Web com Chrome
Demonstra uso do DriverManager com Page Object Model
"""

import sys
from pathlib import Path

# Garantir que a raiz do projeto esteja no sys.path para permitir execução
# a partir da pasta `automation_framework/` ou de qualquer outra
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from automation_framework.web.driver_manager import DriverManager
from automation_framework.web.page_object import BasePage
from automation_framework.web.locators import Locator
from automation_framework.core.config import ConfigManager
from automation_framework.core.logger import Logger


class GoogleSearchPage(BasePage):
    """Page Object para página de busca do Google"""

    # Localizadores
    SEARCH_INPUT = Locator.name("q")
    SEARCH_BUTTON = Locator.xpath("//button[contains(text(), 'Pesquisar')]")
    RESULT_LINKS = Locator.xpath("//a[@href]")

    def search(self, query: str) -> None:
        """Realiza busca"""
        self.type_text(self.SEARCH_INPUT, query)
        self.click(self.SEARCH_BUTTON)

    def get_results_count(self) -> int:
        """Retorna número de resultados"""
        results = self.find_elements(self.RESULT_LINKS)
        return len(results)


def main():
    # Configurar
    config = ConfigManager()
    config.set('browser.headless', False)
    config.set('browser.implicit_wait', 15)

    logger = Logger.get_logger(__name__)
    logger.info("Iniciando exemplo de automação web")

    # Inicializar driver
    driver_manager = DriverManager()
    driver = driver_manager.initialize_browser('chrome')

    try:
        # Navegar e interagir
        page = GoogleSearchPage(driver)
        page.navigate_to("https://www.google.com")

        logger.info("Página carregada")

        page.search("Python automation framework")
        logger.info("Busca realizada")

        results = page.get_results_count()
        logger.info(f"Encontrados {results} resultados")

        # Screenshot
        page.take_screenshot("google_search_results.png")

    finally:
        # Encerrar
        driver_manager.quit_browser()
        logger.info("Navegador encerrado")


if __name__ == "__main__":
    main()
