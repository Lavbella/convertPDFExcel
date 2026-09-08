# -*- mode: python ; coding: utf-8 -*-
import os
import sys
import streamlit
import pdfplumber
import pypdfium2
import pdfminer
from PyInstaller.utils.hooks import copy_metadata, collect_all, get_package_paths

hiddenimports = []
datas = [
    ("app.py", "."),      # O script com a interface Streamlit
    ("run_app.py", "."),  # O script de arranque definitivo criado por si
]

# 🔥 FORÇAR A INCLUSÃO FÍSICA DAS PASTAS CRÍTICAS QUE FALHAM
streamlit_dir = os.path.dirname(streamlit.__file__)
pdfplumber_dir = os.path.dirname(pdfplumber.__file__)
pypdfium2_dir = os.path.dirname(pypdfium2.__file__)
pdfminer_dir = os.path.dirname(pdfminer.__file__)

datas.append((streamlit_dir, "streamlit"))
datas.append((pdfplumber_dir, "pdfplumber"))
datas.append((pypdfium2_dir, "pypdfium2"))
datas.append((pdfminer_dir, "pdfminer"))

# 🔥 CORREÇÃO 1: Extrair corretamente as strings do tuplo retornado pelo get_package_paths
try:
    streamlit_paths = get_package_paths("streamlit")
    if streamlit_paths and isinstance(streamlit_paths, tuple):
        # O get_package_paths devolve (pure_lib_path, plat_lib_path)
        for path in streamlit_paths:
            if path and isinstance(path, str):
                datas.append((path, "streamlit"))
    elif streamlit_paths and isinstance(streamlit_paths, str):
        datas.append((streamlit_paths, "streamlit"))
except Exception:
    pass

# Pacotes vitais que precisam de metadados, ficheiros binários e dados completos
packages_to_collect = ["streamlit", "pandas", "xlsxwriter", "pdfplumber", "pypdfium2", "pdfminer", "openpyxl", "jinja2", "requests", "markupsafe"]

for pkg in packages_to_collect:
    try:
        hi, d, b = collect_all(pkg)
        
        # Filtrar e garantir que adicionamos apenas NOMES de módulos (strings) válidos
        for item in hi:
            if isinstance(item, str) and not item.endswith('.py') and '\\' not in item and '/' not in item:
                hiddenimports.append(item)
                
        datas.extend(d)
        datas.extend(copy_metadata(pkg))
    except Exception:
        pass

# Submódulos ocultos do ecossistema Streamlit que falham frequentemente em executáveis
hiddenimports.extend([
    "streamlit.web",
    "streamlit.web.cli",
    "streamlit.runtime",
    "streamlit.runtime.scriptrunner",
    "streamlit.runtime.runtime",
    "streamlit.config",
    "jinja2.meta",
    "altair.vegalite.v5.schema.mixins",  
    "altair.vegalite.v5.schema.core",    
])

# Filtrar e limpar duplicados de hiddenimports
hiddenimports = list(set([str(h) for h in hiddenimports if h]))

# 2. Análise do PyInstaller apontando diretamente para o seu run_app.py
a = Analysis(
    ["run_app.py"],  
    pathex=["."],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="ConvertPDFExcelApp",
    debug=False,
    strip=False,
    upx=True,
    console=True,  
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="ConvertPDFExcelApp",
)
