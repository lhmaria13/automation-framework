"""
Gerenciador de automação desktop Windows
Suporta interação com aplicações Windows, mouse, teclado e screenshots
"""

import pyautogui
import pywinauto
from pywinauto import keyboard
from typing import Optional, Tuple
from pathlib import Path
from time import sleep
import os

from automation_framework.core.logger import Logger
from automation_framework.core.config import ConfigManager
from automation_framework.core.exceptions import DesktopAutomationException


class DesktopApplication:
    """
    Gerenciador de aplicações desktop Windows
    """

    def __init__(self, app_path: Optional[str] = None):
        self.app = None
        self.app_path = app_path
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.config = ConfigManager().get_desktop_config()
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = self.config.timeout

    def launch_application(self, app_path: str) -> None:
        """
        Inicia uma aplicação

        Args:
            app_path: Caminho completo da aplicação
        """
        try:
            if not Path(app_path).exists():
                raise FileNotFoundError(f"Aplicação não encontrada: {app_path}")

            self.app = pywinauto.Application().start(app_path)
            sleep(self.config.pause_between_actions)
            self.logger.info(f"Aplicação iniciada: {app_path}")
        except Exception as e:
            self.logger.error(f"Erro ao iniciar aplicação: {str(e)}")
            raise DesktopAutomationException(f"Falha ao iniciar aplicação: {str(e)}")

    def connect_to_process(self, process_name: str) -> None:
        """
        Conecta a um processo existente

        Args:
            process_name: Nome do processo (ex: notepad.exe)
        """
        try:
            self.app = pywinauto.Application().connect(path=process_name)
            self.logger.info(f"Conectado ao processo: {process_name}")
        except Exception as e:
            self.logger.error(f"Erro ao conectar: {str(e)}")
            raise DesktopAutomationException(f"Falha ao conectar ao processo: {str(e)}")

    def get_window(self):
        """Obtém janela principal da aplicação"""
        if not self.app:
            raise DesktopAutomationException("Nenhuma aplicação inicializada")
        return self.app.top_window()

    def close_application(self) -> None:
        """Fecha a aplicação"""
        try:
            if self.app:
                self.app.kill()
                self.logger.info("Aplicação encerrada")
        except Exception as e:
            self.logger.warning(f"Erro ao encerrar aplicação: {str(e)}")

    def find_control(self, **kwargs):
        """
        Localiza controle dentro da aplicação

        Args:
            **kwargs: Critérios de busca (name, control_type, etc)

        Returns:
            Control encontrado
        """
        try:
            window = self.get_window()
            control = window.find_element(**kwargs)
            self.logger.debug(f"Controle encontrado: {kwargs}")
            return control
        except Exception as e:
            self.logger.error(f"Controle não encontrado: {kwargs}")
            raise DesktopAutomationException(f"Controle não encontrado: {str(e)}")

    def click_element(self, **kwargs) -> None:
        """
        Clica em um elemento/controle

        Args:
            **kwargs: Critérios de busca do elemento
        """
        try:
            control = self.find_control(**kwargs)
            control.click()
            sleep(self.config.pause_between_actions)
            self.logger.info(f"Clique realizado em: {kwargs}")
        except Exception as e:
            self.logger.error(f"Erro ao clicar: {str(e)}")
            raise

    def type_text_in_field(self, text: str, **field_kwargs) -> None:
        """
        Digita texto em um campo

        Args:
            text: Texto a ser digitado
            **field_kwargs: Critérios de busca do campo
        """
        try:
            field = self.find_control(**field_kwargs)
            field.set_focus()
            field.type_keys(text)
            sleep(self.config.pause_between_actions)
            self.logger.info(f"Texto digitado: {text[:30]}...")
        except Exception as e:
            self.logger.error(f"Erro ao digitar: {str(e)}")
            raise

    def clear_field(self, **field_kwargs) -> None:
        """
        Limpa um campo de texto

        Args:
            **field_kwargs: Critérios de busca do campo
        """
        try:
            field = self.find_control(**field_kwargs)
            field.set_focus()
            keyboard.send_keys('^a')  # Ctrl+A
            keyboard.send_keys('{DELETE}')
            sleep(self.config.pause_between_actions)
            self.logger.info("Campo limpo")
        except Exception as e:
            self.logger.error(f"Erro ao limpar campo: {str(e)}")
            raise


class DesktopMouse:
    """
    Controlador de mouse para automação desktop
    """

    def __init__(self):
        self.logger = Logger.get_logger(self.__class__.__name__)

    def move_to(self, x: int, y: int, duration: float = 0.5) -> None:
        """
        Move mouse para posição

        Args:
            x: Coordenada X
            y: Coordenada Y
            duration: Duração do movimento em segundos
        """
        pyautogui.moveTo(x, y, duration=duration)
        self.logger.debug(f"Mouse movido para ({x}, {y})")

    def click(self, x: int, y: int, button: str = 'left', clicks: int = 1) -> None:
        """
        Clica em posição

        Args:
            x: Coordenada X
            y: Coordenada Y
            button: Botão (left, right, middle)
            clicks: Número de cliques
        """
        pyautogui.click(x, y, clicks=clicks, button=button)
        self.logger.info(f"Clique {button} em ({x}, {y})")

    def double_click(self, x: int, y: int) -> None:
        """Duplo clique em posição"""
        pyautogui.doubleClick(x, y)
        self.logger.info(f"Duplo clique em ({x}, {y})")

    def right_click(self, x: int, y: int) -> None:
        """Clique direito em posição"""
        self.click(x, y, button='right')

    def drag_and_drop(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 0.5) -> None:
        """
        Arrasta e solta

        Args:
            start_x: X inicial
            start_y: Y inicial
            end_x: X final
            end_y: Y final
            duration: Duração da ação
        """
        pyautogui.drag(end_x - start_x, end_y - start_y, duration=duration)
        self.logger.info(f"Arrasta de ({start_x}, {start_y}) para ({end_x}, {end_y})")

    def scroll(self, x: int, y: int, amount: int = 5) -> None:
        """
        Scroll na posição

        Args:
            x: Coordenada X
            y: Coordenada Y
            amount: Quantidade de scroll (positivo = cima)
        """
        self.move_to(x, y)
        pyautogui.scroll(amount)
        self.logger.debug(f"Scroll realizado em ({x}, {y}): {amount}")

    def get_position(self) -> Tuple[int, int]:
        """Obtém posição atual do mouse"""
        return pyautogui.position()


class DesktopKeyboard:
    """
    Controlador de teclado para automação desktop
    """

    def __init__(self):
        self.logger = Logger.get_logger(self.__class__.__name__)

    def press_key(self, key: str) -> None:
        """
        Pressiona uma tecla

        Args:
            key: Nome da tecla (enter, tab, etc)
        """
        pyautogui.press(key)
        self.logger.debug(f"Tecla pressionada: {key}")

    def type_text(self, text: str, interval: float = 0.05) -> None:
        """
        Digita texto

        Args:
            text: Texto a digitar
            interval: Intervalo entre caracteres
        """
        pyautogui.typewrite(text, interval=interval)
        self.logger.info(f"Texto digitado: {text[:30]}...")

    def hot_key(self, *keys) -> None:
        """
        Pressiona combinação de teclas

        Args:
            *keys: Teclas para combinar (ex: 'ctrl', 'a')
        """
        pyautogui.hotkey(*keys)
        self.logger.info(f"Combinação de teclas: {' + '.join(keys)}")

    def key_down(self, key: str) -> None:
        """Pressiona e mantém tecla"""
        pyautogui.keyDown(key)
        self.logger.debug(f"Tecla pressionada (hold): {key}")

    def key_up(self, key: str) -> None:
        """Solta tecla"""
        pyautogui.keyUp(key)
        self.logger.debug(f"Tecla solta: {key}")


class DesktopScreenshot:
    """
    Gerenciador de screenshots para desktop
    """

    def __init__(self):
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.screenshots_dir = Path("screenshots")
        self.screenshots_dir.mkdir(exist_ok=True)

    def take_screenshot(self, file_name: Optional[str] = None) -> Path:
        """
        Captura screenshot

        Args:
            file_name: Nome do arquivo (opcional, auto-gera se não fornecido)

        Returns:
            Path do arquivo capturado
        """
        if not file_name:
            from datetime import datetime
            file_name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

        file_path = self.screenshots_dir / file_name
        pyautogui.screenshot(str(file_path))
        self.logger.info(f"Screenshot capturado: {file_path}")
        return file_path

    def take_screenshot_of_region(self, x: int, y: int, width: int, height: int, file_name: str) -> Path:
        """
        Captura screenshot de região específica

        Args:
            x: Coordenada X
            y: Coordenada Y
            width: Largura
            height: Altura
            file_name: Nome do arquivo

        Returns:
            Path do arquivo capturado
        """
        file_path = self.screenshots_dir / file_name
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        screenshot.save(str(file_path))
        self.logger.info(f"Screenshot de região capturado: {file_path}")
        return file_path

    def find_image_on_screen(self, image_path: str) -> Optional[Tuple[int, int]]:
        """
        Localiza imagem na tela

        Args:
            image_path: Caminho da imagem

        Returns:
            Coordenadas (x, y) ou None
        """
        try:
            location = pyautogui.locateOnScreen(image_path)
            if location:
                self.logger.info(f"Imagem encontrada em: {location}")
                return location
            self.logger.warning(f"Imagem não encontrada: {image_path}")
            return None
        except Exception as e:
            self.logger.error(f"Erro ao localizar imagem: {str(e)}")
            return None

    def click_on_image(self, image_path: str) -> bool:
        """
        Clica em imagem se encontrada na tela

        Args:
            image_path: Caminho da imagem

        Returns:
            True se clicou, False caso contrário
        """
        location = self.find_image_on_screen(image_path)
        if location:
            pyautogui.click(location)
            self.logger.info(f"Clique realizado na imagem: {image_path}")
            return True
        return False
