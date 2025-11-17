"""
Exemplo 2: Automação Desktop Windows
Demonstra interação com aplicações Windows
"""

from automation_framework.desktop.desktop_manager import (
    DesktopApplication,
    DesktopMouse,
    DesktopKeyboard,
    DesktopScreenshot
)
from automation_framework.core.logger import Logger


def main():
    logger = Logger.get_logger(__name__)
    logger.info("Iniciando exemplo de automação desktop")

    # Inicializar aplicação
    app = DesktopApplication()

    try:
        # Iniciar Notepad
        app.launch_application("notepad.exe")
        logger.info("Notepad iniciado")

        # Escrever texto
        keyboard = DesktopKeyboard()
        keyboard.type_text("Olá, Framework de Automação!")

        # Pressionar Enter
        keyboard.press_key("enter")
        keyboard.type_text("Este é um exemplo de automação desktop.")

        logger.info("Texto digitado")

        # Capturar screenshot
        screenshot = DesktopScreenshot()
        screenshot.take_screenshot("notepad_example.png")

        logger.info("Screenshot capturado")

    finally:
        # Fechar aplicação
        app.close_application()
        logger.info("Aplicação encerrada")


if __name__ == "__main__":
    main()
