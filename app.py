import streamlit as st
import pdfplumber
import pandas as pd
import io

# Configuração inicial da página Streamlit
st.set_page_config(page_title="Conversor PDF para Excel", page_icon="📊", layout="centered")

st.title("📊 Conversor de PDF para Excel")
st.write("Insira um ficheiro PDF (originalmente gerado a partir de um Excel) para recuperar as tabelas.")

# Upload do ficheiro PDF
uploaded_file = st.file_uploader("Escolha o ficheiro PDF", type=["pdf"])

if uploaded_file is not None:
    st.success("Ficheiro carregado com sucesso!")
    
    # Botão para iniciar o processamento
    if st.button("Processar e Extrair Dados"):
        with st.spinner("A extrair dados do PDF..."):
            all_tables = []
            
            # Abrir o PDF diretamente da memória
            with pdfplumber.open(uploaded_file) as pdf:
                headers = None  # Guardará o cabeçalho definitivo da primeira página
                
                for i, page in enumerate(pdf.pages):
                    tables = page.extract_tables()
                    for table in tables:
                        if not table:
                            continue
                        
                        # Se for a PRIMEIRA página, extraímos o cabeçalho
                        if headers is None:
                            # Tratar cabeçalhos vazios ou nulos da primeira linha
                            raw_header = [str(cell).strip() if cell else "" for cell in table[0]]
                            
                            # Garantir que todos os nomes são únicos para o Pandas não falhar
                            headers = []
                            for idx, name in enumerate(raw_header):
                                if name == "" or name in headers:
                                    headers.append(f"{name or 'Coluna'}_{idx}")
                                else:
                                    headers.append(name)
                            
                            # O resto da tabela são os dados desta primeira página
                            dados_pagina = table[1:]
                        else:
                            # Nas páginas seguintes, se a primeira linha for igual ao cabeçalho original, ignoramos
                            primeira_linha = [str(cell).strip() if cell else "" for cell in table[0]]
                            
                            # Se a primeira linha parecer um cabeçalho repetido, saltamos
                            if primeira_linha == raw_header or any(elem in primeira_linha for elem in raw_header if elem != ""):
                                dados_pagina = table[1:]
                            else:
                                dados_pagina = table  # Caso contrário, já são dados puros
                        
                        # Criar o DataFrame com os dados da página e as colunas fixas
                        if dados_pagina:
                            df = pd.DataFrame(dados_pagina, columns=headers)
                            all_tables.append(df)

            
            if all_tables:
                # Combinar todas as tabelas encontradas num único DataFrame ou processar por abas
                # Para este exemplo simples, vamos concatenar verticalmente
                final_df = pd.concat(all_tables, ignore_index=True)

                # 🔥 NOVA LINHA: Calcular o total de registos reais extraídos
                total_linhas = len(final_df)
                
                st.subheader("Visualização dos Dados Extraídos")
                st.metric(label="Total de Linhas Recuperadas (sem cabeçalho)", value=f"{total_linhas} linhas")
                # st.dataframe(final_df.head(10))
                st.dataframe(final_df, height=500)  # Mostra todas as linhas numa caixa com scroll de 500 píxeis
                # Criar um buffer em memória para guardar o ficheiro Excel
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    final_df.to_excel(writer, index=False, sheet_name='Dados Extraídos')
                
                # Preparar os dados binários para o botão de download
                excel_data = output.getvalue()
                
                st.write("---")
                # Botão para o utilizador descarregar o ficheiro convertido
                st.download_button(
                    label="📥 Descarregar Ficheiro Excel",
                    data=excel_data,
                    file_name="pdf_convertido.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.error("Não foram encontradas tabelas estruturadas neste PDF. Verifique se o PDF é nativo e não uma imagem digitalizada.")