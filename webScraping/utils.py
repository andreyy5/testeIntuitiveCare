import os
import requests
from bs4 import BeautifulSoup

def criarPasta(nomePasta):
    if not os.path.exists(nomePasta):
        os.makedirs(nomePasta)

def baixarArquivo(url, destino):
    resposta = requests.get(url, stream=True)
    if resposta.status_code == 200:
        with open(destino, "wb") as arquivo:
            for chunk in resposta.iter_content(1024):
                arquivo.write(chunk)
        print(f"Download concluído: {destino}")
    else:
        print(f"Erro ao baixar {url}")

def extrairLinks(url):
    resposta = requests.get(url)
    if resposta.status_code == 200:
        soup = BeautifulSoup(resposta.text, "html.parser")
        return [a["href"] for a in soup.find_all("a", href=True) if a["href"].endswith(".pdf")]
    return []
