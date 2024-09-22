# Tutorial de Criação de Extensão para Madara Massive Uploader

Este guia ensina como criar uma extensão para automatizar o download e upload de mangás ou oneshots em sites que utilizam o tema Madara (versão 1.8.0.1 - 2024.07.30).

### Estrutura Básica da Extensão

Para que o script funcione corretamente com um novo site, é necessário criar dois elementos:

1. Um **script Python** que fará a extração das informações da obra.
2. Um arquivo **`info.json`** que conterá os dados extraídos.

---

## 1. Criando o Arquivo `info.json`

O arquivo `info.json` deve seguir a estrutura abaixo. Mesmo que o site não tenha todas as categorias de informações (como autores, gêneros, etc.), **os campos devem ser preenchidos com `""` (vazio)**, mas sempre mantidos no JSON. 

> **Importante**: Caso a obra seja uma **oneshot**, o campo **`oneshotTitle`** deve obrigatoriamente estar preenchido, mesmo que seja com o valor `"Oneshot"`.

### Estrutura do `info.json`:

```json
{
    "originalLink": "",
    "title": "",
    "synopsis": "",
    "cover": "",
    "pages": "",
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
```

### Explicação dos Campos:

- **originalLink**: URL original da obra.
- **title**: Título principal da obra.
- **synopsis**: Sinopse da obra.
- **cover**: Caminho do arquivo da capa, que será baixada com o nome `capa.jpg`.
- **pages**: Caminho do arquivo zip com as páginas. Se for oneshot, nomeie como `oneshot.zip`; se for um mangá, use `manga.zip`.
- **oneshotTitle**: Se for uma oneshot, este campo deve conter `"Oneshot"` ou o título do capítulo. **Deve ser preenchido**.
- **type**: Tipo da obra. Use `"oneshot"` para histórias curtas e `"manga"` para séries com múltiplos capítulos.
- **alternativeTitle**: Títulos alternativos (se houver).
- **mangaStatus**: Status do mangá (em andamento, completo, etc.).
- **releaseYear**: Ano de lançamento.
- **authors**: Lista de autores.
- **artists**: Lista de artistas.
- **genres**: Lista de gêneros.
- **tags**: Lista de tags.

---

## 2. Criando o Script Python para Extração

Seu script Python será responsável por extrair as informações do mangá ou oneshot e preenchê-las no arquivo `info.json`. Além disso, será encarregado de baixar as imagens e criar os arquivos necessários (capa e zip das páginas).

### Passos para o Script:

1. **Extraia as informações da obra**: Utilize as bibliotecas adequadas para fazer scraping do site e obter as informações da obra (título, sinopse, autores, etc.).
   
2. **Baixe a capa**: A capa deve ser baixada diretamente no diretório dos scripts, com o nome **`capa.jpg`**.

3. **Baixe as páginas**: As páginas devem ser baixadas diretamente no mesmo diretório e, após isso, compactadas em um arquivo zip.

   - Para **oneshots**, crie um arquivo **`oneshot.zip`** contendo todas as páginas.
   - Para **mangás com múltiplos capítulos**, crie um arquivo **`manga.zip`** onde cada capítulo será uma pasta dentro do zip (por exemplo, `Chapter 1/`, `Chapter 2/`, etc.).

4. **Exclua as páginas baixadas**: Após zipar, exclua as imagens baixadas para manter o diretório limpo.

5. **Preencha o `info.json`**: Crie o arquivo `info.json` e preencha os campos com as informações extraídas, incluindo o caminho para a capa e o arquivo zip das páginas.

### Exemplo de Estrutura do Diretório:

- `capa.jpg` → Arquivo da capa.
- `oneshot.zip` → Arquivo zip contendo as páginas (se for oneshot).
- `manga.zip` → Arquivo zip contendo os capítulos em pastas (se for mangá).
- `info.json` → Arquivo JSON contendo as informações da obra.

### Regras Importantes:

- **Nome da capa**: Sempre nomeie a capa como **`capa.jpg`** e insira o nome no campo `"cover"` do JSON.
- **Nome do arquivo zip**: 
  - Para oneshots, nomeie como **`oneshot.zip`** e insira o nome no campo `"pages"` do JSON.
  - Para mangás, siga a estrutura de capítulos (pasta por capítulo dentro do zip) e nomeie o arquivo como **`manga.zip`**.
  
> **Nota**: Caso o site não forneça alguma informação, como autores, artistas, ou tags, basta deixar esses campos vazios (`""` ou `[]`), mas nunca excluí-los.

---

## 3. Considerações Especiais

- **Título da Oneshot**: Se a oneshot não tiver um título definido, use `"Oneshot"` como título padrão.
  
- **Type (Tipo da Obra)**: 
  - `"oneshot"`: Para obras curtas com um único capítulo.
  - `"manga"`: Para séries com múltiplos capítulos. Lembre-se de zipar os capítulos corretamente.

## Finalizando

Com esses passos, você poderá criar uma extensão para qualquer site que deseja utilizar com o Madara Massive Uploader. Certifique-se de que seu script extraia corretamente as informações e siga as regras de nomeação para que o processo de download e upload funcione sem erros.

Para mais informações ou contribuições, entre no [Discord do projeto](https://discord.gg/SQKcCAuBRr) ou confira o repositório original.
