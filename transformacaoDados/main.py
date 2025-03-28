import os
import sys
import zipfile
import pandas as pd
from pdfminer.high_level import extract_text

# Ajustar caminho para importar utils.py do diretório correto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRAPING_DIR = os.path.abspath(os.path.join(BASE_DIR, "../webScraping"))
sys.path.append(SCRAPING_DIR)

from utils import criarPasta  # Importação do utils do webScraping

# Definir caminhos
pastaDownloads = os.path.join(SCRAPING_DIR, "downloads")
pastaOutput = os.path.join(BASE_DIR, "arquivoZip")
arquivoPdf = os.path.join(pastaDownloads, "Anexo_1.pdf")  # Ajuste conforme necessário
arquivoCsv = os.path.join(pastaOutput, "dados_transformados.csv")
arquivoZip = os.path.join(pastaOutput, "Teste_Andrey.zip")  # Substituir "SeuNome"

# Criar diretório de saída
criarPasta(pastaOutput)

def extrairTextoPdf(caminhoPdf):
    """Extrai o texto de um PDF."""
    try:
        texto = extract_text(caminhoPdf)
        return texto
    except Exception as e:
        print(f"Erro ao extrair texto do PDF: {e}")
        return ""

def transformarDados(texto):
    """Transforma o texto extraído do PDF em um DataFrame estruturado."""
    linhas = texto.split("\n")
    dados = []
    for linha in linhas:
        colunas = linha.split()
        if len(colunas) >= 3:  # Ajuste conforme a estrutura do PDF
            dados.append(colunas)
    
    df = pd.DataFrame(dados, columns=["CODIGO", "DESCRICAO", "AMB", "OD"])
    
    # Substituir abreviações
    legenda = {"AMB": "Ambulatorial", "OD": "Hospitalar"}
    df.replace({"AMB": legenda["AMB"], "OD": legenda["OD"]}, inplace=True)
    
    return df

if os.path.exists(arquivoPdf):
    print(f"Processando {arquivoPdf}...")
    texto = extrairTextoPdf(arquivoPdf)
    df = transformarDados(texto)
    
    df.to_csv(arquivoCsv, index=False, encoding="utf-8-sig")
    print(f"Dados salvos em {arquivoCsv}")
    
    # Compactar CSV em ZIP
    with zipfile.ZipFile(arquivoZip, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(arquivoCsv, os.path.basename(arquivoCsv))
    print(f"Arquivo CSV compactado em {arquivoZip}")
else:
    print("Arquivo PDF não encontrado! Verifique se o scraping foi concluído corretamente.")
