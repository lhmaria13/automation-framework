"""
Exemplo 2: Automação Desktop Windows
Demonstra interação com aplicações Windows
"""
import sys
from pathlib import Path
import time

# Garantir que a raiz do projeto esteja no sys.path para permitir execução
# a partir da pasta `automation_framework/` ou de qualquer outra
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

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
        app.launch_application(r"C:\Windows\notepad.exe")
        logger.info("Notepad iniciado")
        time.sleep(1)  # Aguardar Notepad abrir

        # Usar clipboard para suportar caracteres especiais (acentos)
        import subprocess
        
        # Função auxiliar para copiar texto para clipboard e colar
        def type_with_clipboard(text):
            """Copia texto para clipboard e cola (suporta acentos)"""
            # Copiar para clipboard usando powershell
            ps_cmd = f'[System.Windows.Forms.SendKeys]::SendWait("' + text.replace('"', '\\"') + '")'
            subprocess.run(['powershell', '-Command', f'Set-Clipboard -Value @"\n{text}\n"@'], check=True)
            time.sleep(0.2)
            # Colar com Ctrl+V
            keyboard = DesktopKeyboard()
            keyboard.hot_key('ctrl', 'v')
            time.sleep(0.3)
        
        # Escrever texto com acentos
        type_with_clipboard("Olá, Framework de Automação!")
        
        # Pressionar Enter
        keyboard = DesktopKeyboard()
        keyboard.press_key('enter')
        time.sleep(0.3)
        
        type_with_clipboard("Este é um exemplo de automação desktop.")

        logger.info("Texto digitado")
        time.sleep(1)

        # Capturar screenshot
        screenshot = DesktopScreenshot()
        screenshot.take_screenshot("notepad_example.png")

        logger.info("Screenshot capturado")
        time.sleep(1)
        
        # Salvar arquivo (Ctrl+S)
        keyboard.hot_key('ctrl', 's')
        time.sleep(1)  # Aguardar diálogo abrir
        
        # Digitar caminho e nome do arquivo no diálogo "Salvar como"
        import subprocess
        file_path = r"C:\Users\lhmaria1\OneDrive - Stefanini\Desktop\Automacao_Framework.txt"
        subprocess.run(['powershell', '-Command', f'Set-Clipboard -Value "{file_path}"'], check=True)
        time.sleep(0.2)
        keyboard.hot_key('ctrl', 'a')  # Selecionar tudo no campo
        time.sleep(0.2)
        keyboard.hot_key('ctrl', 'v')  # Colar caminho
        time.sleep(0.5)
        keyboard.press_key('enter')  # Pressionar Enter (ou clicar Salvar)
        time.sleep(1)
        
        # Fechar aplicação (Alt+F4)
        keyboard.hot_key('alt', 'f4')
        time.sleep(0.5)

    finally:
        # Fechar aplicação
        app.close_application()
        logger.info("Aplicação encerrada")


if __name__ == "__main__":
    main()
