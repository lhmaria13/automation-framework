# Automation Framework - Guia de Implementação

## Passo 1: Instalação

```bash
# Instale as dependências
pip install -r requirements.txt
```

## Passo 2: Estruture seus testes

```
seu-projeto/
├── automation_framework/    # Framework (inclua na raiz ou em site-packages)
├── tests/
│   ├── test_web.py
│   ├── test_desktop.py
│   └── test_console.py
├── pages/                   # Page Objects da sua aplicação
│   ├── login_page.py
│   └── dashboard_page.py
├── data/                    # Dados de teste
│   ├── credentials.json
│   └── test_data.csv
├── screenshots/             # Screenshots automáticos
├── logs/                    # Logs
├── requirements.txt
└── config.json
```

## Passo 3: Crie seu primeiro Page Object

`pages/exemplo_page.py`:

```python
from automation_framework.web.page_object import BasePage
from automation_framework.web.locators import Locator

class ExemploPage(BasePage):
    # Defina seus localizadores
    TITULO = Locator.xpath("//h1")
    CAMPO_BUSCA = Locator.css_selector("input[name='q']")
    BOTAO_ENVIAR = Locator.id("submit-btn")
    RESULTADOS = Locator.css_selector("div.resultado")
    
    def obter_titulo(self) -> str:
        return self.get_text(self.TITULO)
    
    def realizar_busca(self, termo: str) -> None:
        self.type_text(self.CAMPO_BUSCA, termo)
        self.click(self.BOTAO_ENVIAR)
        
    def contar_resultados(self) -> int:
        elementos = self.find_elements(self.RESULTADOS)
        return len(elementos)
```

## Passo 4: Crie seu primeiro teste

`tests/test_exemplo.py`:

```python
import pytest
from automation_framework.web.driver_manager import DriverManager
from pages.exemplo_page import ExemploPage

class TestExemplo:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.driver_manager = DriverManager()
        self.driver = self.driver_manager.initialize_browser('chrome')
        yield
        self.driver_manager.quit_browser()
    
    def test_busca(self):
        page = ExemploPage(self.driver)
        page.navigate_to("https://www.exemplo.com")
        
        # Assert
        assert page.obter_titulo() == "Bem-vindo"
        
        # Ação
        page.realizar_busca("Python")
        
        # Assert
        assert page.contar_resultados() > 0
```

## Passo 5: Execute os testes

```bash
# Teste individual
pytest tests/test_exemplo.py::TestExemplo::test_busca -v

# Todos os testes com coverage
pytest tests/ --cov=automation_framework --cov-report=html

# Com paralelização
pip install pytest-xdist
pytest tests/ -n auto
```

## Padrões Recomendados

### 1. Page Factory Pattern

```python
class BasePageFactory:
    def __init__(self, driver):
        self.driver = driver
    
    def create_page(self, page_class):
        return page_class(self.driver)
```

### 2. Componentes Reutilizáveis

```python
from automation_framework.web.page_object import BaseComponent

class HeaderComponent(BaseComponent):
    LOGO = Locator.css_selector("header .logo")
    MENU = Locator.css_selector("nav ul li")
    
    def clique_no_logo(self):
        self.click(self.LOGO)
```

### 3. Fixtures do Pytest

```python
@pytest.fixture
def driver():
    manager = DriverManager()
    driver = manager.initialize_browser('chrome')
    yield driver
    manager.quit_browser()

@pytest.fixture
def browser_types():
    return ['chrome', 'firefox', 'edge']
```

### 4. Parametrização

```python
@pytest.mark.parametrize("usuario,senha", [
    ("user1", "pass1"),
    ("user2", "pass2"),
])
def test_login(driver, usuario, senha):
    page = LoginPage(driver)
    page.login(usuario, senha)
```

## Integração com CI/CD

### GitHub Actions

`.github/workflows/tests.yml`:

```yaml
name: Automated Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: pytest tests/ --cov
```

## Troubleshooting

### Problema: Elemento não encontrado
- Aumente `implicit_wait` em config.json
- Verifique o localizador com inspector
- Use `wait_for_element()` para waits explícitos

### Problema: Timeout em processos
- Aumente `timeout` em console ou desktop config
- Verifique se processo está respondendo
- Veja logs em `logs/`

### Problema: Driver não inicializa
- Verifique instalação do webdriver (webdriver-manager resolve automaticamente)
- Confirme que navegador está instalado
- Limpe cache: `rm -rf .wdm/`

## Próximas Melhorias

1. Implementar relatórios com Allure
2. Adicionar suporte a múltiplas plataformas (Linux, macOS)
3. Criar mock server para testes offline
4. Implementar image recognition avançado
5. Integrar com ferramentas de performance

---

**Bom desenvolvimento!** 🚀
