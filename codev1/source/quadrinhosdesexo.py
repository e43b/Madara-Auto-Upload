import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
import zipfile
import json

# Verificar se o argumento URL foi passado
if len(sys.argv) > 1:
    url = sys.argv[1]  # Pega o primeiro argumento passado (o link do mangá)
else:
    print("Nenhuma URL foi fornecida.")
    sys.exit(1)

# Extrai o domínio da URL
dominio = urlparse(url).netloc  # Extrai o domínio

# Função para limpar e formatar a sinopse
def clean_text(text):
    return ' '.join(text.split())  # Remove quebras de linha e espaços extras

# Faz a requisição HTTP
response = requests.get(url)

# Verifica se a requisição foi bem sucedida
if response.status_code == 200:
    # Parseia o HTML com BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extrai o título
    titulo = soup.find('h1').text if soup.find('h1') else ""
    print(f"Título: {titulo}")
    
    # Extrai a sinopse
    sinopse_elem = soup.find('div', class_='cn-texts')
    sinopse = sinopse_elem.find('p').text if sinopse_elem else ""
    sinopse = clean_text(sinopse)  # Aplica a limpeza da sinopse
    print(f"Sinopse: {sinopse}")
    
    # Extrai os links das páginas (imagens)
    imagens = soup.select('div#gallery-1 img')
    paginas = []
    
    for img in imagens:
        # Pega o link da imagem
        img_link = img.get('data-lazy-src') or img.get('src')
        
        # Verifica se o link pertence ao domínio do post
        if img_link and dominio in img_link and img_link not in paginas:  # Evita duplicatas
            paginas.append(img_link)

    # Baixa as imagens e renomeia
    for i, img_link in enumerate(paginas):
        if i < len(paginas):  # Limita ao número de imagens
            response = requests.get(img_link)
            img_name = f'{i + 1}.jpg'
            with open(img_name, 'wb') as f:
                f.write(response.content)
            print(f'Baixada: {img_name}')

    # Cria um arquivo ZIP
    with zipfile.ZipFile('oneshot.zip', 'w') as zipf:
        for i in range(len(paginas)):
            img_name = f'{i + 1}.jpg'
            zipf.write(img_name)

    # Baixa a imagem da capa novamente e renomeia para capa.jpg
    if paginas:
        response = requests.get(paginas[0])  # Primeira imagem é a capa
        with open('capa.jpg', 'wb') as f:
            f.write(response.content)
        print('Baixada: capa.jpg')

    # Remove as imagens baixadas
    for img in os.listdir('.'):
        if img.endswith('.jpg') and img != 'capa.jpg' and img != 'oneshot.zip':
            os.remove(img)

    # Cria o arquivo JSON com as informações
    info = {
        "originalLink": url,
        "title": titulo,
        "synopsis": sinopse,
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

    with open('info.json', 'w', encoding='utf-8') as json_file:
        json.dump(info, json_file, ensure_ascii=False, indent=4)

    print("Informações salvas em info.json.")

else:
    print(f"Erro ao acessar o site: {response.status_code}")
