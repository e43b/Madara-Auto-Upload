import sys
import requests
from bs4 import BeautifulSoup
import os
import json
import zipfile

# Verificar se o argumento URL foi passado
if len(sys.argv) > 1:
    url = sys.argv[1]  # Pega o primeiro argumento passado (o link do mangá)
else:
    print("Nenhuma URL foi fornecida.")
    sys.exit(1)

# Exibir mensagem de início
print(f"Iniciando o download do mangá: {url}")

# Função para baixar imagens e salvar no mesmo diretório que o script
def download_images(image_urls):
    image_files = []
    
    for idx, img_url in enumerate(image_urls):
        img_data = requests.get(img_url).content
        img_filename = f"page_{idx + 1}.jpg"  # Nome do arquivo de imagem
        with open(img_filename, 'wb') as img_file:
            img_file.write(img_data)
            image_files.append(img_filename)
    
    return image_files

# Função para baixar uma imagem específica (como a capa) e salvar como "capa.jpg"
def download_cover_image(cover_url):
    img_data = requests.get(cover_url).content
    cover_filename = "capa.jpg"
    with open(cover_filename, 'wb') as img_file:
        img_file.write(img_data)
    return cover_filename

# Função para criar um arquivo zip com as imagens
def create_zip(image_files, zip_name):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for file in image_files:
            zipf.write(file, os.path.basename(file))

# Função para excluir as imagens após criar o ZIP
def delete_images(image_files):
    for file in image_files:
        if os.path.exists(file):
            os.remove(file)

# Fazendo a requisição HTTP para obter o HTML da página
response = requests.get(url)

# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    # Cria o objeto BeautifulSoup para análise do HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 1. Extrair o título e remover a parte após o primeiro "-"
    title_tag = soup.find('title').text
    title = title_tag.split('-')[0].strip()  # Remove o que vem depois do primeiro "-" e remove espaços
    
    # 2. Extrair a sinopse da meta tag "description"
    description_tag = soup.find('meta', attrs={'name': 'description'})
    sinopse = description_tag['content'] if description_tag else 'Sinopse não encontrada.'
    
    # 3. Extrair URLs das imagens da div com id "fotos"
    images_div = soup.find('div', id='fotos')
    if images_div:
        img_tags = images_div.find_all('img')
        image_urls = [img['src'] for img in img_tags]  # Pega o atributo 'src' de cada imagem
    else:
        image_urls = []

    # Baixando as imagens diretamente no diretório do script
    image_files = download_images(image_urls)
    
    # Nome do arquivo ZIP
    zip_name = "oneshot.zip"
    
    # Criando o arquivo ZIP com as imagens baixadas
    create_zip(image_files, zip_name)

    # Excluindo as imagens originais após a criação do ZIP
    delete_images(image_files)
    
    # Baixando a primeira imagem novamente e renomeando para capa.jpg
    cover_image_url = image_urls[0] if image_urls else ""
    cover_filename = download_cover_image(cover_image_url)

    # 4. Salvar as informações em um arquivo JSON
    info_data = {
        "originalLink": url,
        "title": title,
        "synopsis": sinopse,
        "cover": cover_filename,  # Arquivo da capa salvo como "capa.jpg"
        "pages": zip_name,
        "oneshotTitle": "Oneshot",
        "type": "oneshot",
        "alternativeTitle": "",
        "mangaStatus": "",
        "releaseYear": "",
        "authors": [],
        "artists": [],
        "genres": [],
        "tags": []
    }

    # Salvando o JSON no arquivo info.json
    with open('info.json', 'w', encoding='utf-8') as json_file:
        json.dump(info_data, json_file, ensure_ascii=False, indent=4)
    
    print("Dados salvos em info.json, capa salva como capa.jpg e imagens compactadas em oneshot.zip.")
else:
    print(f"Erro ao acessar o site: {response.status_code}")
