import sys
import os
import requests
import zipfile
import json
from bs4 import BeautifulSoup

# Verificar se o argumento URL foi passado
if len(sys.argv) > 1:
    url = sys.argv[1]  # Pega o primeiro argumento passado (o link do mangá)
else:
    print("Nenhuma URL foi fornecida. Use o comando: python hipercool.py <URL>")
    sys.exit(1)

# Exibindo uma mensagem quando o script inicia
print(f"Iniciando o download do mangá: {url}")

# Função para baixar uma imagem
def download_image(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)

# Fazendo a requisição para a URL fornecida
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extraindo informações do título e outras
titulo = soup.find('h1', class_='post-titulo').get_text(strip=True)
artistas = [a.get_text() for a in soup.select('ul.post-itens li strong:-soup-contains("Artista") ~ a')]
tags = [a.get_text() for a in soup.select('ul.post-itens li strong:-soup-contains("Tags") ~ a')]

# Obtendo URLs das imagens (mantendo o formato original .webp)
image_urls = [img['src'] for img in soup.select('ul.post-fotos img')]

# Criando uma lista para salvar os nomes das imagens (dentro do zip)
image_filenames = []

# Baixando e salvando a primeira imagem como 'capa.webp' (fora do zip)
if image_urls:
    download_image(image_urls[0], 'capa.webp')   # Salvar como capa

    # Também salvar como 'image_1.webp' dentro do zip
    download_image(image_urls[0], 'image_1.webp')  
    image_filenames.append('image_1.webp')  # Adicionar ao zip

# Baixando as outras imagens, sem duplicar a primeira
for i, image_url in enumerate(image_urls[1:], start=2):  # Começar com image_2.webp
    image_filename = f"image_{i}.webp"
    download_image(image_url, image_filename)
    image_filenames.append(image_filename)

# Criando o arquivo zip com todas as imagens (apenas as páginas, sem a capa)
with zipfile.ZipFile('oneshot.zip', 'w') as zipf:
    for image_filename in image_filenames:
        zipf.write(image_filename)
        os.remove(image_filename)  # Excluir a imagem após adicionar ao zip

# Gerando o arquivo info.json
info_data = {
    "originalLink": url,
    "title": titulo,
    "synopsis": "",
    "cover": "capa.webp",  # A capa está fora do zip
    "pages": "oneshot.zip",  # Apenas as imagens numeradas estão no zip
    "oneshotTitle": "Oneshot",
    "type": "oneshot",
    "alternativeTitle": "",
    "mangaStatus": "",
    "releaseYear": "",
    "authors": [],
    "artists": artistas,
    "genres": [],
    "tags": tags
}

if os.path.exists('info.json'):
    os.remove('info.json')

with open('info.json', 'w') as json_file:
    json.dump(info_data, json_file, indent=4)

# Exibindo uma mensagem ao final do processo
print("Processo concluído. Arquivos salvos: capa.webp, oneshot.zip, info.json.")
