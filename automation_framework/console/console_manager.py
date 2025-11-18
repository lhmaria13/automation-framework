"""
Gerenciador de processos console e aplicações CLI
Suporta execução de comandos, captura de saída e interação
"""

import subprocess
import threading
from typing import Optional, List, Tuple
from pathlib import Path
import os
import signal

from automation_framework.core.logger import Logger
from automation_framework.core.config import ConfigManager
from automation_framework.core.exceptions import ConsoleAutomationException


class ConsoleProcess:
    """
    Gerenciador de processo console/CLI
    """

    def __init__(self, working_dir: Optional[str] = None):
        self.process: Optional[subprocess.Popen] = None
        self.output: List[str] = []
        self.error_output: List[str] = []
        self.working_dir = working_dir or os.getcwd()
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.config = ConfigManager().get_console_config()
        self.is_running = False

    def execute_command(self, command: str, timeout: Optional[int] = None, capture_output: bool = True) -> Tuple[str, str, int]:
        """
        Executa comando no console

        Args:
            command: Comando a executar
            timeout: Timeout em segundos
            capture_output: Se deve capturar saída

        Returns:
            Tupla (stdout, stderr, return_code)
        """
        timeout = timeout or self.config.timeout

        try:
            self.logger.info(f"Executando comando: {command}")

            result = subprocess.run(
                command,
                cwd=self.working_dir,
                shell=True,
                capture_output=capture_output,
                timeout=timeout,
                text=True,
                encoding=self.config.encoding,
                errors=getattr(self.config, 'encoding_errors', 'replace')
            )

            # result.stdout / result.stderr podem ser None em alguns ambientes;
            # normalizar para string vazia antes de usar .strip()
            stdout = (result.stdout or "").strip()
            stderr = (result.stderr or "").strip()

            if capture_output:
                self.output.append(stdout)
                if stderr:
                    self.error_output.append(stderr)

            self.logger.debug(f"Comando executado com código de saída: {result.returncode}")

            if result.returncode != 0 and stderr:
                self.logger.warning(f"Erro na execução: {stderr}")

            return stdout, stderr, result.returncode

        except subprocess.TimeoutExpired:
            self.logger.error(f"Timeout ao executar comando: {command}")
            raise ConsoleAutomationException(f"Timeout ao executar comando: {command}")
        except Exception as e:
            self.logger.error(f"Erro ao executar comando: {str(e)}")
            raise ConsoleAutomationException(f"Erro ao executar comando: {str(e)}")

    def start_process(self, command: str) -> None:
        """
        Inicia processo interativo

        Args:
            command: Comando a executar
        """
        try:
            self.logger.info(f"Iniciando processo: {command}")

            self.process = subprocess.Popen(
                command,
                cwd=self.working_dir,
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding=self.config.encoding,
                errors=getattr(self.config, 'encoding_errors', 'replace'),
                bufsize=1
            )

            self.is_running = True
            self.logger.info(f"Processo iniciado com PID: {self.process.pid}")

        except Exception as e:
            self.logger.error(f"Erro ao iniciar processo: {str(e)}")
            raise ConsoleAutomationException(f"Erro ao iniciar processo: {str(e)}")

    def write_input(self, input_text: str) -> None:
        """
        Escreve entrada para processo

        Args:
            input_text: Texto a enviar
        """
        if not self.process:
            raise ConsoleAutomationException("Nenhum processo em execução")

        try:
            self.process.stdin.write(input_text + '\n')
            self.process.stdin.flush()
            self.logger.debug(f"Entrada enviada: {input_text}")
        except Exception as e:
            self.logger.error(f"Erro ao enviar entrada: {str(e)}")
            raise

    def read_output(self, timeout: Optional[int] = None) -> str:
        """
        Lê saída do processo

        Args:
            timeout: Timeout para leitura

        Returns:
            Saída lida
        """
        if not self.process:
            raise ConsoleAutomationException("Nenhum processo em execução")

        try:
            output, _ = self.process.communicate(timeout=timeout)
            self.is_running = False
            # output pode ser None em alguns casos; normalizar antes de usar
            return (output or "").strip()
        except subprocess.TimeoutExpired:
            self.logger.warning("Timeout ao ler saída do processo")
            return ""
        except Exception as e:
            self.logger.error(f"Erro ao ler saída: {str(e)}")
            raise

    def terminate_process(self) -> None:
        """Termina o processo"""
        if self.process and self.is_running:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
                self.is_running = False
                self.logger.info("Processo encerrado")
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.logger.info("Processo finalizado (killed)")
            except Exception as e:
                self.logger.warning(f"Erro ao terminar processo: {str(e)}")

    def get_last_output(self) -> str:
        """Obtém última linha de saída"""
        return self.output[-1] if self.output else ""

    def get_all_output(self) -> str:
        """Obtém toda saída capturada"""
        return '\n'.join(self.output)

    def clear_output(self) -> None:
        """Limpa histórico de saída"""
        self.output.clear()
        self.error_output.clear()


class JavaApplicationManager:
    """
    Gerenciador especializado para aplicações Java
    """

    def __init__(self, java_home: Optional[str] = None):
        self.java_home = java_home or os.environ.get('JAVA_HOME', 'java')
        self.process: Optional[ConsoleProcess] = None
        self.logger = Logger.get_logger(self.__class__.__name__)

    def run_jar_file(self, jar_path: str, args: Optional[List[str]] = None, timeout: Optional[int] = None) -> Tuple[str, str, int]:
        """
        Executa arquivo JAR

        Args:
            jar_path: Caminho do arquivo JAR
            args: Argumentos para a aplicação
            timeout: Timeout de execução

        Returns:
            Tupla (stdout, stderr, return_code)
        """
        if not Path(jar_path).exists():
            raise FileNotFoundError(f"Arquivo JAR não encontrado: {jar_path}")

        args_str = ' '.join(args) if args else ''
        command = f"{self.java_home} -jar {jar_path} {args_str}".strip()

        process = ConsoleProcess()
        return process.execute_command(command, timeout)

    def run_java_class(self, class_name: str, classpath: str, args: Optional[List[str]] = None) -> Tuple[str, str, int]:
        """
        Executa classe Java

        Args:
            class_name: Nome qualificado da classe
            classpath: Classpath para execução
            args: Argumentos para a aplicação

        Returns:
            Tupla (stdout, stderr, return_code)
        """
        args_str = ' '.join(args) if args else ''
        command = f"{self.java_home} -cp {classpath} {class_name} {args_str}".strip()

        process = ConsoleProcess()
        return process.execute_command(command)

    def get_java_version(self) -> str:
        """Obtém versão do Java"""
        process = ConsoleProcess()
        stdout, _, _ = process.execute_command(f"{self.java_home} -version 2>&1")
        return stdout


class CommandBuilder:
    """
    Builder para construir comandos complexos
    """

    def __init__(self, base_command: str):
        self.command = base_command
        self.args: List[str] = []
        self.env_vars: dict = {}

    def add_argument(self, key: str, value: Optional[str] = None) -> 'CommandBuilder':
        """Adiciona argumento ao comando"""
        if value:
            self.args.append(f'{key} {value}')
        else:
            self.args.append(key)
        return self

    def add_flag(self, flag: str) -> 'CommandBuilder':
        """Adiciona flag ao comando"""
        self.args.append(f'-{flag}')
        return self

    def add_env_var(self, key: str, value: str) -> 'CommandBuilder':
        """Adiciona variável de ambiente"""
        self.env_vars[key] = value
        return self

    def build(self) -> str:
        """Constrói comando final"""
        full_command = self.command
        if self.args:
            full_command += ' ' + ' '.join(self.args)
        return full_command

    def execute(self, timeout: Optional[int] = None) -> Tuple[str, str, int]:
        """Executa comando construído"""
        process = ConsoleProcess()
        command = self.build()

        # Adicionar variáveis de ambiente
        if self.env_vars:
            for key, value in self.env_vars.items():
                os.environ[key] = value

        return process.execute_command(command, timeout)

    def __str__(self) -> str:
        return self.build()
