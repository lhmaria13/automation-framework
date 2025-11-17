"""
VERIFICAÇÃO DE INSTALAÇÃO DO FRAMEWORK
Execute este script para verificar se tudo está configurado corretamente
"""

import sys
from pathlib import Path
import importlib.util

def check_file_exists(file_path, description):
    """Verifica se arquivo existe"""
    exists = Path(file_path).exists()
    status = "✅ OK" if exists else "❌ FALTA"
    print(f"{status:<12} {description:<50} {file_path if not exists else ''}")
    return exists

def check_module_import(module_name, description):
    """Verifica se módulo pode ser importado"""
    try:
        __import__(module_name)
        print(f"✅ OK       {description:<50}")
        return True
    except ImportError as e:
        print(f"❌ FALTA    {description:<50} (Erro: {str(e)[:40]}...)")
        return False

def main():
    print("="*80)
    print("🔍 VERIFICAÇÃO DO FRAMEWORK DE AUTOMAÇÕES")
    print("="*80)
    
    base_path = Path(__file__).parent
    
    # 1. Verificar estrutura de pastas
    print("\n📁 ESTRUTURA DE PASTAS")
    print("-" * 80)
    
    folders = [
        ("automation_framework/core", "Core do framework"),
        ("automation_framework/web", "Módulo Web"),
        ("automation_framework/desktop", "Módulo Desktop"),
        ("automation_framework/console", "Módulo Console"),
        ("automation_framework/utils", "Módulo Utils"),
        ("automation_framework/examples", "Exemplos"),
        ("automation_framework/tests", "Testes"),
    ]
    
    folders_ok = sum(check_file_exists(base_path / f, d) for f, d in folders)
    
    # 2. Verificar arquivos principais
    print("\n📄 ARQUIVOS PRINCIPAIS")
    print("-" * 80)
    
    main_files = [
        ("automation_framework/__init__.py", "Init do framework"),
        ("automation_framework/core/logger.py", "Logger"),
        ("automation_framework/core/config.py", "Config Manager"),
        ("automation_framework/core/exceptions.py", "Exceções"),
        ("automation_framework/web/driver_manager.py", "Driver Manager"),
        ("automation_framework/web/page_object.py", "Page Objects"),
        ("automation_framework/web/locators.py", "Locators"),
        ("automation_framework/desktop/desktop_manager.py", "Desktop Manager"),
        ("automation_framework/console/console_manager.py", "Console Manager"),
        ("automation_framework/utils/wait.py", "Wait & Retry"),
        ("automation_framework/utils/credentials.py", "Credentials"),
        ("automation_framework/utils/data.py", "Data Helper"),
        ("automation_framework/examples/example_web_automation.py", "Exemplo Web"),
        ("automation_framework/examples/example_desktop_automation.py", "Exemplo Desktop"),
        ("automation_framework/examples/example_console_automation.py", "Exemplo Console"),
        ("automation_framework/examples/example_utilities.py", "Exemplo Utilities"),
        ("automation_framework/tests/test_framework_core.py", "Testes"),
        ("automation_framework/config.json", "Config JSON"),
        ("automation_framework/README.md", "README"),
        ("requirements.txt", "Requirements"),
        ("QUICK_START.md", "Quick Start"),
        ("IMPLEMENTATION_GUIDE.md", "Implementation Guide"),
        ("CHANGELOG_AND_CHECKLIST.md", "Checklist"),
        (".env.example", ".env Example"),
    ]
    
    files_ok = sum(check_file_exists(base_path / f, d) for f, d in main_files)
    
    # 3. Verificar dependências
    print("\n📦 DEPENDÊNCIAS PYTHON")
    print("-" * 80)
    
    dependencies = [
        ("selenium", "Selenium"),
        ("pyautogui", "PyAutoGUI"),
        ("pywinauto", "PyWinAuto"),
    ]
    
    deps_ok = sum(check_module_import(d, f"{f} (versão do sistema)") for d, f in dependencies)
    
    # 4. Verificar módulos do framework
    print("\n🔧 MÓDULOS DO FRAMEWORK")
    print("-" * 80)
    
    framework_modules = [
        ("automation_framework.core.logger", "Logger"),
        ("automation_framework.core.config", "ConfigManager"),
        ("automation_framework.core.exceptions", "Exceções"),
        ("automation_framework.web.driver_manager", "DriverManager"),
        ("automation_framework.web.page_object", "Page Objects"),
        ("automation_framework.web.locators", "Locators"),
        ("automation_framework.desktop.desktop_manager", "Desktop"),
        ("automation_framework.console.console_manager", "Console"),
        ("automation_framework.utils.wait", "Wait & Retry"),
        ("automation_framework.utils.credentials", "Credentials"),
        ("automation_framework.utils.data", "Data Helper"),
    ]
    
    modules_ok = sum(check_module_import(m, f"{d:<40}") for m, d in framework_modules)
    
    # 5. Resumo
    print("\n" + "="*80)
    print("📊 RESUMO")
    print("="*80)
    
    total_folders = len(folders)
    total_files = len(main_files)
    total_deps = len(dependencies)
    total_modules = len(framework_modules)
    
    print(f"Pastas:       {folders_ok:2d}/{total_folders:2d} ✅" if folders_ok == total_folders else f"Pastas:       {folders_ok:2d}/{total_folders:2d} ⚠️")
    print(f"Arquivos:     {files_ok:2d}/{total_files:2d} ✅" if files_ok == total_files else f"Arquivos:     {files_ok:2d}/{total_files:2d} ⚠️")
    print(f"Dependências: {deps_ok:2d}/{total_deps:2d} {'✅' if deps_ok == total_deps else '⚠️'} (instale com: pip install -r requirements.txt)")
    print(f"Módulos:      {modules_ok:2d}/{total_modules:2d} {'✅' if modules_ok == total_modules else '⚠️'}")
    
    # 6. Próximos passos
    print("\n" + "="*80)
    print("🚀 PRÓXIMOS PASSOS")
    print("="*80)
    
    steps = [
        "1. Leia 'QUICK_START.md' para começar rápido",
        "2. Leia 'README.md' para documentação completa",
        "3. Execute 'python automation_framework/examples/example_web_automation.py'",
        "4. Crie sua primeira página: 'pages/minha_pagina.py'",
        "5. Crie seu primeiro teste: 'tests/test_meu_app.py'",
        "6. Execute: 'pytest tests/ -v'",
    ]
    
    for step in steps:
        print(f"  {step}")
    
    # Status final
    print("\n" + "="*80)
    if modules_ok == total_modules and files_ok == total_files:
        print("✅ FRAMEWORK PRONTO PARA USO!")
        print("="*80)
        return 0
    else:
        print("⚠️  FRAMEWORK COM PROBLEMAS")
        print("Instale as dependências: pip install -r requirements.txt")
        print("="*80)
        return 1

if __name__ == "__main__":
    sys.exit(main())
