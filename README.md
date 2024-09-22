# Madara Massive Uploader

Este script automatiza a postagem de mangas e oneshots em sites WordPress que utilizam o tema Madara.

## Instruções para Uso

### Passo 1: Clonar o Repositório

Primeiro, clone o repositório necessário para este script:

```bash
git clone https://github.com/e43b/Madara-Auto-Upload
```

### Passo 2: Instalar Dependências

Entre na pasta `code` e instale as bibliotecas necessárias:

```bash
cd code
pip install -r requirements.txt
```

### Passo 3: Executar o Script

Execute o arquivo `main.py` para configurar o programa:

```bash
python main.py
```

### Passo 4: Configurar o Programa

No menu principal, você encontrará as seguintes opções para configuração:

- **Opção 3**: Insira o domínio do seu site e defina se os posts serão públicos ou privados.
- **Opção 4**: Configure suas credenciais de login (usuário e senha). Utilize uma conta com função de **Autor** para garantir permissões adequadas.

### Passo 5: Enviar Mangás

#### Opção 1: Upload Manual

Escolha a opção **1** no menu. Você será solicitado a inserir o(s) link(s) dos mangás. Após inserir os links, o script automaticamente fará o download e upload para o seu site, desde que o domínio esteja registrado no arquivo `sources.json` com uma extensão adequada para download.

Verifique o arquivo `sources.json` para visualizar os sites suportados ou acesse a lista de sites [aqui](#sites-suportados). Para adicionar suporte para novos sites, consulte o tutorial [de criação de extensões](#tutorial-de-criação-de-extensões).

#### Opção 2: Upload via Arquivo

A opção **2** permite que você envie mangás a partir de um arquivo `.txt` ou `.json` contendo os links. Os formatos de arquivo são:

##### Exemplo de Arquivo `.txt`:

```txt
http://site1.com/manga/123
http://site2.com/manga/456
http://site3.com/manga/789
```

##### Exemplo de Arquivo `.json`:

```json
{
    "links": [
        "http://site1.com/manga/123",
        "http://site2.com/manga/456",
        "http://site3.com/manga/789"
    ]
}
```

Basta criar o arquivo no mesmo diretório do script `main.py` e, ao selecionar a opção 2, inserir o nome do arquivo (por exemplo: `links.txt`). O script processará os links, baixará e postará automaticamente.

### Logs

Durante a execução, são gerados dois arquivos de log:

- **log.txt**
- **log.json**

Os logs armazenam informações como:

```json
[
    {
        "ID": 1,
        "Data da Execução": "2024-09-20 10:32:49",
        "Tempo de execução": "46.70 segundos",
        "Link original": "https://link.com/obra",
        "Capa": "https://site.com/wp-content/uploads/2024/09/capa.jpg",
        "Capitulo": "https://site.com/wp-content/uploads/2024/09/oneshot.zip",
        "Link da obra no site": "https://site.com/manga/obra/"
    }
]
```

### Sites Suportados

Atualmente, o script suporta download e upload automático de sites como:

- **hiper.cool**
- **brasilhentai.com**
- **hentaitokyo.net**
- **mundohentaioficial.com**
- **quadrinhosdesexo.com**
- **meuhentai.com**
- **superecchi.com**
- **nhentaibr.com**
- **mangashentais.com**

Verifique o arquivo `sources.json` para mais detalhes. Caso queira adicionar suporte para um novo site, siga as instruções no [tutorial de criação de extensões](#tutorial-de-criação-de-extensões).

### Tutorial de Criação de Extensões

Deseja adicionar suporte para novos sites? Acesse o tutorial completo [aqui](link para extensao.md).

## Contribuição

Sinta-se à vontade para contribuir com novas extensões ou melhorias no script. 

Para suporte direto e discussões sobre o projeto, entre no nosso [Discord](https://discord.gg/SQKcCAuBRr).

Se você gostou do projeto e gostaria de apoiar financeiramente, considere fazer uma doação:

- [Doe aqui](https://oxapay.com/donate/70144069)

Doadores podem solicitar a criação de extensões para outros sites e terão contato mais direto comigo.
