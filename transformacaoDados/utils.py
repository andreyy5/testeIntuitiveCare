import os
import pandas as pd
import requests
import pdfplumber

def criarPasta(nomePasta):
    """Cria uma pasta caso ela não exista."""
    if not os.path.exists(nomePasta):
        os.makedirs(nomePasta)

def extrairDadosTabela(arquivoPdf):
    """Extrai a tabela do PDF e retorna os dados em formato de lista."""
    dados = []
    
    with pdfplumber.open(arquivoPdf) as pdf:
        for pagina in pdf.pages:
            tabelas = pagina.extract_tables()
            for tabela in tabelas:
                for linha in tabela:
                    if any(celula is not None and celula.strip() != "" for celula in linha):
                        dados.append(linha)

    if not dados:
        print("⚠️ Nenhum dado foi extraído do PDF!")
        return []

    # Normalizar os dados e substituir abreviações
    legendaSubstituicao = {"OD": "Odontologia", "AMB": "Ambulatorial"}

    for i, linha in enumerate(dados):
        dados[i] = [legendaSubstituicao.get(celula.strip().upper(), celula) if celula else "" for celula in linha]

    return dados

def salvarCsv(dados, arquivoCsv):
    """Salva os dados extraídos em um arquivo CSV."""
    if not dados:
        print("⚠️ Nenhum dado para salvar no CSV!")
        return
    
    df = pd.DataFrame(dados)
    df.to_csv(arquivoCsv, index=False, encoding="utf-8", sep=";")
    print(f"✅ Dados salvos em: {arquivoCsv}")
