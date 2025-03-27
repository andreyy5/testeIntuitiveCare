import os
import zipfile
from utils import criarPasta, baixarArquivo, extrairLinks


URL = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

pastaDownloads = os.path.join(BASE_DIR, "downloads")
pastaOutput = os.path.join(BASE_DIR, "arquivoZip")
arquivoZip = os.path.join(pastaOutput, "anexos.zip")

criarPasta(pastaDownloads)
criarPasta(pastaOutput)

linksPdfs = extrairLinks(URL)

linksFiltrados = [link for link in linksPdfs if "Anexo_I" in link or "Anexo_II" in link]

if not linksFiltrados:
    print("Nenhum anexo encontrado para download.")
else:
    print(f"Encontrados {len(linksFiltrados)} arquivos para download.")

arquivosBaixados = []
for i, link in enumerate(linksFiltrados):
    nomeArquivo = f"Anexo_{i+1}.pdf"
    caminhoArquivo = os.path.join(pastaDownloads, nomeArquivo)
    baixarArquivo(link, caminhoArquivo)
    arquivosBaixados.append(caminhoArquivo)


with zipfile.ZipFile(arquivoZip, "w", zipfile.ZIP_DEFLATED) as zipf:
    for arquivo in arquivosBaixados:
        zipf.write(arquivo, os.path.basename(arquivo))

print(f"Arquivos compactados em {arquivoZip}")
