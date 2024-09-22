# Extension Creation Tutorial for Madara Massive Uploader

This guide explains how to create an extension to automate the download and upload of mangas or oneshots on sites using the Madara theme (version 1.8.0.1 - 2024.07.30).

### Basic Structure of the Extension

For the script to work correctly with a new site, two components are required:

1. A **Python script** that will extract the manga's information.
2. A **`info.json`** file containing the extracted data.

---

## 1. Creating the `info.json` File

The `info.json` file should follow the structure below. Even if the site does not provide all categories of information (like authors, genres, etc.), **the fields must be filled with `""` (empty)** but must always remain in the JSON.

> **Important**: If the work is a **oneshot**, the field **`oneshotTitle`** must be filled in, even if the value is just `"Oneshot"`.

### Structure of `info.json`:

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

### Explanation of Fields:

- **originalLink**: Original URL of the work.
- **title**: Main title of the work.
- **synopsis**: Synopsis of the work.
- **cover**: Path to the cover file, which will be downloaded with the name `capa.jpg`.
- **pages**: Path to the zip file containing the pages. For oneshots, name it `oneshot.zip`; for a manga, use `manga.zip`.
- **oneshotTitle**: If it is a oneshot, this field should contain `"Oneshot"` or the chapter title. **Must be filled**.
- **type**: Type of the work. Use `"oneshot"` for short stories and `"manga"` for series with multiple chapters.
- **alternativeTitle**: Alternative titles (if any).
- **mangaStatus**: Status of the manga (ongoing, completed, etc.).
- **releaseYear**: Release year.
- **authors**: List of authors.
- **artists**: List of artists.
- **genres**: List of genres.
- **tags**: List of tags.

---

## 2. Creating the Python Script for Extraction

Your Python script will be responsible for extracting the manga or oneshot information and filling it in the `info.json` file. Additionally, it will handle downloading images and creating the required files (cover and zipped pages).

### Steps for the Script:

1. **Extract the work's information**: Use appropriate libraries to scrape the site and get the work's information (title, synopsis, authors, etc.).
   
2. **Download the cover**: The cover should be downloaded directly into the script directory with the name **`capa.jpg`**.

3. **Download the pages**: The pages should be downloaded directly into the same directory, and then zipped.

   - For **oneshots**, create a **`oneshot.zip`** file containing all pages.
   - For **mangas with multiple chapters**, create a **`manga.zip`** file where each chapter is a folder inside the zip (e.g., `Chapter 1/`, `Chapter 2/`, etc.).

4. **Delete the downloaded pages**: After zipping, delete the downloaded images to keep the directory clean.

5. **Fill in the `info.json`**: Create the `info.json` file and fill the fields with the extracted information, including the path to the cover and the zip file with the pages.

### Example of Directory Structure:

- `capa.jpg` → Cover file.
- `oneshot.zip` → Zip file containing the pages (if it's a oneshot).
- `manga.zip` → Zip file containing chapters in folders (if it's a manga).
- `info.json` → JSON file containing the work's information.

### Important Rules:

- **Cover name**: Always name the cover **`capa.jpg`** and insert the name in the `"cover"` field of the JSON.
- **Zip file name**: 
  - For oneshots, name it **`oneshot.zip`** and insert the name in the `"pages"` field of the JSON.
  - For mangas, follow the chapter structure (a folder per chapter inside the zip) and name the file **`manga.zip`**.
  
> **Note**: If the site does not provide some information, such as authors, artists, or tags, just leave these fields empty (`""` or `[]`), but never remove them.

---

## 3. Special Considerations

- **Oneshot Title**: If the oneshot does not have a defined title, use `"Oneshot"` as the default title.
  
- **Type of Work (Type)**: 
  - `"oneshot"`: For short works with a single chapter.
  - `"manga"`: For series with multiple chapters. Remember to zip the chapters correctly.

## Finalizing

By following these steps, you will be able to create an extension for any site you want to use with the Madara Massive Uploader. Make sure your script extracts the information correctly and follows the naming rules to ensure the download and upload process works smoothly.

For more information or contributions, join the [project's Discord](https://discord.gg/SQKcCAuBRr) or check out the original repository.
