import sys
import requests
import os
import zipfile
import json
from bs4 import BeautifulSoup

# Função para extrair informações da página do livro
def extract_book_info(book_url):
    response = requests.get(book_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extraindo título
    title = soup.find('h2').text.strip()

    # Extraindo artista
    artist = soup.find('div', class_='artist-list').find('a').text.strip()

    # Extraindo tags
    tags_element = soup.find('td', class_='relatedtags').find_all('a')
    tags = [tag.text.strip() for tag in tags_element]

    # Estrutura para o arquivo JSON
    info = {
        "originalLink": book_url,
        "title": title,
        "synopsis": "",
        "cover": "capa.jpg",
        "pages": "oneshot.zip",
        "oneshotTitle": "Oneshot",
        "type": "oneshot",
        "alternativeTitle": "",
        "mangaStatus": "",
        "releaseYear": "",
        "authors": [],
        "artists": [artist],
        "genres": [],
        "tags": tags
    }

    return info

# Função para substituir "livro" por "leitor" e extrair as imagens
def extract_images_from_reader(book_url):
    # Substituindo "livro" por "leitor" no URL
    reader_url = book_url.replace("livro", "leitor")

    response = requests.get(reader_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extraindo as imagens
    image_elements = soup.find('div', id='gerar_pdf').find_all('img')
    image_urls = [img['src'] for img in image_elements]

    # Baixar e salvar as imagens
    for idx, img_url in enumerate(image_urls):
        img_name = f"page_{idx + 1}.jpg"
        img_data = requests.get(img_url).content
        with open(img_name, 'wb') as img_file:
            img_file.write(img_data)
        print(f"Baixado: {img_name}")

    return len(image_urls)  # Retorna o número total de imagens

# Função para criar um arquivo ZIP e renomear a primeira imagem
def create_zip_and_cleanup(total_pages):
    # Remover arquivos existentes
    if os.path.exists('oneshot.zip'):
        os.remove('oneshot.zip')
        print("Arquivo oneshot.zip removido.")

    # Criar arquivo ZIP
    with zipfile.ZipFile('oneshot.zip', 'w') as zipf:
        for idx in range(1, total_pages + 1):
            img_name = f"page_{idx}.jpg"
            zipf.write(img_name)

    # Remover arquivos anteriores caso já existam
    if os.path.exists('capa.jpg'):
        os.remove('capa.jpg')
        print("Arquivo capa.jpg removido.")

    # Renomear a primeira imagem para 'capa.jpg'
    os.rename("page_1.jpg", "capa.jpg")
    print("Renomeado page_1.jpg para capa.jpg")

    # Excluir todas as outras imagens exceto a capa
    for idx in range(2, total_pages + 1):
        img_name = f"page_{idx}.jpg"
        os.remove(img_name)

# Função para criar o arquivo JSON
def save_info_json(info):
    # Remover arquivo info.json se existir
    if os.path.exists('info.json'):
        os.remove('info.json')
        print("Arquivo info.json removido.")

    # Salvar as informações em um arquivo JSON
    with open("info.json", "w", encoding='utf-8') as json_file:
        json.dump(info, json_file, ensure_ascii=False, indent=4)
    print("info.json criado com sucesso")

# Função principal
def main():
    # Verificar se o argumento URL foi passado
    if len(sys.argv) > 1:
        url = sys.argv[1]  # Pega o primeiro argumento passado (o link do mangá)
    else:
        print("Nenhuma URL foi fornecida.")
        sys.exit(1)

    # Exibir a URL fornecida
    print(f"Iniciando o download do mangá: {url}")

    # Extrair informações do livro
    book_info = extract_book_info(url)

    # Extrair imagens do leitor
    total_pages = extract_images_from_reader(url)

    # Criar arquivo ZIP e renomear a primeira imagem
    create_zip_and_cleanup(total_pages)

    # Salvar informações em um arquivo JSON
    save_info_json(book_info)

if __name__ == "__main__":
    main()
