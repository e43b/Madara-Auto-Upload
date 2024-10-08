import os
import sys
import requests
from bs4 import BeautifulSoup
import json
import re
from PIL import Image
import shutil
import zipfile

# Verificar se o argumento URL foi passado
if len(sys.argv) > 1:
    url = sys.argv[1]  # Pega o primeiro argumento passado (o link do mangá)
else:
    print("Nenhuma URL foi fornecida.")
    sys.exit(1)

# Função para lidar com caracteres especiais no nome
def sanitize_title(title):
    return re.sub(r'[\\/*?:"<>|]', "", title)

# Função para converter imagens WebP para JPG
def converter_para_jpg(image_path):
    with Image.open(image_path) as img:
        if img.format == "WEBP":
            jpg_path = image_path.replace(".webp", ".jpg")
            img.convert("RGB").save(jpg_path, "JPEG")
            os.remove(image_path)  # Exclui a imagem original em WebP
            return jpg_path
    return image_path

# Função para salvar a capa no diretório atual
def salvar_capa(cover_url, diretorio_atual):
    extension = cover_url.split('.')[-1]
    image_name = f"capa.{extension}"
    image_path = os.path.join(diretorio_atual, image_name)
    
    response = requests.get(cover_url)
    with open(image_path, 'wb') as file:
        file.write(response.content)
    
    # Converter para JPG se for WebP
    image_path = converter_para_jpg(image_path)
    
    return image_name  # Retorna o nome do arquivo

# Função para salvar informações da obra em um JSON no diretório atual
def salvar_info_json(data, diretorio_atual, filename="info.json"):
    json_path = os.path.join(diretorio_atual, filename)
    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Função para extrair e salvar as imagens dos capítulos ou oneshot
def extrair_e_salvar_imagens(url, diretorio_atual, tipo_obra):
    capítulo, links_paginas = extrair_links_paginas(url)
    
    # Se for manga, cria uma pasta por capítulo
    if tipo_obra == 'manga':
        pasta_destino = os.path.join(diretorio_atual, f"Chapter {capítulo}")
        os.makedirs(pasta_destino, exist_ok=True)

        # Salvando as imagens dentro da pasta do capítulo
        for i, link in enumerate(links_paginas, 1):
            extension = link.split('.')[-1]
            image_name = f"{i}.{extension}"
            image_path = os.path.join(pasta_destino, image_name)
            
            response = requests.get(link)
            with open(image_path, 'wb') as file:
                file.write(response.content)
            
            # Converter para JPG se for WebP
            converter_para_jpg(image_path)

        # Retorna o caminho da pasta do capítulo
        return pasta_destino

    # Se for oneshot, baixa as imagens diretamente no diretório atual
    elif tipo_obra == 'oneshot':
        imagens_oneshot = []
        for i, link in enumerate(links_paginas, 1):
            extension = link.split('.')[-1]
            image_name = f"{i}.{extension}"
            image_path = os.path.join(diretorio_atual, image_name)
            imagens_oneshot.append(image_path)
            
            response = requests.get(link)
            with open(image_path, 'wb') as file:
                file.write(response.content)
            
            # Converter para JPG se for WebP
            converter_para_jpg(image_path)

        # Retorna a lista de imagens baixadas para o oneshot
        return imagens_oneshot

# Função para criar um arquivo ZIP de uma pasta ou imagens
def zipar_pasta(diretorio_atual, pasta_para_zipar=None, files=None, excluir_original=False):
    if pasta_para_zipar:
        zip_filename = os.path.join(diretorio_atual, f"{os.path.basename(pasta_para_zipar)}.zip")
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(pasta_para_zipar):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), diretorio_atual))
        if excluir_original:
            shutil.rmtree(pasta_para_zipar)
    elif files:
        zip_filename = os.path.join(diretorio_atual, "oneshot.zip")
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in files:
                zipf.write(file, os.path.basename(file))

        if excluir_original:
            for file in files:
                os.remove(file)

    return zip_filename

# Função para criar um arquivo ZIP com pastas de capítulos
def zipar_capitulos(diretorio_atual, pastas_capitulos, excluir_original=False):
    zip_filename = os.path.join(diretorio_atual, "manga.zip")
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for pasta_capitulo in pastas_capitulos:
            for root, dirs, files in os.walk(pasta_capitulo):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), diretorio_atual))
    
    if excluir_original:
        for pasta_capitulo in pastas_capitulos:
            shutil.rmtree(pasta_capitulo)

    return zip_filename

# Função para extrair informações do link do capítulo ou volume
def extrair_links_paginas(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Verificar o padrão do URL e formatar o número do capítulo ou volume
    if 'capitulo-' in url:
        capítulo_match = re.search(r'capitulo-(\d+)', url)
        if capítulo_match:
            número_capítulo = int(capítulo_match.group(1))  # Converte para int para remover zero à esquerda
            capítulo_formatado = número_capítulo
        else:
            capítulo_formatado = "Capítulo não encontrado"
    elif 'vol-' in url or 'oneshot' in url:
        capítulo_formatado = 1  # Se for oneshot, considera como capítulo único
    else:
        capítulo_formatado = "Formato não reconhecido"

    # Extrair links das páginas
    imagens = soup.find_all('div', class_='page-break no-gaps')
    links_paginas = [img.find('img')['src'] for img in imagens]
    
    return capítulo_formatado, links_paginas

# Fazendo o request para a página
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extraindo o título e removendo " - Hipercool", além de sanitizar para criar a pasta
title = sanitize_title(soup.find('meta', property="og:title")['content'].replace(" - Hipercool", ""))

# Diretório atual onde o script está sendo executado
diretorio_atual = os.getcwd()

# Extraindo a capa (pegando tudo antes de "?")
cover = soup.find('meta', property="og:image")['content'].split('?')[0]

# Extraindo o autor
authors = [author.get_text(strip=True) for author in soup.find_all('div', class_='author-content')] if soup.find('div', 'author-content') else []

# Extraindo o artista
artists = [artist.get_text(strip=True) for artist in soup.find_all('div', class_='artist-content')] if soup.find('div', 'artist-content') else []

# Extraindo o gênero
genres = [g.strip() for g in soup.find('div', class_='genres-content').get_text(strip=True).split(",")] if soup.find('div', 'genres-content') else []

# Extraindo as tags
tags = [tag.get_text(strip=True) for tag in soup.select('div.tags-content a')] if soup.find('div', class_='tags-content') else []

# Extraindo o título alternativo
alt_title = soup.find('div', class_='summary-heading', string="Alternative")
alt_title = alt_title.find_next_sibling('div').get_text(strip=True) if alt_title else ""

# Extraindo a sinopse
summary_heading = soup.find('h5', string='Summary')
sinopse = str(summary_heading.find_next('div').find('p')) if summary_heading else ""

# Extraindo o status do manga
manga_status = soup.find('div', class_='status-content').get_text(strip=True) if soup.find('div', class_='status-content') else ""

# Extraindo o ano de lançamento
release_year = ""  # Esse campo pode precisar de um método diferente dependendo do site

# Extraindo os links dos capítulos
chapter_links = []
for chapter in soup.select('ul.main.version-chap.no-volumn li a'):
    link = chapter['href']
    if link not in chapter_links:
        chapter_links.append(link)

# Definindo se é um manga ou oneshot
tipo_obra = "manga" if len(chapter_links) > 1 else "oneshot"

# Salvando as informações iniciais em um JSON
info_data_initial = {
    "originalLink": url,
    "title": title,
    "synopsis": "",
    "cover": "",
    "pages": "",
    "oneshotTitle": "Oneshot" if tipo_obra == 'oneshot' else "",
    "type": tipo_obra,
    "alternativeTitle": "",
    "mangaStatus": "",
    "releaseYear": release_year,
    "authors": [],
    "artists": [],
    "genres": [],
    "tags": []
}
salvar_info_json(info_data_initial, diretorio_atual)

# Salvando a capa e atualizando o JSON
capa_name = salvar_capa(cover, diretorio_atual)

# Baixando e organizando as imagens dos capítulos ou oneshot
zip_path = None
if tipo_obra == 'manga':
    pastas_capitulos = []
    for chapter_url in chapter_links:
        pasta_capitulo = extrair_e_salvar_imagens(chapter_url, diretorio_atual, tipo_obra)
        pastas_capitulos.append(pasta_capitulo)
    
    # Criar um único ZIP com todas as pastas de capítulos
    zip_path = zipar_capitulos(diretorio_atual, pastas_capitulos, excluir_original=True)
else:
    # One-shot: baixa as imagens diretamente no diretório e zipa
    imagens_oneshot = extrair_e_salvar_imagens(chapter_links[0], diretorio_atual, tipo_obra)
    zip_path = zipar_pasta(diretorio_atual, files=imagens_oneshot, excluir_original=True)

# Atualizando o JSON com o nome da capa e o caminho do ZIP
info_data_final = {
    "originalLink": url,
    "title": title,
    "synopsis": sinopse,
    "cover": capa_name,
    "pages": os.path.basename(zip_path),
    "oneshotTitle": "Oneshot" if tipo_obra == 'oneshot' else "",
    "type": tipo_obra,
    "alternativeTitle": alt_title,
    "mangaStatus": manga_status,
    "releaseYear": release_year,
    "authors": authors,
    "artists": artists,
    "genres": genres,
    "tags": tags
}

# Salvando as informações finais em um JSON
salvar_info_json(info_data_final, diretorio_atual)
