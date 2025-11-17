"""
Exemplo 3: Automação Console e Comandos CLI
Demonstra execução e interação com console
"""

from automation_framework.console.console_manager import (
    ConsoleProcess,
    JavaApplicationManager,
    CommandBuilder
)
from automation_framework.core.logger import Logger


def main():
    logger = Logger.get_logger(__name__)
    logger.info("Iniciando exemplo de automação console")

    # Exemplo 1: Executar comando simples
    logger.info("--- Exemplo 1: Comando Simples ---")
    process = ConsoleProcess()
    stdout, stderr, code = process.execute_command("echo Automação Console")
    logger.info(f"Saída: {stdout}")
    logger.info(f"Código de saída: {code}")

    # Exemplo 2: Usar CommandBuilder
    logger.info("--- Exemplo 2: CommandBuilder ---")
    builder = CommandBuilder("dir")
    builder.add_argument("/B")  # Bare format
    command = builder.build()
    logger.info(f"Comando construído: {command}")

    stdout, stderr, code = process.execute_command(command)
    logger.info(f"Arquivos encontrados: {len(stdout.splitlines())}")

    # Exemplo 3: Processo interativo
    logger.info("--- Exemplo 3: Processo Interativo ---")
    interactive = ConsoleProcess()
    interactive.start_process("cmd")

    interactive.write_input("cd .")
    interactive.write_input("echo Teste interativo")

    import time
    time.sleep(2)

    output = interactive.read_output()
    logger.info(f"Saída do processo interativo: {output[:100]}...")

    interactive.terminate_process()

    # Exemplo 4: Java (se instalado)
    logger.info("--- Exemplo 4: Java ---")
    try:
        java_manager = JavaApplicationManager()
        java_version = java_manager.get_java_version()
        logger.info(f"Versão Java: {java_version[:50]}...")
    except Exception as e:
        logger.warning(f"Java não disponível: {str(e)}")


if __name__ == "__main__":
    main()
