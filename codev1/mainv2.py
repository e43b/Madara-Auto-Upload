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
        os.system("python3 autov2.py")

        print(f"Upload de {link} concluído.")
    else:
        print(f"Domínio não suportado: {dominio}. Adicione-o ao sources.json para processá-lo.")

# Função para gerenciar o processo de download e upload de múltiplos mangás
def gerenciar_mangas(links):
    sources = carregar_sources()
    for link in links:
        processar_manga(link, sources)
        time.sleep(2)  # Pequena espera antes de processar o próximo link (caso haja mais)

# Menu principal
def menu():
    while True:
        print("\nMadara Massive Uploader")
        print("1. Upar manga")
        print("2. Configurar programa")
        print("3. Configurar credenciais")
        print("4. Sair")
        
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            links = input("Digite os links dos mangás, separados por vírgula: ").split(',')
            gerenciar_mangas([link.strip() for link in links])
        elif escolha == "2":
            configurar_programa()
        elif escolha == "3":
            configurar_credenciais()
        elif escolha == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
