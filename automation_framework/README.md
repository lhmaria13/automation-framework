# Automation Framework - Framework Padrão para Automações em Python

Framework completo e reutilizável para automações em Python, com suporte a navegadores, aplicações Windows e console.

## Características Principais

### 1. **Automação Web** 🌐
- ✅ Suporte multi-navegador (Chrome, Firefox, Edge)
- ✅ Troca dinâmica de navegador
- ✅ Padrão Page Object Model
- ✅ Localizadores fluentes
- ✅ Waits inteligentes
- ✅ Helpers para tabelas e formulários

### 2. **Automação Desktop** 🖥️
- ✅ Controle de mouse e teclado
- ✅ Interação com aplicações Windows
- ✅ Screenshots e busca de imagens
- ✅ Automação pyautogui + pywinauto

### 3. **Automação Console/CLI** 💻
- ✅ Execução de comandos
- ✅ Processos interativos
- ✅ Suporte a aplicações Java
- ✅ Builder de comandos complexos

### 4. **Sistema Core** ⚙️
- ✅ Configuração centralizada
- ✅ Logging estruturado
- ✅ Gerenciamento de credenciais
- ✅ Sistema de exceções customizado

### 5. **Utilitários** 🛠️
- ✅ Waits e Retry com backoff exponencial
- ✅ Manipulação de dados (JSON, CSV, dicionários)
- ✅ Helpers para conversões

## Estrutura do Projeto

```
automation_framework/
├── core/
│   ├── logger.py              # Logging centralizado
│   ├── config.py              # Gerenciamento de configurações
│   └── exceptions.py          # Exceções customizadas
├── web/
│   ├── driver_manager.py      # Gerenciador de WebDrivers
│   ├── page_object.py         # Base pages e componentes
│   └── locators.py            # Localizadores fluentes
├── desktop/
│   └── desktop_manager.py     # Automação Windows
├── console/
│   └── console_manager.py     # Automação CLI/Java
├── utils/
│   ├── wait.py               # Waits e Retry
│   ├── credentials.py        # Gerenciamento de credenciais
│   └── data.py               # Helpers de dados
├── examples/                 # Exemplos práticos
└── config.json              # Arquivo de configuração
```

## Instalação

### Dependências

```bash
pip install selenium webdriver-manager pyautogui pywinauto
```

### Setup Completo

```bash
# Clone ou copie o framework para seu projeto
cd seu-projeto
cp -r automation_framework .

# Instale as dependências
pip install -r requirements.txt
```

## Guia de Uso Rápido

### Automação Web

```python
from automation_framework.web.driver_manager import DriverManager
from automation_framework.web.page_object import BasePage
from automation_framework.web.locators import Locator

class MinhaPage(BasePage):
    BOTAO = Locator.css_selector(".btn-submit")
    
    def clicar_botao(self):
        self.click(self.BOTAO)

# Uso
driver_manager = DriverManager()
driver = driver_manager.initialize_browser('chrome')

page = MinhaPage(driver)
page.navigate_to("https://exemplo.com")
page.clicar_botao()

driver_manager.quit_browser()
```

### Automação Desktop

```python
from automation_framework.desktop.desktop_manager import (
    DesktopApplication,
    DesktopMouse,
    DesktopKeyboard
)

app = DesktopApplication()
app.launch_application("notepad.exe")

keyboard = DesktopKeyboard()
keyboard.type_text("Olá Mundo!")

mouse = DesktopMouse()
mouse.click(100, 100)

app.close_application()
```

### Automação Console

```python
from automation_framework.console.console_manager import ConsoleProcess

process = ConsoleProcess()
stdout, stderr, code = process.execute_command("dir")
print(stdout)
```

### Utilities

```python
from automation_framework.utils.wait import Wait
from automation_framework.utils.credentials import CredentialManager

# Wait
waiter = Wait(timeout=10)
waiter.until(lambda: elemento_carregado())

# Credenciais
cred = CredentialManager()
usuario = cred.get_credential("admin_user")
```

## Configuração

### Via arquivo JSON

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
  }
}
```

### Via código

```python
from automation_framework.core.config import ConfigManager

config = ConfigManager()
config.set('browser.headless', True)
config.set('browser.implicit_wait', 15)
```

### Via variáveis de ambiente

```bash
export AUTO_BROWSER_HEADLESS=true
export AUTO_BROWSER_IMPLICIT_WAIT=10
```

## Page Objects Avançado

```python
from automation_framework.web.page_object import BasePage, BaseComponent
from automation_framework.web.locators import Locator, Table, Form

class LoginComponent(BaseComponent):
    USERNAME_INPUT = Locator.id("username")
    PASSWORD_INPUT = Locator.id("password")
    LOGIN_BTN = Locator.xpath("//button[@type='submit']")
    
    def login(self, user, password):
        self.click(self.USERNAME_INPUT)
        self.driver.type_text(self.USERNAME_INPUT.by, self.USERNAME_INPUT.value, user)
        self.click(self.PASSWORD_INPUT)
        self.driver.type_text(self.PASSWORD_INPUT.by, self.PASSWORD_INPUT.value, password)
        self.click(self.LOGIN_BTN)

class DashboardPage(BasePage):
    LOGIN_COMPONENT = Locator.id("login-form")
    
    def get_login_component(self):
        return LoginComponent(self.driver, self.LOGIN_COMPONENT)
```

## Padrões e Boas Práticas

### 1. Sempre use Page Objects
```python
# ✅ BOM
class LoginPage(BasePage):
    USERNAME = Locator.id("user")
    def login(self, user): self.type_text(self.USERNAME, user)

# ❌ EVITAR
driver.find_element(By.ID, "user").send_keys("user")
```

### 2. Use Logger para rastreamento
```python
logger = Logger.get_logger(__name__)
logger.info("Iniciando teste")
```

### 3. Implemente Waits apropriados
```python
# ✅ BOM
waiter = Wait(timeout=10)
waiter.until(element_visible)

# ❌ EVITAR
time.sleep(5)
```

### 4. Gerencie recursos com context manager
```python
with DriverManager() as driver:
    # Use driver aqui
    pass
# Driver encerrado automaticamente
```

## Exemplos Completos

Veja a pasta `examples/` para:
- `example_web_automation.py` - Automação web com Page Objects
- `example_desktop_automation.py` - Automação Windows
- `example_console_automation.py` - Automação CLI/Java
- `example_utilities.py` - Uso de utilities

## Logging

Todos os eventos são registrados em `logs/` com rotação automática:

```
logs/
├── automation_framework.web.driver_manager.log
├── automation_framework.desktop.desktop_manager.log
└── automation_framework.console.console_manager.log
```

## Exceções Customizadas

```python
from automation_framework.core.exceptions import (
    ElementNotFound,
    TimeoutException,
    BrowserException,
    DesktopAutomationException,
    ConsoleAutomationException
)
```

## Contribuição e Extensão

Para adicionar novos browsers:

```python
from automation_framework.web.driver_manager import BaseWebDriver

class SafariWebDriver(BaseWebDriver):
    def _create_options(self):
        # Implementar opções
        pass
    
    def _create_driver(self):
        # Implementar driver
        pass
```

## Performance e Otimização

- Use `headless=true` para testes rápidos
- Implemente waits adequados para evitar timeouts
- Reutilize instâncias de driver quando possível
- Use `screenshot_on_error=true` em desktop para debug

## Próximos Passos

1. Estenda Page Objects para suas páginas específicas
2. Crie componentes reutilizáveis
3. Integre com framework de testes (pytest, unittest)
4. Implemente relatórios com screenshot em falhas
5. Configure CI/CD com o framework

## Suporte

Para dúvidas ou melhorias, consulte os exemplos e a documentação em docstrings do código.

---

**Versão:** 1.0.0  
**Autor:** Automation Team  
**Licença:** MIT
