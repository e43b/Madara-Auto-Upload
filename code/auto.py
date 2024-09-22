import json
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime

# Função para carregar o arquivo config.json
def load_config():
    with open('config.json', 'r', encoding='utf-8') as file:
        return json.load(file)

# Função para checar se o elemento existe a cada segundo, com um timeout máximo
def esperar_elemento(driver, by, value, timeout=10, polling_interval=1):
    start_time = time.time()
    while True:
        try:
            element = driver.find_element(by, value)
            return element  # Retorna o elemento se encontrado
        except NoSuchElementException:
            if time.time() - start_time > timeout:
                raise Exception(f"Elemento com {by}='{value}' não foi encontrado no tempo limite de {timeout} segundos")
            time.sleep(polling_interval)

# Função para carregar o arquivo info.json e preencher valores faltantes
def load_info_json():
    with open('info.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Verificar e preencher valores faltantes com strings vazias
    keys = ["title", "synopsis", "cover", "pages", "alternativeTitle", "mangaStatus", "releaseYear", "authors", "artists", "genres", "tags", "type", "oneshotTitle"]
    for key in keys:
        if key not in data or data[key] is None:
            data[key] = "" if isinstance(data[key], str) else []

    return data

# Função para salvar log no arquivo TXT e JSON
def salvar_log(id_sequencial, start_time, end_time, original_link, capa_url, paginas_url, post_link):
    log_txt = f"""
ID: {id_sequencial}
Data da Execução: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Tempo de execução: {end_time - start_time:.2f} segundos
Link original: {original_link}
Capa: {capa_url}
Capitulo: {paginas_url}
Link da obra no site: {post_link}
"""

    # Salvar no log.txt
    with open("log.txt", "a", encoding="utf-8") as file:
        file.write(log_txt)

    # Criar o conteúdo para o log.json
    log_json = {
        "ID": id_sequencial,
        "Data da Execução": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "Tempo de execução": f"{end_time - start_time:.2f} segundos",
        "Link original": original_link,
        "Capa": capa_url,
        "Capitulo": paginas_url,
        "Link da obra no site": post_link
    }

    # Verificar se o arquivo JSON já existe e carregar os logs antigos
    if os.path.exists("log.json"):
        with open("log.json", "r", encoding="utf-8") as file:
            logs = json.load(file)
    else:
        logs = []

    # Adicionar o novo log
    logs.append(log_json)

    # Salvar no log.json
    with open("log.json", "w", encoding="utf-8") as file:
        json.dump(logs, file, ensure_ascii=False, indent=4)

# Função para obter o próximo ID sequencial
def obter_proximo_id():
    if os.path.exists("log.txt"):
        with open("log.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

        # Filtrar e extrair os IDs
        ids = [int(line.replace("ID: ", "").strip()) for line in lines if line.startswith("ID:")]
        if ids:
            return max(ids) + 1
    return 1  # Se não houver ID, começar do 1

# Função para monitorar progresso de uploads
def monitorar_progresso(driver):
    try:
        while True:
            progress_elements = driver.find_elements(By.CSS_SELECTOR, ".progress .percent")
            all_completed = True
            for progress_element in progress_elements:
                percent_text = progress_element.text.strip('%')
                percent_value = int(percent_text)
                print(f"Progresso do upload: {percent_value}%")

                if percent_value < 100:
                    all_completed = False

            if all_completed:
                break

            time.sleep(1)
    except Exception as e:
        print(f"Erro ao monitorar progresso: {e}")

# Função para fazer upload e obter links dos arquivos
def upload_files_and_get_links(driver, info):
    config = load_config()
    driver.get(f"{config['website']}wp-admin/media-new.php")
    upload_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    upload_input.send_keys(f'{os.getcwd()}/{info["cover"]}\n{os.getcwd()}/{info["pages"]}')

    # Monitorar o progresso do upload
    monitorar_progresso(driver)

    # Copia o link dos arquivos enviados com espera explícita
    try:
        capa_link_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f"button[data-clipboard-text*='{info['cover'].split('.')[0]}']"))
        )
        paginas_link_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f"button[data-clipboard-text*='{info['pages'].split('.')[0]}']"))
        )

        capa_url = capa_link_button.get_attribute('data-clipboard-text')
        paginas_url = paginas_link_button.get_attribute('data-clipboard-text')

        # Exibe os links no console
        print(f"Link da capa: {capa_url}")
        print(f"Link do zip: {paginas_url}")

        return capa_url, paginas_url

    except Exception as e:
        print(f"Erro ao obter links dos arquivos enviados: {e}")
        return None, None

def fill_content(driver, content):
    driver.execute_script("document.querySelector('#content-html').click();")
    time.sleep(1)
    content_area = esperar_elemento(driver, By.ID, "content")
    content_area.clear()
    content_area.send_keys(content)
    time.sleep(1)

def fill_alternative_title(driver, alt_title):
    alt_title_input = esperar_elemento(driver, By.ID, "wp-manga-alternative")
    alt_title_input.clear()
    alt_title_input.send_keys(alt_title)

def select_manga_status(driver, status):
    status_select = esperar_elemento(driver, By.ID, "manga-status")
    for option in status_select.find_elements(By.TAG_NAME, "option"):
        if option.text.lower() == status.lower():
            option.click()
            break

def fill_release_year(driver, year):
    release_year_input = esperar_elemento(driver, By.ID, "new-tag-wp-manga-release")
    release_year_input.clear()
    release_year_input.send_keys(str(year))
    release_year_input.send_keys(Keys.ENTER)

def fill_authors(driver, authors):
    authors_input = esperar_elemento(driver, By.ID, "new-tag-wp-manga-author")
    authors_input.clear()
    authors_input.send_keys(", ".join(authors))
    authors_input.send_keys(Keys.ENTER)

def fill_artists(driver, artists):
    artists_input = esperar_elemento(driver, By.ID, "new-tag-wp-manga-artist")
    artists_input.clear()
    artists_input.send_keys(", ".join(artists))
    artists_input.send_keys(Keys.ENTER)

def fill_genres_and_tags(driver, genres, tags):
    tags_input = esperar_elemento(driver, By.ID, "new-tag-wp-manga-tag")
    tags_input.clear()
    tags_input.send_keys(", ".join(genres + tags))
    tags_input.send_keys(Keys.ENTER)

def remove_domain(url, domain):
    return url.replace(domain, "")

def upload_single_chapter(driver, info, paginas_url):
    config = load_config()
    upload_single_chapter_tab = esperar_elemento(driver, By.CSS_SELECTOR, 'a[href="#chapter-upload"]')
    driver.execute_script("arguments[0].click();", upload_single_chapter_tab)

    time.sleep(2)
    chapter_name_input = esperar_elemento(driver, By.ID, "wp-manga-chapter-name")
    chapter_name_input.send_keys(info['oneshotTitle'])

    upload_type_section = esperar_elemento(driver, By.CSS_SELECTOR, 'label[for="upload-zip"]')
    upload_type_section.click()

    time.sleep(2)
    chapter_link_input = esperar_elemento(driver, By.ID, "wp-manga-chapter-link")
    relative_url = remove_domain(paginas_url, config['website'])
    chapter_link_input.send_keys(relative_url)

    upload_button = esperar_elemento(driver, By.ID, "wp-manga-chapter-file-upload")
    upload_button.click()

def upload_manga(driver, paginas_url):
    config = load_config()
    upload_manga_tab = esperar_elemento(driver, By.CSS_SELECTOR, 'a[href="#manga-upload"]')
    driver.execute_script("arguments[0].click();", upload_manga_tab)

    time.sleep(2)
    direct_file_path_input = esperar_elemento(driver, By.ID, "wp-manga-file-path")
    relative_url = remove_domain(paginas_url, config['website'])
    direct_file_path_input.send_keys(relative_url)

    upload_button = esperar_elemento(driver, By.ID, "wp-manga-upload")
    upload_button.click()

# Função principal de upload e publicação
def upload_and_publish():
    start_time = time.time()  # Captura o tempo de início do script
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        info = load_info_json()
        config = load_config()

        with open('credentials.json', 'r') as f:
            credentials = json.load(f)

        driver.get(f"{config['website']}wp-login.php")
        username_input = esperar_elemento(driver, By.ID, 'user_login')
        username_input.send_keys(credentials['username'])
        password_input = esperar_elemento(driver, By.ID, 'user_pass')
        password_input.send_keys(credentials['password'])
        login_button = esperar_elemento(driver, By.ID, 'wp-submit')
        login_button.click()

        # Upload dos arquivos e obtenção dos links
        capa_url, paginas_url = upload_files_and_get_links(driver, info)
        if not capa_url or not paginas_url:
            return

        # Publicar o post
        driver.get(f"{config['website']}wp-admin/post-new.php?post_type=wp-manga")

        title_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "title")))
        title_input.send_keys(info['title'])

        fill_content(driver, info['synopsis'])

        # Selecionar a capa na biblioteca de mídia
        driver.find_element(By.ID, "set-post-thumbnail").click()
        time.sleep(3)
        media_library_button = driver.find_element(By.ID, "menu-item-browse")
        media_library_button.click()

        # Procurar por capa específica
        search_input = driver.find_element(By.ID, "media-search-input")
        search_input.send_keys(capa_url.split('/')[-1])
        search_input.send_keys(Keys.RETURN)

        # Verifica a cada 1 segundo até que o elemento da capa seja encontrado
        timeout = 10  # tempo máximo para aguardar, em segundos
        polling_interval = 1  # intervalo de checagem, em segundos
        start_time_capa = time.time()

        while True:
            try:
                # Tenta encontrar o primeiro elemento da capa
                first_capa = driver.find_element(By.CSS_SELECTOR, 'li.attachment')
                first_capa.click()
                break  # Se encontrar o elemento, sai do loop
            except NoSuchElementException:
                # Se o elemento não for encontrado, espera 1 segundo e tenta novamente
                if time.time() - start_time_capa > timeout:
                    raise Exception("Elemento 'first_capa' não foi encontrado no tempo limite")
                time.sleep(polling_interval)

        # Selecionar a imagem destacada
        set_featured_image_button = driver.find_element(By.CSS_SELECTOR, 'button.media-button-select')
        set_featured_image_button.click()
        time.sleep(3)

        postbox_container = esperar_elemento(driver, By.ID, "postbox-container-2")
        normal_sortables = esperar_elemento(postbox_container, By.ID, "normal-sortables")
        manga_information_metabox = esperar_elemento(normal_sortables, By.ID, "manga-information-metabox")
        inside_div = esperar_elemento(manga_information_metabox, By.CLASS_NAME, "inside")

        manga_type_choice = esperar_elemento(inside_div, By.CLASS_NAME, "manga-type-choice")
        manga_type_choice.find_element(By.ID, "wp-manga-type").click()

        fill_alternative_title(driver, info['alternativeTitle'])
        select_manga_status(driver, info['mangaStatus'])
        fill_release_year(driver, info['releaseYear'])
        fill_authors(driver, info['authors'])
        fill_artists(driver, info['artists'])
        fill_genres_and_tags(driver, info['genres'], info['tags'])

        if info['type'] == 'oneshot':
            upload_single_chapter(driver, info, paginas_url)
        else:
            upload_manga(driver, paginas_url)

        # Definir visibilidade conforme configuração
        driver.execute_script("document.querySelector('.edit-visibility').click();")
        time.sleep(1)
        visibility_option = config['visibility'].lower()
        if visibility_option == 'privado':
            driver.execute_script("document.getElementById('visibility-radio-private').click();")
        elif visibility_option == 'público':
            driver.execute_script("document.getElementById('visibility-radio-public').click();")
        elif visibility_option == 'protegido por senha':
            driver.execute_script("document.getElementById('visibility-radio-password').click();")
        driver.execute_script("document.querySelector('.save-post-visibility').click();")

        # Forçar o clique no botão de "Publicar" via JavaScript
        publish_button = driver.find_element(By.ID, "publish")
        driver.execute_script("arguments[0].click();", publish_button)

        # Esperar até que o post seja publicado
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "sample-permalink")))

        # Obter o link do post publicado
        edit_slug_box = driver.find_element(By.ID, "edit-slug-box")
        permalink = edit_slug_box.find_element(By.ID, "sample-permalink")
        post_link = permalink.find_element(By.TAG_NAME, "a").get_attribute("href")

        print(f"Post publicado com sucesso! Link: {post_link}")

        end_time = time.time()  # Captura o tempo de término
        total_time = end_time - start_time  # Calcula o tempo total de execução
        print(f"Tempo total de execução: {total_time:.2f} segundos")

        # Salvar os logs
        proximo_id = obter_proximo_id()
        salvar_log(proximo_id, start_time, end_time, info["originalLink"], capa_url, paginas_url, post_link)

    finally:
        driver.quit()
        
if __name__ == "__main__":
    upload_and_publish()
