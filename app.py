import streamlit as st
import pandas as pd
import pdfplumber
import camelot
import tabula
import tempfile
import io

from pdf2image import convert_from_path
import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

st.set_page_config(
    page_title="PDF para Excel",
    page_icon="📊"
)

st.title("📊 Conversor Universal PDF → Excel")

uploaded_file = st.file_uploader(
    "Escolha um PDF",
    type=["pdf"]
)

###########################################################################
# UTILIDADES
###########################################################################

def clean_dataframe(df):

    df = df.fillna("")

    # remover linhas totalmente vazias
    df = df[
        ~(df.astype(str)
            .apply(
                lambda x: ''.join(x).strip(),
                axis=1
            ) == "")
    ]

    return df


###########################################################################
# CAMELOT
###########################################################################

def extract_with_camelot(pdf_path):

    tables = camelot.read_pdf(
        pdf_path,
        pages="all",
        flavor="stream"
    )

    dfs = []

    for table in tables:

        df = table.df

        df = clean_dataframe(df)

        if not df.empty:
            dfs.append(df)

    return dfs


###########################################################################
# TABULA
###########################################################################

def extract_with_tabula(pdf_path):

    tables = tabula.read_pdf(
        pdf_path,
        pages="all",
        multiple_tables=True
    )

    dfs = []

    for table in tables:

        if table is not None and not table.empty:

            table = clean_dataframe(table)

            dfs.append(table)

    return dfs


###########################################################################
# PDFPLUMBER
###########################################################################

def extract_with_pdfplumber(pdf_path):

    dfs = []

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            tables = page.extract_tables()

            for table in tables:

                if not table:
                    continue

                max_cols = max(len(row) for row in table if row)

                rows = []

                for row in table:

                    if row:

                        row = [
                            str(cell).strip()
                            if cell else ""
                            for cell in row
                        ]

                        row += [""] * (max_cols - len(row))

                        rows.append(row)

                if rows:

                    headers = [
                        f"Coluna_{i+1}"
                        for i in range(max_cols)
                    ]

                    df = pd.DataFrame(
                        rows,
                        columns=headers
                    )

                    df = clean_dataframe(df)

                    dfs.append(df)

    return dfs


###########################################################################
# OCR
###########################################################################

def extract_with_ocr(pdf_path):

    pages = convert_from_path(pdf_path)

    data = []

    for page in pages:

        text = pytesseract.image_to_string(
            page,
            lang="por"
        )

        lines = text.split("\n")

        for line in lines:

            line = line.strip()

            if line:
                data.append([line])

    if not data:
        return []

    df = pd.DataFrame(
        data,
        columns=["Texto"]
    )

    return [df]


###########################################################################
# PROCESSAMENTO
###########################################################################

if uploaded_file:

    if st.button("Converter"):

        with st.spinner("A processar PDF..."):

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as tmp:

                tmp.write(uploaded_file.read())

                pdf_path = tmp.name

            tables = []

            ################################################################
            # 1. CAMELOT
            ################################################################

            try:

                st.info("A tentar Camelot...")

                tables = extract_with_camelot(pdf_path)

                if tables:
                    st.success(
                        f"Camelot encontrou {len(tables)} tabela(s)"
                    )

            except Exception as e:

                st.warning(f"Camelot falhou: {e}")

            ################################################################
            # 2. TABULA
            ################################################################

            if not tables:

                try:

                    st.info("A tentar Tabula...")

                    tables = extract_with_tabula(pdf_path)

                    if tables:
                        st.success(
                            f"Tabula encontrou {len(tables)} tabela(s)"
                        )

                except Exception as e:

                    st.warning(f"Tabula falhou: {e}")

            ################################################################
            # 3. PDFPLUMBER
            ################################################################

            if not tables:

                try:

                    st.info("A tentar pdfplumber...")

                    tables = extract_with_pdfplumber(pdf_path)

                    if tables:
                        st.success(
                            f"pdfplumber encontrou {len(tables)} tabela(s)"
                        )

                except Exception as e:

                    st.warning(
                        f"pdfplumber falhou: {e}"
                    )

            ################################################################
            # 4. OCR
            ################################################################

            if not tables:

                try:

                    st.info("A tentar OCR...")

                    tables = extract_with_ocr(pdf_path)

                    if tables:
                        st.success(
                            "OCR executado com sucesso"
                        )

                except Exception as e:

                    st.warning(f"OCR falhou: {e}")

            ################################################################
            # RESULTADO
            ################################################################

            if tables:

                output = io.BytesIO()

                with pd.ExcelWriter(
                    output,
                    engine="xlsxwriter"
                ) as writer:

                    for idx, df in enumerate(
                        tables,
                        start=1
                    ):

                        nome_folha = f"Tabela_{idx}"

                        df.to_excel(
                            writer,
                            sheet_name=nome_folha[:31],
                            index=False
                        )

                excel_data = output.getvalue()

                st.success(
                    f"Extraídas {len(tables)} tabelas."
                )

                for i, df in enumerate(tables):

                    st.subheader(
                        f"Tabela {i+1}"
                    )

                    st.dataframe(
                        df.head(20)
                    )

                st.download_button(
                    "📥 Descarregar Excel",
                    data=excel_data,
                    file_name="pdf_convertido.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            else:

                st.error(
                    "Não foi possível extrair dados do PDF."
                )