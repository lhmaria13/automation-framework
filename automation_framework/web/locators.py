"""
Localizadores fluentes e helpers para elementos web
Implementa pattern Fluent Interface para queries elegantes
"""

from typing import Optional, Callable, Any
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from automation_framework.core.logger import Logger


class Locator:
    """Encapsula um localizador (By, value)"""

    def __init__(self, by: By, value: str):
        self.by = by
        self.value = value

    def __repr__(self):
        return f"Locator({self.by.name}, '{self.value}')"

    @staticmethod
    def id(value: str) -> 'Locator':
        """Localiza por ID"""
        return Locator(By.ID, value)

    @staticmethod
    def name(value: str) -> 'Locator':
        """Localiza por name"""
        return Locator(By.NAME, value)

    @staticmethod
    def xpath(value: str) -> 'Locator':
        """Localiza por XPath"""
        return Locator(By.XPATH, value)

    @staticmethod
    def css_selector(value: str) -> 'Locator':
        """Localiza por CSS Selector"""
        return Locator(By.CSS_SELECTOR, value)

    @staticmethod
    def class_name(value: str) -> 'Locator':
        """Localiza por classe CSS"""
        return Locator(By.CLASS_NAME, value)

    @staticmethod
    def tag_name(value: str) -> 'Locator':
        """Localiza por tag HTML"""
        return Locator(By.TAG_NAME, value)

    @staticmethod
    def link_text(value: str) -> 'Locator':
        """Localiza link por texto exato"""
        return Locator(By.LINK_TEXT, value)

    @staticmethod
    def partial_link_text(value: str) -> 'Locator':
        """Localiza link por texto parcial"""
        return Locator(By.PARTIAL_LINK_TEXT, value)


class ElementHelper:
    """
    Helper para trabalhar com elementos
    Fornece métodos auxiliares comuns
    """

    @staticmethod
    def get_text(element: WebElement) -> str:
        """Obtém texto do elemento"""
        return element.text.strip()

    @staticmethod
    def get_value(element: WebElement) -> str:
        """Obtém valor do elemento (para inputs)"""
        return element.get_attribute('value')

    @staticmethod
    def is_enabled(element: WebElement) -> bool:
        """Verifica se elemento está habilitado"""
        return element.is_enabled()

    @staticmethod
    def is_displayed(element: WebElement) -> bool:
        """Verifica se elemento está visível"""
        return element.is_displayed()

    @staticmethod
    def is_selected(element: WebElement) -> bool:
        """Verifica se elemento está selecionado"""
        return element.is_selected()

    @staticmethod
    def get_attribute(element: WebElement, attr: str) -> Optional[str]:
        """Obtém atributo do elemento"""
        return element.get_attribute(attr)

    @staticmethod
    def get_css_value(element: WebElement, property_name: str) -> str:
        """Obtém valor CSS do elemento"""
        return element.value_of_css_property(property_name)

    @staticmethod
    def get_size(element: WebElement) -> dict:
        """Obtém tamanho do elemento"""
        size = element.size
        return {'width': size['width'], 'height': size['height']}

    @staticmethod
    def get_location(element: WebElement) -> dict:
        """Obtém localização do elemento"""
        location = element.location
        return {'x': location['x'], 'y': location['y']}

    @staticmethod
    def find_child_element(element: WebElement, by: By, value: str) -> Optional[WebElement]:
        """Localiza elemento filho"""
        try:
            return element.find_element(by, value)
        except:
            return None

    @staticmethod
    def find_child_elements(element: WebElement, by: By, value: str) -> list:
        """Localiza múltiplos elementos filhos"""
        try:
            return element.find_elements(by, value)
        except:
            return []


class Table:
    """
    Helper para trabalhar com tabelas HTML
    """

    def __init__(self, table_element: WebElement):
        self.table = table_element
        self.logger = Logger.get_logger(self.__class__.__name__)

    def get_row_count(self) -> int:
        """Obtém número de linhas da tabela"""
        try:
            rows = self.table.find_elements(By.XPATH, ".//tr")
            return len(rows)
        except:
            return 0

    def get_column_count(self) -> int:
        """Obtém número de colunas da tabela"""
        try:
            headers = self.table.find_elements(By.XPATH, ".//th")
            if headers:
                return len(headers)
            cells = self.table.find_elements(By.XPATH, ".//tr[1]/td")
            return len(cells)
        except:
            return 0

    def get_cell_text(self, row: int, column: int) -> str:
        """Obtém texto de uma célula"""
        try:
            cell = self.table.find_element(By.XPATH, f".//tr[{row + 1}]/td[{column + 1}]")
            return cell.text.strip()
        except Exception as e:
            self.logger.error(f"Erro ao obter célula ({row},{column}): {str(e)}")
            return ""

    def get_row_data(self, row: int) -> list:
        """Obtém dados de uma linha completa"""
        try:
            cells = self.table.find_elements(By.XPATH, f".//tr[{row + 1}]/td")
            return [cell.text.strip() for cell in cells]
        except:
            return []

    def find_cell_by_text(self, text: str) -> Optional[WebElement]:
        """Localiza célula pelo texto"""
        try:
            cell = self.table.find_element(By.XPATH, f".//td[contains(text(), '{text}')]")
            return cell
        except:
            return None

    def get_all_data(self) -> list:
        """Obtém todos os dados da tabela como lista de listas"""
        data = []
        rows = self.table.find_elements(By.XPATH, ".//tr")

        for row in rows:
            cells = row.find_elements(By.XPATH, ".//td")
            if cells:
                data.append([cell.text.strip() for cell in cells])

        return data


class Form:
    """
    Helper para trabalhar com formulários
    """

    def __init__(self, form_element: WebElement):
        self.form = form_element
        self.logger = Logger.get_logger(self.__class__.__name__)

    def fill_text_field(self, field_name: str, value: str) -> None:
        """Preenche campo de texto por name"""
        try:
            field = self.form.find_element(By.NAME, field_name)
            field.clear()
            field.send_keys(value)
            self.logger.info(f"Campo '{field_name}' preenchido")
        except Exception as e:
            self.logger.error(f"Erro ao preencher campo '{field_name}': {str(e)}")

    def select_dropdown(self, field_name: str, value: str) -> None:
        """Seleciona opção de dropdown por name"""
        try:
            select = self.form.find_element(By.NAME, field_name)
            options = select.find_elements(By.TAG_NAME, "option")
            for option in options:
                if option.text == value or option.get_attribute('value') == value:
                    option.click()
                    return
            self.logger.warning(f"Opção '{value}' não encontrada em '{field_name}'")
        except Exception as e:
            self.logger.error(f"Erro ao selecionar dropdown '{field_name}': {str(e)}")

    def check_checkbox(self, field_name: str) -> None:
        """Marca checkbox por name"""
        try:
            checkbox = self.form.find_element(By.NAME, field_name)
            if not checkbox.is_selected():
                checkbox.click()
                self.logger.info(f"Checkbox '{field_name}' marcado")
        except Exception as e:
            self.logger.error(f"Erro ao marcar checkbox '{field_name}': {str(e)}")

    def uncheck_checkbox(self, field_name: str) -> None:
        """Desmarca checkbox por name"""
        try:
            checkbox = self.form.find_element(By.NAME, field_name)
            if checkbox.is_selected():
                checkbox.click()
                self.logger.info(f"Checkbox '{field_name}' desmarcado")
        except Exception as e:
            self.logger.error(f"Erro ao desmarcar checkbox '{field_name}': {str(e)}")

    def submit(self) -> None:
        """Submete o formulário"""
        try:
            self.form.submit()
            self.logger.info("Formulário submetido")
        except Exception as e:
            self.logger.error(f"Erro ao submeter formulário: {str(e)}")

    def get_field_value(self, field_name: str) -> str:
        """Obtém valor de um campo"""
        try:
            field = self.form.find_element(By.NAME, field_name)
            return field.get_attribute('value')
        except:
            return ""
