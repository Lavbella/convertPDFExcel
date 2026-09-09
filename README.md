# 📊 Universal PDF to Excel Converter

Convert PDF documents into Excel spreadsheets using multiple extraction engines, automatically selecting the best available method for each document.

---

##  Features

- ✅ Upload PDF documents through a modern Streamlit interface
- ✅ Extract tables from native PDFs
- ✅ Support PDF files generated from Excel
- ✅ Support structured text PDFs
- ✅ OCR support for scanned/image-based PDFs
- ✅ Export extracted data to Excel (.xlsx)
- ✅ Automatic fallback mechanism
- ✅ Multi-sheet Excel generation
- ✅ Preview extracted data before download

---

## Extraction Workflow

The application uses a layered extraction strategy to maximize success rates:

```text
                PDF Document
                      │
                      ▼
          ┌──────────────────────┐
          │      Camelot         │
          │  Structured Tables   │
          └──────────┬───────────┘
                     │
         Success? ───┤
                     ▼ No
          ┌──────────────────────┐
          │       Tabula         │
          │ PDF Table Extraction │
          └──────────┬───────────┘
                     │
         Success? ───┤
                     ▼ No
          ┌──────────────────────┐
          │     pdfplumber       │
          │  Text/Table Parsing  │
          └──────────┬───────────┘
                     │
         Success? ───┤
                     ▼ No
          ┌──────────────────────┐
          │   Tesseract OCR      │
          │ Scanned Documents    │
          └──────────┬───────────┘
                     │
                     ▼
                 Excel File
```

---

##  Built With

- Python
- Streamlit
- Pandas
- Camelot 0.11
- Tabula
- pdfplumber
- Tesseract OCR
- pdf2image
- XlsxWriter

---

##  Requirements

### Python

- Python 3.10+

### External Dependencies

| Component | Purpose |
|------------|----------|
| Java | Required by Tabula |
| Ghostscript | Required by Camelot |
| Poppler | Required by pdf2image |
| Tesseract OCR | Required for scanned PDFs |

---

#  Installation

## 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/universal-pdf-to-excel.git

cd universal-pdf-to-excel
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv .venv
```

### Activate Environment

```bash
.venv\Scripts\activate
```

---

## 3. Install Python Packages

### Using requirements.txt

```bash
pip install -r requirements.txt
```

### Or manually

```bash
pip install streamlit
pip install pandas
pip install pdfplumber
pip install camelot-py
pip install tabula-py
pip install pdf2image
pip install pytesseract
pip install xlsxwriter
```

---

#  Install External Dependencies

## Java

Check installation:

```bash
java -version
```

Expected result:

```text
java version "1.8.x"
```

---

## Ghostscript

Check installation:

```bash
gswin64c -version
```

If command is not found:

1. Locate:

```text
C:\Program Files\gs\...\bin
```

2. Add folder to Windows PATH

3. Restart VS Code

---

## Poppler

Check installation:

```bash
pdfinfo -v
```

If not installed:

- Download Poppler for Windows
- Add Poppler `bin` folder to PATH

Example:

```text
C:\poppler\Library\bin
```

---

## Tesseract OCR

Check installation:

```bash
tesseract --version
```

Recommended languages:

- English (eng)
- Portuguese (por)

---

#  Run Application

Start Streamlit:

```bash
streamlit run app.py
```

Open browser:

```text
http://localhost:8501
```

---

# 📁 Project Structure

```text
universal-pdf-to-excel/
│
├── app.py
├── requirements.txt
├── README.md
│
├── assets/
│
├── output/
│
└── temp/
```

---

#  Build Executable

## Install PyInstaller

```bash
pip install pyinstaller
```

---

## Create EXE

```bash
pyinstaller --onefile app.py
```

Generated executable:

```text
dist/
└── app.exe
```

---

## Create EXE with Icon

```bash
pyinstaller --onefile --icon=assets/icon.ico app.py
```

---

## Recommended Production Build

```bash
pyinstaller ^
--onefile ^
--windowed ^
--icon=assets/icon.ico ^
app.py
```

---

#  Deployment

### Option 1 - Streamlit Cloud

Deploy directly from GitHub:

```text
GitHub ➜ Streamlit Cloud ➜ Deploy
```

---

### Option 2 - Windows Executable

Package:

```text
app.exe
Poppler
Ghostscript
Tesseract
```

---

### Option 3 - Internal Corporate Deployment

- Windows Server
- Azure Web App
- Azure Container Apps
- Docker

---

#  Supported PDF Types

| PDF Type | Supported |
|-----------|------------|
| Excel Generated PDFs | ✅ |
| Financial Reports | ✅ |
| Invoices | ✅ |
| Structured Tables | ✅ |
| Scanned Documents | ✅ |
| Multi-page Documents | ✅ |
| Mixed Layout PDFs | ✅ |

---

#  Project Objective

This project was created to provide a simple, reliable, and free solution for converting PDF documents into structured Excel spreadsheets, regardless of their source format or complexity.

By combining multiple extraction technologies and OCR capabilities, the application significantly increases data recovery success rates compared to single-library PDF conversion tools.

---
#  Windows Setup

To ensure all extraction engines work correctly on Windows, install and configure the following components.

---

## Java (Required by Tabula)

Verify installation:

```powershell
java -version
```

Example:

```text
java version "1.8.0_481"
```

If Java is not installed:

```powershell
winget install Microsoft.OpenJDK.21
```

---

## Ghostscript (Required by Camelot)

Download:

https://ghostscript.com/releases/gsdnld.html

After installation verify:

```powershell
gswin64c -version
```

If the command is not recognized:

1. Locate the installation folder:

```text
C:\Program Files\gs\gsXX.XX.X\bin
```

2. Add the folder to the Windows PATH environment variable.

Example:

```text
C:\Program Files\gs\gs10.05.1\bin
```

3. Restart VS Code.

Verify:

```powershell
where gswin64c
```

---

## Tesseract OCR (Required for Scanned PDFs)

Download:

https://github.com/UB-Mannheim/tesseract/wiki

Recommended languages:

- English (eng)
- Portuguese (por)

Verify installation:

```powershell
tesseract --version
```

Example Python configuration:

```python
import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
```

---

## Poppler (Required by pdf2image)

Download:

https://github.com/oschwartz10612/poppler-windows/releases

Extract to:

```text
C:\poppler
```

Add to PATH:

```text
C:\poppler\Library\bin
```

Verify:

```powershell
pdfinfo -v
```

---

#  Verify Installation

Run:

```python
import camelot
import tabula
import pdfplumber
import pytesseract
import pdf2image

print("All dependencies loaded successfully")
```

or

```powershell
python -c "import camelot, tabula, pdfplumber, pytesseract, pdf2image; print('OK')"
```

Expected result:

```text
OK
```


#  Contributing

Contributions are welcome!

Feel free to:

- Open Issues
- Submit Pull Requests
- Suggest Improvements
- Report Bugs

---

#  Support

If you found this project useful:

 Star the repository

🔄 Share it with your network

Contribute with ideas and improvements

---

# 📄 License

This project is licensed under the MIT License.

---

**Created with Python and Streamlit**
