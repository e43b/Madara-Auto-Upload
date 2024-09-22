import requests
from bs4 import BeautifulSoup
import os
import json
import zipfile
import sys

# Função para baixar imagens
def download_image(url, path):
    img_data = requests.get(url).content
    with open(path, 'wb') as handler:
        handler.write(img_data)

# Função para processar e extrair a sinopse
def extract_synopsis(content, title):
    # Encontrar o primeiro parágrafo dentro da div
    paragraph = content.find('p')
    if paragraph:
        # Obter o texto do parágrafo
        text = paragraph.get_text()
        # Verificar se o texto contém o título
        if title in text:
            # Encontrar o índice após "– "
            start_index = text.find("– ") + 2
            if start_index > 1:  # Verificar se encontrou o "– "
                return text[start_index:].strip()
    # Retornar uma string vazia se não encontrar a sinopse válida
    return ""

# Verificar se o argumento URL foi passado
if len(sys.argv) > 1:
    url = sys.argv[1]  # Pega o primeiro argumento passado (o link do mangá)
else:
    print("Nenhuma URL foi fornecida.")
    sys.exit(1)

# Cabeçalhos para a requisição
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# Enviando uma requisição para o site
response = requests.get(url, headers=headers)

# Verificando se a requisição foi bem-sucedida
if response.status_code == 200:
    # Parsing do conteúdo HTML da página
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontrar o título da página
    title = soup.find('h1', class_='entry-title').text.strip()
    print(f"Título: {title}")

    # Encontrar a div com a classe "entry-content"
    entry_content = soup.find('div', class_='entry-content')

    # Inicializar a sinopse como uma string vazia
    synopsis = ""

    # Verificar se a div foi encontrada
    if entry_content:
        # Extrair a sinopse
        synopsis = extract_synopsis(entry_content, title)
        print(f"Sinopse: {synopsis}")

    # Criar arquivo info.json com os dados solicitados
    info_data = {
        "originalLink": url,
        "title": title,
        "synopsis": synopsis,
        "cover": "capa.jpg",
        "pages": "oneshot.zip",
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
    with open('info.json', 'w', encoding='utf-8') as info_file:
        json.dump(info_data, info_file, ensure_ascii=False, indent=4)
    print("Arquivo info.json criado com sucesso!")

    # Encontrar todas as tags <img> dentro da div
    images = entry_content.find_all('img') if entry_content else []

    # Verificar se existe pelo menos uma imagem
    if images:
        # A primeira imagem dentro da div é a capa
        cover_img_url = images[0].get('src')
        print(f"Link da Capa: {cover_img_url}")

        # Baixar a capa
        download_image(cover_img_url, 'capa.jpg')
        print("Capa salva como capa.jpg!")

        # Baixar as outras imagens (páginas)
        page_files = []
        for i, img in enumerate(images[1:], start=1):
            img_url = img.get('src')

            # Verificar se o link da imagem é válido
            if img_url and img_url.startswith('http'):
                page_filename = f'pagina_{i}.jpg'
                download_image(img_url, page_filename)
                page_files.append(page_filename)
                print(f"Página {i} salva como {page_filename}!")

        # Criar um arquivo zip para as páginas
        with zipfile.ZipFile('oneshot.zip', 'w') as zipf:
            for page_file in page_files:
                zipf.write(page_file)
                os.remove(page_file)  # Excluir a página após adicioná-la ao ZIP
        print("Páginas salvas em onshot.zip e arquivos individuais excluídos!")

else:
    print(f"Erro ao acessar a página. Status code: {response.status_code}")
