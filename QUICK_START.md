# 🎯 GUIA RÁPIDO - AUTOMATION FRAMEWORK

## ⚡ 30 SEGUNDOS PARA COMEÇAR

### 1. Instale as dependências
```bash
pip install -r requirements.txt
```

### 2. Crie seu primeiro teste
```python
from automation_framework.web.driver_manager import DriverManager
from automation_framework.web.page_object import BasePage
from automation_framework.web.locators import Locator

class GooglePage(BasePage):
    SEARCH_INPUT = Locator.name("q")
    SEARCH_BTN = Locator.xpath("//button[contains(., 'Pesquisar')]")
    
    def search(self, query):
        self.type_text(self.SEARCH_INPUT, query)
        self.click(self.SEARCH_BTN)

# Uso
dm = DriverManager()
driver = dm.initialize_browser('chrome')
page = GooglePage(driver)
page.navigate_to("https://www.google.com")
page.search("Python automation")
dm.quit_browser()
```

---

## 📁 ARQUIVOS IMPORTANTES

| Arquivo | Descrição |
|---------|-----------|
| `automation_framework/` | Framework principal |
| `examples/` | 4 exemplos funcionais |
| `README.md` | Documentação completa |
| `IMPLEMENTATION_GUIDE.md` | Passo a passo |
| `config.json` | Configurações padrão |
| `requirements.txt` | Dependências |

---

## 🌐 AUTOMAÇÃO WEB

### Localizadores Disponíveis
```python
Locator.id("elemento")
Locator.name("nome")
Locator.xpath("//div")
Locator.css_selector(".classe")
Locator.class_name("classe")
Locator.tag_name("tag")
Locator.link_text("Texto")
Locator.partial_link_text("Texto parcial")
```

### Métodos Page
```python
page.navigate_to(url)
page.click(locator)
page.type_text(locator, text)
page.get_text(locator)
page.is_element_visible(locator)
page.wait_for_element(locator, timeout=10)
page.take_screenshot(filename)
page.execute_script(script)
page.get_current_url()
page.refresh()

# Tabelas
table = page.get_table(locator)
table.get_row_count()
table.get_cell_text(row, col)
table.get_all_data()

# Formulários
form = page.get_form(locator)
form.fill_text_field("nome", "valor")
form.select_dropdown("campo", "opção")
form.check_checkbox("campo")
form.submit()
```

---

## 🖥️ AUTOMAÇÃO DESKTOP

### Iniciar Aplicação
```python
from automation_framework.desktop.desktop_manager import (
    DesktopApplication, DesktopMouse, DesktopKeyboard, DesktopScreenshot
)

app = DesktopApplication()
app.launch_application("C:\\Windows\\notepad.exe")
app.close_application()
```

### Mouse
```python
mouse = DesktopMouse()
mouse.move_to(100, 100)
mouse.click(100, 100)
mouse.double_click(100, 100)
mouse.right_click(100, 100)
mouse.drag_and_drop(10, 10, 100, 100)
mouse.scroll(100, 100, amount=5)
x, y = mouse.get_position()
```

### Teclado
```python
keyboard = DesktopKeyboard()
keyboard.press_key('enter')
keyboard.type_text("Olá")
keyboard.hot_key('ctrl', 'a')
keyboard.key_down('shift')
keyboard.key_up('shift')
```

### Screenshots
```python
screenshot = DesktopScreenshot()
screenshot.take_screenshot("teste.png")
screenshot.take_screenshot_of_region(0, 0, 800, 600, "region.png")
location = screenshot.find_image_on_screen("imagem.png")
screenshot.click_on_image("imagem.png")
```

---

## 💻 AUTOMAÇÃO CONSOLE

### Executar Comando
```python
from automation_framework.console.console_manager import ConsoleProcess

process = ConsoleProcess()
stdout, stderr, code = process.execute_command("dir", timeout=10)
print(f"Saída: {stdout}")
print(f"Código: {code}")
```

### Processo Interativo
```python
process.start_process("cmd")
process.write_input("dir")
output = process.read_output(timeout=5)
process.terminate_process()
```

### Java
```python
from automation_framework.console.console_manager import JavaApplicationManager

java = JavaApplicationManager()
stdout, stderr, code = java.run_jar_file("app.jar", ["--arg1", "valor"])
version = java.get_java_version()
```

### CommandBuilder
```python
from automation_framework.console.console_manager import CommandBuilder

cmd = CommandBuilder("npm")
cmd.add_argument("run", "build")
cmd.add_flag("watch")
cmd.add_env_var("NODE_ENV", "development")
stdout, stderr, code = cmd.execute()
```

---

## ⏱️ WAITS E RETRY

### Wait Simples
```python
from automation_framework.utils.wait import Wait

waiter = Wait(timeout=10, poll_frequency=0.5)
waiter.until(lambda: elemento_apareceu(), "Elemento não apareceu")
waiter.until_not(lambda: elemento_desapareceu(), "Elemento ainda visível")
```

### Wait com Valor
```python
waiter.until_value_changes(lambda: get_texto())
waiter.until_value_equals(lambda: contador, 10)
waiter.until_no_exception(lambda: get_elemento())
```

### Retry
```python
from automation_framework.utils.wait import Retry

retrier = Retry(max_attempts=3, delay=1.0, backoff=2.0)
resultado = retrier.execute(funcao_instavel)

# Ou usar função helper
from automation_framework.utils.wait import retry
resultado = retry(funcao_instavel, max_attempts=3)
```

---

## 🔐 CREDENCIAIS E DADOS

### Credenciais
```python
from automation_framework.utils.credentials import CredentialManager

cred = CredentialManager()
usuario = cred.get_credential("APP_USER", "padrao")
cred.set_credential("token", "abc123")
cred.save_credentials("credenciais.json")

# Via variáveis de ambiente
os.environ['APP_USER'] = 'admin'
usuario = cred.get_credential("APP_USER")  # Lê do ambiente
```

### Dados
```python
from automation_framework.utils.data import DataHelper

# JSON
data = DataHelper.parse_json('{"nome": "teste"}')
json_str = DataHelper.to_json(data)
DataHelper.load_json_file("dados.json")
DataHelper.save_json_file(data, "saida.json")

# CSV
dados = DataHelper.load_csv_file("dados.csv", headers=True)
DataHelper.save_csv_file(dados, "saida.csv")

# Dicionário
flat = DataHelper.flatten_dict({"a": {"b": {"c": 1}}})
diff = DataHelper.compare_dictionaries(dict1, dict2)
```

---

## ⚙️ CONFIGURAÇÃO

### Via config.json
```json
{
  "browser": {
    "browser_type": "chrome",
    "headless": false,
    "implicit_wait": 10
  },
  "logging": {
    "level": "INFO"
  }
}
```

### Via Código
```python
from automation_framework.core.config import ConfigManager

config = ConfigManager()
config.load_from_json("config.json")
config.set('browser.headless', True)
config.load_from_env("AUTO_")  # Variáveis AUTO_*
```

### Via Variáveis de Ambiente
```bash
export AUTO_BROWSER_HEADLESS=true
export AUTO_BROWSER_IMPLICIT_WAIT=15
```

---

## 📊 LOGGING

### Usar Logger
```python
from automation_framework.core.logger import Logger

logger = Logger.get_logger(__name__)
logger.info("Informação")
logger.debug("Debug")
logger.warning("Aviso")
logger.error("Erro")

# Logs salvos em: logs/
```

### Limpar Logs
```python
Logger.clear_logs()
```

---

## 🧪 TESTES COM PYTEST

### Estrutura Básica
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
        # Seu teste aqui
        assert True
```

### Executar Testes
```bash
pytest tests/ -v
pytest tests/ --cov=automation_framework
pytest tests/test_web.py::TestClass::test_method -v
pytest tests/ -n auto  # Paralelo
```

---

## 🔄 ALTERNANDO NAVEGADORES

```python
dm = DriverManager()

# Iniciar com Chrome
driver = dm.initialize_browser('chrome')
# ... usar driver ...

# Trocar para Firefox
driver = dm.switch_browser('firefox')
# ... usar driver com Firefox ...

# Trocar para Edge
driver = dm.switch_browser('edge')

# Encerrar
dm.quit_browser()
```

---

## 💡 EXEMPLOS PRONTOS

Execute os exemplos:
```bash
python automation_framework/examples/example_web_automation.py
python automation_framework/examples/example_desktop_automation.py
python automation_framework/examples/example_console_automation.py
python automation_framework/examples/example_utilities.py
```

---

## 🚨 EXCEÇÕES

Todas customizadas para melhor tratamento:
```python
from automation_framework.core.exceptions import (
    ElementNotFound,
    TimeoutException,
    BrowserException,
    DesktopAutomationException,
    ConsoleAutomationException,
    InvalidBrowserType
)

try:
    page.click(locator)
except ElementNotFound:
    print("Elemento não encontrado")
except TimeoutException:
    print("Timeout aguardando")
```

---

## 📞 PRECISA DE AJUDA?

1. **Documentação** → `README.md`
2. **Implementação** → `IMPLEMENTATION_GUIDE.md`
3. **Exemplos** → `automation_framework/examples/`
4. **Docstrings** → `help(ClassName)` no Python
5. **Testes** → `automation_framework/tests/`

---

## ✅ CHECKLIST INICIAL

- [ ] Instalou dependências: `pip install -r requirements.txt`
- [ ] Leu `README.md`
- [ ] Executou um exemplo
- [ ] Criou seu primeiro Page Object
- [ ] Criou seu primeiro teste
- [ ] Testou com `pytest`
- [ ] Configurou variáveis de ambiente
- [ ] Explorou os helpers (Table, Form, etc)
- [ ] Experimentou Wait e Retry
- [ ] Está pronto para sua automação!

---

**Versão:** 1.0.0 | **Status:** ✅ Pronto para usar | **Data:** 13/11/2025
