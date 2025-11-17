"""
Utility para garantir que drivers de navegador estejam instalados/atualizados
Baixa os drivers usando webdriver-manager e armazena na pasta `drivers/` do projeto.
"""
from pathlib import Path
from typing import Optional
import logging
import shutil

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


logger = logging.getLogger(__name__)


def _default_drivers_dir() -> Path:
    # pasta raiz do projeto: automation_framework/.. -> Framework
    return Path(__file__).resolve().parents[2] / "drivers"


def ensure_driver_installed(browser_type: str, target_dir: Optional[str] = None, force_download: bool = False) -> str:
    """
    Garante que o driver do `browser_type` esteja disponível em `target_dir`.
    Usa `webdriver-manager` para baixar o driver (em seu cache) e copia o executável para a pasta do projeto.

    Args:
        browser_type: 'chrome' | 'firefox' | 'edge'
        target_dir: Pasta onde salvar o driver (se None, usa ./drivers no projeto)
        force_download: Se True, remove qualquer driver existente no destino e força cópia do cache

    Returns:
        caminho absoluto para o executável do driver
    """
    drivers_dir = Path(target_dir) if target_dir else _default_drivers_dir()
    drivers_dir.mkdir(parents=True, exist_ok=True)

    browser = browser_type.lower()

    if browser == 'chrome':
        manager = ChromeDriverManager()
    elif browser == 'firefox':
        manager = GeckoDriverManager()
    elif browser == 'edge':
        manager = EdgeChromiumDriverManager()
    else:
        raise ValueError(f"Tipo de navegador não suportado: {browser_type}")

    # Remover drivers antigos no destino se for forçar
    if force_download:
        for p in drivers_dir.glob('*'):
            try:
                if p.is_file():
                    p.unlink()
            except Exception:
                pass

    try:
        # manager.install() baixa para cache do webdriver-manager e retorna o caminho do executável
        cached_executable = Path(manager.install())

        # Copiar para a pasta de drivers do projeto, a não ser que já exista
        destination = drivers_dir / cached_executable.name

        if not destination.exists() or force_download:
            shutil.copy2(str(cached_executable), str(destination))

        logger.info(f"Driver para {browser} disponível em: {str(destination.resolve())}")
        return str(destination.resolve())
    except Exception as e:
        logger.exception(f"Falha ao instalar driver para {browser}: {e}")
        raise


def ensure_all_drivers(target_dir: Optional[str] = None, browsers: Optional[list] = None) -> dict:
    """Garante drivers para múltiplos navegadores e retorna mapeamento browser->path"""
    browsers = browsers or ['chrome', 'firefox', 'edge']
    results = {}

    for b in browsers:
        path = ensure_driver_installed(b, target_dir=target_dir)
        results[b] = path

    return results
