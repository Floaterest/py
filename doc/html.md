# html.py <!-- omit in toc -->
> Create a single html file as an image/manga viewer.

<!-- omit in toc -->
# Table of Contents 

- [Usage](#usage)
    - [Positional Arguments](#positional-arguments)
    - [Optional Arguments](#optional-arguments)
- [More Details](#more-details)
    - [Definition of Image File](#definition-of-image-file)

# Usage
`html.py [-h] path [mode] [wrap]`
## Positional Arguments
- `path`: directory path
    - the script will search for folders that contain images **recursively**
    - if `path` contains spaces, quote it with double quote (`"/path to/destination folder/"`)
- `mode`: display mode
    - current available modes are tab
    - by default, the script will use the 1st display mode
- `wrap`: wrap option
    - `0` to wrap after each page
    - `1` to wrap after page with odd page numbers (1-indexed)
    - `2` to wrap after page with even page numbers (1-indexed)
## Optional Arguments
- `-h`, `--help`: display a help page

# More Details
## Definition of Image File
- if a file's extension is in `.png`, `.jpg`, and `.gif`, then the file is considered an image and will be included in the final HTML output
    - in the [source code](../src/html.py), it is defined in the `EXTENSIONS` constant and the `is_image(fn: str) -> bool` function