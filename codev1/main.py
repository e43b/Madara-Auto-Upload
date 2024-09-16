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
def processar_manga(link):
    # Verifica se o domínio é "hiper.cool"
    if "hiper.cool" in link:
        print(f"\nProcessando link: {link}")

        # Executa o script de download, passando o link como argumento
        os.system(f"python3 source/hipercool.py {link}")  # Passa o link como argumento para o script

        print("Download concluído. Iniciando upload...")

        # Executa o script de upload
        os.system("python3 autov2.py")  # Executa o script de upload

        print(f"Upload de {link} concluído.")
    else:
        print(f"Domínio não suportado: {link}. Apenas 'hiper.cool' é aceito.")

# Função para gerenciar o processo de download e upload de múltiplos mangás
def gerenciar_mangas(links):
    for link in links:
        processar_manga(link)
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
