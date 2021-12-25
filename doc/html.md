# html.py <!-- omit in toc -->
> Create a single html file as an image/manga viewer.

<!-- omit in toc -->
# Table of Contents 

- [Usage](#usage)

# Usage
`html.py [-h] path [mode] [wrap]`
- positional arguments
    - `path`: directory path
        - the script will search for folders that contain images **recursively**
        - if `path` contains spaces, quote it with double quote (`"/path to/destination folder/"`)
    - `mode`: display mode
        - current available modes are tab
        - by default, the script will use the 1st display mode
    - `wrap`: wrap option
        - `0` for wrap at each page
        - `1` for wrap after page with odd page numbers (1-indexed)
        - `2` for wrap after page with even page numbers (1-indexed)
- optional arguments
    - `-h`, `--help`: display a help page