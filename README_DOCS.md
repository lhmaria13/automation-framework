# 📚 ÍNDICE DE DOCUMENTAÇÃO E REFERÊNCIA

## 🎯 Comece por aqui

### Para Iniciantes
1. **[QUICK_START.md](QUICK_START.md)** ⭐ - Guia rápido de 30 segundos
2. **[README.md](automation_framework/README.md)** - Documentação principal
3. **[IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)** - Passo a passo

### Para Desenvolvedores Experientes
1. **[Exemplos Funcionais](automation_framework/examples/)** - 4 exemplos prontos
2. **[API Reference](#referência-rápida-de-api)** - Referência abaixo
3. **[Padrões de Design](#padrões-de-design)** - Arquitetura

---

## 📖 Documentação Detalhada

### Módulo Core
- **[Logger](automation_framework/core/logger.py)** - Sistema de logging centralizado
  - Singleton Pattern
  - Múltiplos níveis (DEBUG, INFO, WARNING, ERROR)
  - Rotação automática de arquivos

- **[Config](automation_framework/core/config.py)** - Gerenciamento de configurações
  - Carrega de JSON, ambiente, código
  - Notação de ponto para acesso (ex: `browser.headless`)
  - Padrões para browser, logging, desktop, console

- **[Exceptions](automation_framework/core/exceptions.py)** - Exceções customizadas
  - ElementNotFound, TimeoutException
  - BrowserException, DesktopAutomationException
  - ConsoleAutomationException, InvalidBrowserType

### Módulo Web
- **[DriverManager](automation_framework/web/driver_manager.py)** - Gerenciador de WebDrivers
  - Suporte Chrome, Firefox, Edge
  - Troca dinâmica de navegador
  - Factory + Singleton Pattern
  - Context manager support

- **[Page Objects](automation_framework/web/page_object.py)** - Page Object Model
  - BasePage - classe base para páginas
  - BaseComponent - para componentes reutilizáveis
  - Métodos: navigate, click, type_text, wait_for_element, etc

- **[Locators](automation_framework/web/locators.py)** - Localizadores fluentes
  - Locator - encapsula By + value
  - ElementHelper - métodos úteis para elementos
  - Table - helpers para tabelas HTML
  - Form - helpers para formulários

### Módulo Desktop
- **[Desktop Manager](automation_framework/desktop/desktop_manager.py)** - Automação Windows
  - DesktopApplication - iniciar/conectar/fechar apps
  - DesktopMouse - controle de mouse
  - DesktopKeyboard - controle de teclado
  - DesktopScreenshot - screenshots e busca de imagens

### Módulo Console
- **[Console Manager](automation_framework/console/console_manager.py)** - Automação CLI/Java
  - ConsoleProcess - executar comandos
  - JavaApplicationManager - suporte para Java
  - CommandBuilder - construir comandos complexos

### Módulo Utils
- **[Wait](automation_framework/utils/wait.py)** - Waits e Retry
  - Wait - esperar com poll_frequency
  - Retry - retry com backoff exponencial
  - Funções helper: wait_for, retry

- **[Credentials](automation_framework/utils/credentials.py)** - Gerenciamento de credenciais
  - CredentialManager - Singleton seguro
  - Prioridade: ENV > arquivo > padrão

- **[Data](automation_framework/utils/data.py)** - Helpers de dados
  - JSON, CSV, dicionário
  - Flatten, compare_dictionaries

---

## 🔍 Referência Rápida de API

### Web Automation
```python
# Inicializar
from automation_framework.web.driver_manager import DriverManager
dm = DriverManager()
driver = dm.initialize_browser('chrome')  # chrome, firefox, edge
driver = dm.switch_browser('firefox')
dm.quit_browser()

# Page Object
from automation_framework.web.page_object import BasePage
from automation_framework.web.locators import Locator

class MinhaPage(BasePage):
    BOTAO = Locator.id("submit")
    
    def clicar(self):
        self.click(self.BOTAO)

page = MinhaPage(driver)
page.navigate_to(url)
page.click(Locator.xpath("//button"))
page.type_text(Locator.id("input"), "texto")
page.get_text(locator)
page.wait_for_element(locator)
page.take_screenshot("arquivo.png")
```

### Desktop Automation
```python
from automation_framework.desktop.desktop_manager import (
    DesktopApplication, DesktopMouse, DesktopKeyboard, DesktopScreenshot
)

app = DesktopApplication()
app.launch_application("notepad.exe")
app.close_application()

mouse = DesktopMouse()
mouse.click(100, 100)
mouse.drag_and_drop(10, 10, 100, 100)

keyboard = DesktopKeyboard()
keyboard.type_text("Texto")
keyboard.hot_key('ctrl', 'a')

screenshot = DesktopScreenshot()
screenshot.take_screenshot("arquivo.png")
```

### Console Automation
```python
from automation_framework.console.console_manager import (
    ConsoleProcess, JavaApplicationManager, CommandBuilder
)

# Comando simples
process = ConsoleProcess()
stdout, stderr, code = process.execute_command("dir")

# Processo interativo
process.start_process("cmd")
process.write_input("comando")
output = process.read_output()
process.terminate_process()

# Java
java = JavaApplicationManager()
stdout, _, _ = java.run_jar_file("app.jar", ["--arg"])

# CommandBuilder
cmd = CommandBuilder("npm")
cmd.add_argument("run", "build")
stdout, _, _ = cmd.execute()
```

### Utils
```python
from automation_framework.utils.wait import Wait, Retry
from automation_framework.utils.credentials import CredentialManager
from automation_framework.utils.data import DataHelper

# Wait
waiter = Wait(timeout=10)
waiter.until(lambda: elemento_apareceu())

# Retry
retrier = Retry(max_attempts=3)
resultado = retrier.execute(funcao_instavel)

# Credenciais
cred = CredentialManager()
usuario = cred.get_credential("USER")

# Data
dados = DataHelper.load_json_file("arquivo.json")
flat = DataHelper.flatten_dict(nested_dict)
```

---

## 🏗️ Padrões de Design

### Padrões Implementados

1. **Singleton Pattern**
   - ConfigManager, Logger, DriverManager
   - Garante uma única instância
   - Uso: `config = ConfigManager()`

2. **Factory Pattern**
   - DriverManager cria WebDrivers corretos
   - Uso: `driver = dm.initialize_browser('chrome')`

3. **Strategy Pattern**
   - BaseWebDriver com múltiplas implementações
   - Chrome, Firefox, Edge

4. **Builder Pattern**
   - CommandBuilder para construir comandos
   - Uso: `cmd = CommandBuilder("npm").add_argument(...)`

5. **Page Object Model**
   - BasePage e BaseComponent
   - Localização de elementos centralizada
   - Métodos reutilizáveis

---

## 📋 Exemplos por Caso de Uso

### Teste Web Simples
Ver: `automation_framework/examples/example_web_automation.py`

### Teste Desktop Simples
Ver: `automation_framework/examples/example_desktop_automation.py`

### Teste Console Simples
Ver: `automation_framework/examples/example_console_automation.py`

### Usar Utilities
Ver: `automation_framework/examples/example_utilities.py`

---

## 🔧 Configuração

### Arquivo config.json
```json
{
  "browser": {
    "browser_type": "chrome",
    "headless": false,
    "implicit_wait": 10,
    "page_load_timeout": 30
  },
  "logging": {
    "level": "INFO",
    "log_dir": "logs"
  },
  "desktop": {
    "timeout": 10,
    "pause_between_actions": 0.5
  },
  "console": {
    "timeout": 30,
    "encoding": "utf-8"
  }
}
```

### Variáveis de Ambiente
```bash
AUTO_BROWSER_HEADLESS=true
AUTO_BROWSER_IMPLICIT_WAIT=15
AUTO_LOGGING_LEVEL=DEBUG
```

---

## 🧪 Testes

### Executar Testes
```bash
pytest automation_framework/tests/ -v
pytest automation_framework/tests/ --cov=automation_framework
pytest automation_framework/tests/test_framework_core.py -v
```

### Estrutura de Teste
```python
import pytest
from automation_framework.web.driver_manager import DriverManager

class TestMeuApp:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.dm = DriverManager()
        self.driver = self.dm.initialize_browser('chrome')
        yield
        self.dm.quit_browser()
    
    def test_funcionalidade(self):
        assert True
```

---

## 🔐 Segurança

### Credenciais Seguras
```python
from automation_framework.utils.credentials import CredentialManager

# Via variável de ambiente
os.environ['DB_PASSWORD'] = 'senha'
cred = CredentialManager()
senha = cred.get_credential('db_password')

# Via arquivo (não commitar!)
cred.set_credential('api_token', 'token123')
cred.save_credentials('credenciais.json')
```

---

## ⚡ Performance

### Dicas de Otimização
1. Use `headless=true` para testes
2. Configure waits apropriados
3. Reutilize instâncias de driver
4. Use retry para operações instáveis
5. Considere paralelização com pytest-xdist

---

## 🐛 Troubleshooting

### Problema: Elemento não encontrado
- Aumentar `implicit_wait` em config.json
- Verificar localizador com inspector
- Usar `wait_for_element()` explicitamente

### Problema: Timeout
- Aumentar timeout em configuração
- Verificar se aplicação responde
- Ver logs em `logs/`

### Problema: Driver não inicializa
- Verificar instalação: `pip install -r requirements.txt`
- Limpar cache: `rm -rf .wdm/`
- Confirmar navegador instalado

---

## 📞 Suporte

- **Documentação:** README.md
- **Quick Start:** QUICK_START.md
- **Guia de Implementação:** IMPLEMENTATION_GUIDE.md
- **Exemplos:** automation_framework/examples/
- **Testes:** automation_framework/tests/

---

## 📦 Arquivos e Pastas

```
Framework/
├── automation_framework/          # Código principal
│   ├── core/                      # Core (logger, config, exceptions)
│   ├── web/                       # Web automation
│   ├── desktop/                   # Desktop automation
│   ├── console/                   # Console automation
│   ├── utils/                     # Utilities
│   ├── examples/                  # Exemplos
│   ├── tests/                     # Testes
│   ├── config.json                # Config padrão
│   └── README.md
├── requirements.txt               # Dependências
├── QUICK_START.md                 # Início rápido
├── README_DOCS.md                 # Este arquivo
├── IMPLEMENTATION_GUIDE.md        # Guia detalhado
├── CHANGELOG_AND_CHECKLIST.md     # Checklist
└── verify_installation.py         # Verificar instalação
```

---

## ✨ Pronto para Começar!

1. **Instale:** `pip install -r requirements.txt`
2. **Leia:** `QUICK_START.md` ou `README.md`
3. **Execute:** Um dos exemplos
4. **Crie:** Sua primeira página e teste
5. **Divirta-se:** Automatizando! 🚀

---

**Versão:** 1.0.0  
**Última atualização:** 13 de novembro de 2025  
**Status:** ✅ Pronto para Produção
