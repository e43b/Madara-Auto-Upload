import json
import time
import os

# Função para carregar e exibir configurações
def carregar_configuracao():
    with open("config.json", "r") as f:
        config = json.load(f)
    print("\nConfigurações atuais:")
    print(f"Website: {config['website']}")
    print(f"Visibilidade: {config['visibility']}")
    return config

# Função para carregar e exibir credenciais
def carregar_credenciais():
    with open("credentials.json", "r") as f:
        creds = json.load(f)
    print("\nCredenciais atuais:")
    print(f"Usuário: {creds['username']}")
    return creds

# Função para carregar e exibir os scripts associados aos domínios
def carregar_sources():
    with open("sources.json", "r") as f:
        sources = json.load(f)
    return sources

# Função para alterar configuração
def configurar_programa():
    config = carregar_configuracao()
    website = input(f"Digite o novo website (atual: {config['website']}): ") or config['website']
    visibility = input(f"Digite a visibilidade (público/privado) (atual: {config['visibility']}): ") or config['visibility']
    
    if visibility not in ["público", "privado"]:
        print("Visibilidade inválida. Deve ser 'público' ou 'privado'.")
        return
    
    config['website'] = website
    config['visibility'] = visibility
    
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)
    print("Configuração atualizada com sucesso!")

# Função para alterar credenciais
def configurar_credenciais():
    creds = carregar_credenciais()
    username = input(f"Digite o novo usuário (atual: {creds['username']}): ") or creds['username']
    password = input(f"Digite a nova senha (atual: {creds['password']}): ") or creds['password']
    
    creds['username'] = username
    creds['password'] = password
    
    with open("credentials.json", "w") as f:
        json.dump(creds, f, indent=4)
    print("Credenciais atualizadas com sucesso!")

# Função para checar o domínio do link e processar o mangá
def processar_manga(link, sources):
    # Extrai o domínio do link
    dominio = link.split('/')[2]
    
    # Verifica se o domínio existe no arquivo sources.json
    if dominio in sources:
        script = sources[dominio]
        print(f"\nProcessando link: {link} com o script {script}")

        # Executa o script de download, passando o link como argumento
        os.system(f"python3 {script} {link}")

        print("Download concluído. Iniciando upload...")

        # Executa o script de upload
        os.system("python3 auto.py")

        print(f"Upload de {link} concluído.")
    else:
        print(f"Domínio não suportado: {dominio}. Adicione-o ao sources.json para processá-lo.")

# Função para gerenciar o processo de download e upload de múltiplos mangás
def gerenciar_mangas(links):
    sources = carregar_sources()
    for link in links:
        processar_manga(link, sources)
        time.sleep(2)  # Pequena espera antes de processar o próximo link (caso haja mais)

# Função para ler links de um arquivo .txt
def ler_links_txt(filepath):
    with open(filepath, 'r') as file:
        links = [line.strip() for line in file.readlines()]
    return links

# Função para ler links de um arquivo .json
def ler_links_json(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
        # Assumindo que o arquivo JSON tem um formato {"links": ["link1", "link2", ...]}
        return data.get("links", [])

# Nova função para gerenciar o upload a partir de arquivos
def gerenciar_mangas_de_arquivo(filepath):
    if filepath.endswith('.txt'):
        links = ler_links_txt(filepath)
    elif filepath.endswith('.json'):
        links = ler_links_json(filepath)
    else:
        print("Formato de arquivo não suportado. Use .txt ou .json.")
        return
    
    gerenciar_mangas(links)

# Menu principal
def menu():
    while True:
        print("\nMadara Massive Uploader")
        print("1. Upar mangá (links inseridos manualmente)")
        print("2. Upar mangá de arquivo (.txt ou .json)")
        print("3. Configurar programa")
        print("4. Configurar credenciais")
        print("5. Sair")
        
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            links = input("Digite os links dos mangás, separados por vírgula: ").split(',')
            gerenciar_mangas([link.strip() for link in links])
        elif escolha == "2":
            filepath = input("Digite o caminho do arquivo (.txt ou .json): ")
            gerenciar_mangas_de_arquivo(filepath)
        elif escolha == "3":
            configurar_programa()
        elif escolha == "4":
            configurar_credenciais()
        elif escolha == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
