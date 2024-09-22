# Madara Massive Uploader

This script automates the posting of mangas and oneshots on WordPress sites using the **Madara** theme.

> **Theme version used in this project**: [Madara Version 1.8.0.1 - 2024.07.30](https://mangabooth.com/product/wp-manga-theme-madara/).

## Usage Instructions

### Step 1: Clone the Repository

First, clone the repository required for this script:

```bash
git clone https://github.com/e43b/Madara-Auto-Upload
```

### Step 2: Install Dependencies

Navigate to the `code` folder and install the required libraries:

```bash
cd code
pip install -r requirements.txt
```

### Step 3: Run the Script

Run the `main.py` file to configure the program:

```bash
python main.py
```

### Step 4: Configure the Program

In the main menu, you will find the following options for configuration:

- **Opção 3**: Enter your site's domain and define whether the posts will be public or private.
- **Opção 4**: Set up your login credentials (username and password). Use an account with **Author** role to ensure proper permissions.

### Step 5: Upload Mangas

#### Opção 1: Manual Upload

Select **Opção 1** in the menu. You will be asked to enter the manga link(s). After inserting the links, the script will automatically download and upload to your site, provided that the domain is registered in the `sources.json` file with an appropriate extension for downloading.

Check the `sources.json` file to view the supported sites or access the list of sites [here](#sites-suportados). To add support for new sites, see the [extension creation tutorial](#tutorial-de-criação-de-extensões).

#### Opção 2: Upload via File

The **Opção 2** allows you to upload mangas from a `.txt` or `.json` file containing the links. The file formats are as follows:

##### Example of a `.txt` File:

```txt
http://site1.com/manga/123
http://site2.com/manga/456
http://site3.com/manga/789
```

##### Example of a `.json` File:

```json
{
    "links": [
        "http://site1.com/manga/123",
        "http://site2.com/manga/456",
        "http://site3.com/manga/789"
    ]
}
```

Simply create the file in the same directory as the `main.py` script and, when selecting Opção 2, input the file name (e.g., `links.txt`). The script will process the links, download, and post automatically.

### Logs

During execution, two log files are generated:

- **log.txt**
- **log.json**

The logs store information such as:

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

### Supported Sites

Currently, the script supports automatic download and upload from sites such as:

- **hiper.cool**
- **brasilhentai.com**
- **hentaitokyo.net**
- **mundohentaioficial.com**
- **quadrinhosdesexo.com**
- **meuhentai.com**
- **superecchi.com**
- **nhentaibr.com**
- **mangashentais.com**

Check the `sources.json` file for more details. If you want to add support for a new site, follow the instructions in the [extension creation tutorial](#tutorial-de-criação-de-extensões).

### Extension Creation Tutorial

Do you want to add support for new sites? Access the full tutorial [here](extensao.md).

## Contribution

Feel free to contribute new extensions or improvements to the script.

For direct support and project discussions, join our [Discord](https://discord.gg/SQKcCAuBRr).

If you like the project and would like to support it financially, consider making a donation:

- [Donate here](https://oxapay.com/donate/70144069)

Donors can request the creation of extensions for other sites and will have more direct contact with me.
