# -*- mode: python ; coding: utf-8 -*-

import os
import streamlit
import pdfplumber
import pypdfium2
import pdfminer
import camelot
import tabula
import pdf2image

from PyInstaller.utils.hooks import (
    copy_metadata,
    collect_all
)

hiddenimports = []
datas = []

# --------------------------------------------------
# Ficheiros da aplicação
# --------------------------------------------------

datas += [
    ("app.py", "."),
    ("run_app.py", "."),
]

# --------------------------------------------------
# Pastas críticas
# --------------------------------------------------

datas += [
    (os.path.dirname(streamlit.__file__), "streamlit"),
    (os.path.dirname(pdfplumber.__file__), "pdfplumber"),
    (os.path.dirname(pypdfium2.__file__), "pypdfium2"),
    (os.path.dirname(pdfminer.__file__), "pdfminer"),
    (os.path.dirname(camelot.__file__), "camelot"),
    (os.path.dirname(tabula.__file__), "tabula"),
    (os.path.dirname(pdf2image.__file__), "pdf2image"),
]

# --------------------------------------------------
# Pacotes a recolher
# --------------------------------------------------

packages_to_collect = [
    "streamlit",
    "pandas",
    "xlsxwriter",
    "pdfplumber",
    "pypdfium2",
    "openpyxl",
    "jinja2",
    "requests",
    "markupsafe",
]

for pkg in packages_to_collect:

    try:

        hi, d, b = collect_all(pkg)

        # Apenas strings válidas
        for item in hi:

            if isinstance(item, str):

                hiddenimports.append(item)

        datas.extend(d)

        try:
            datas.extend(copy_metadata(pkg))
        except Exception:
            pass

    except Exception as e:

        print(f"Erro ao recolher {pkg}: {e}")

# Limpar hiddenimports
hiddenimports = [
    h
    for h in hiddenimports
    if isinstance(h, str)
]

# Remover duplicados
hiddenimports = list(set(hiddenimports))

# --------------------------------------------------
# Imports ocultos
# --------------------------------------------------

hiddenimports.extend([

    # Streamlit
    "streamlit.web",
    "streamlit.web.cli",
    "streamlit.runtime",
    "streamlit.runtime.scriptrunner",
    "streamlit.runtime.runtime",
    "streamlit.config",

    # Altair
    "altair.vegalite.v5.schema.mixins",
    "altair.vegalite.v5.schema.core",

    # Camelot
    "camelot",
    "camelot.parsers",
    "camelot.core",
    "camelot.handlers",

    # Tabula
    "tabula",
    "tabula.io",

    # OCR
    "pytesseract",

    # PDF2Image
    "pdf2image",

    # Dependências frequentes
    "cv2",
    "numpy",
    "PIL",
])

hiddenimports = list(
    set(
        [
            h
            for h in hiddenimports
            if isinstance(h, str)
        ]
    )
)

# --------------------------------------------------
# Analysis
# --------------------------------------------------

a = Analysis(
    ["run_app.py"],
    pathex=["."],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=["hooks"],
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