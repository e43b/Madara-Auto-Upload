import sys
import requests
from bs4 import BeautifulSoup
import os
import zipfile
import json

# Verificar se o argumento URL foi passado
if len(sys.argv) > 1:
    url = sys.argv[1]  # Pega o primeiro argumento passado (o link do mangá)
else:
    print("Nenhuma URL foi fornecida.")
    sys.exit(1)

# Função para baixar as imagens
def baixar_imagem(url, nome_arquivo):
    response = requests.get(url)
    if response.status_code == 200:
        with open(nome_arquivo, 'wb') as f:
            f.write(response.content)
        print(f"Imagem {nome_arquivo} baixada")
    else:
        print(f"Erro ao baixar a imagem: {url}")

# Fazendo o request na URL
response = requests.get(url)

# Verificando se a requisição foi bem-sucedida
if response.status_code == 200:
    # Parse do conteúdo HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extraindo o link da capa
    meta_image = soup.find('meta', {'property': 'og:image'})
    capa_link = meta_image['content'] if meta_image else ''

    # Baixar a imagem da capa com o nome "capa.jpg"
    if capa_link:
        baixar_imagem(capa_link, 'capa.jpg')

    # Extraindo o título principal
    titulo_element = soup.find('h1', class_='post-titulo')
    titulo = titulo_element.text.strip() if titulo_element else ''

    # Extraindo o título alternativo
    titulo_alternativo_element = soup.find('div', class_='tituloOriginal')
    titulo_alternativo = titulo_alternativo_element.text.strip() if titulo_alternativo_element else ''

    # Extraindo categorias (gêneros)
    categorias_element = soup.select('li strong:-soup-contains("Categorias:") ~ a')
    generos = [cat.text for cat in categorias_element] if categorias_element else []

    # Extraindo tags
    tags_element = soup.select('li strong:-soup-contains("Tags:") ~ a')
    tags = [tag.text for tag in tags_element] if tags_element else []

    # Extraindo autores
    autores_element = soup.select_one('li strong:-soup-contains("Autor:") ~ a')
    autores = [autores_element.text] if autores_element else []

    # Extraindo artistas
    artistas_element = soup.select_one('li strong:-soup-contains("Artista:") ~ a')
    artistas = [artistas_element.text] if artistas_element else []

    # Extraindo a sinopse
    sinopse_element = soup.find('div', class_='post-texto')
    sinopse = sinopse_element.text.strip().replace('Sinopse', '').strip() if sinopse_element else ''

    # Extraindo os links das imagens
    imagens_element = soup.select('ul.post-fotos img')
    links_imagens = [img['src'] for img in imagens_element] if imagens_element else []

    # Baixar as páginas e salvar no arquivo zip "oneshot.zip"
    if links_imagens:
        with zipfile.ZipFile('oneshot.zip', 'w') as zipf:
            for i, link in enumerate(links_imagens, start=1):
                nome_arquivo = f'{i}.jpg'
                baixar_imagem(link, nome_arquivo)
                zipf.write(nome_arquivo)
                os.remove(nome_arquivo)  # Excluir a imagem após adicioná-la ao zip
        print("Arquivo oneshot.zip criado com sucesso!")

    # Estrutura de dados a ser salva em JSON
    dados_json = {
        "originalLink": url,
        "title": titulo,
        "synopsis": sinopse,
        "cover": "capa.jpg",
        "pages": "oneshot.zip",
        "oneshotTitle": "oneshot",
        "type": "oneshot",
        "alternativeTitle": titulo_alternativo,
        "mangaStatus": "",  # Não especificado no HTML
        "releaseYear": "",  # Não especificado no HTML
        "authors": autores,
        "artists": artistas,
        "genres": generos,
        "tags": tags
    }

    # Salvando os dados em um arquivo JSON
    with open('info.json', 'w', encoding='utf-8') as f:
        json.dump(dados_json, f, ensure_ascii=False, indent=4)

    print("Dados salvos em info.json com sucesso!")

else:
    print(f"Erro ao acessar a página. Código de status: {response.status_code}")
