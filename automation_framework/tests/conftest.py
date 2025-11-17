"""
Configuração do pytest
Garante que o módulo automation_framework está no path
"""

import sys
from pathlib import Path

# Adicionar raiz do projeto ao path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
