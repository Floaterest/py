# html.py <!-- omit in toc -->
> Create a single html file as an image/manga viewer.


<!-- omit in toc -->
# Table of Contents 
- [Usage](#usage)
    - [Positional Arguments](#positional-arguments)
    - [Optional Arguments](#optional-arguments)
- [More Details](#more-details)
    - [File Searching](#file-searching)
        - [Recursive](#recursive)
        - [Definition of Image File](#definition-of-image-file)
    - [Display Modes](#display-modes)
        - [Tab](#tab)
    - [Wrap Options](#wrap-options)
        - [`0`: Wrap After Each Page](#0-wrap-after-each-page)
        - [`1`: Wrap After Odd Pages](#1-wrap-after-odd-pages)
        - [`2`: Wrap After Even Pages](#2-wrap-after-even-pages)


# Usage
`html.py [-h] path [mode] [wrap]`

## Positional Arguments
[Back to top](#table-of-contents)
- `path`: directory path, more details: [#file-searching](#file-searching)
    - if `path` contains spaces, quote it with double quote (`"/path to/destination folder/"`)
- `mode`: display mode, more details: [#display-modes](#display-modes)
    - current available modes are [tab](#tab)
    - by default, the script will use the 1st display mode
- `wrap`: wrap option, more details: [#wrap-options](#wrap-options)
    - `0` to wrap after each page
    - `1` to wrap after page with odd page numbers (1-indexed)
    - `2` to wrap after page with even page numbers (1-indexed)

## Optional Arguments
[Back to top](#table-of-contents)
- `-h`, `--help`: display a help page


# More Details

## File Searching
[Back to top](#table-of-contents)
### Recursive
- the script will look for `path` and its subfolders that contain images (using `os.walk()`)
### Definition of Image File
- if a file's extension is in `.png`, `.jpg`, and `.gif`, then the file is considered an image and will be included in the final HTML output
    - in the source code ([common.py](../src/utils/common.py)), it is defined in the `EXTENSIONS` constant and the `is_image(fn: str) -> bool` function

## Display Modes
[Back to top](#table-of-contents)
### Tab
- features
    - click on an image to toggle table of contents(toc) on the right
    - in toc, automatically hightlight the current reading chapter (determined based on which chapter was clicked)
    - in toc, click on a chapter to toggle the visibility of that chapter
    - in toc, the `invert` button will switch the visibility of all chapter (programmatically defined as click on all the chapters once)
- styles and scripts (defined in `MODES` from [writer.py](../src/utils/writer.py))
    - [t2b.css](../src/utils/t2b.css)
    - [tab.css](../src/utils/tab.css)
    - [tab.js](../src/utils/tab.js)
    - [wrap0.css](../src/utils/wrap0.css) or [wrap.css](../src/utils/wrap.css) depending on the wrap option (see [Positional Arguments](#positional-arguments))

## Wrap Options
[Back to top](#table-of-contents)
### `0`: Wrap After Each Page 
<details><summary>The final result will look like this:</summary>

```
1
2
3
4
5
6
7
8
9
```

</details>

### `1`: Wrap After Odd Pages
<details><summary>The final result will look like this:</summary>

```
1 
32
54
76
98
```
or
```
1
32
54
76
8
```
</details>
- the pages are right to left because that is just how manga works
- the alignment is done using <code>&lt;table&gt;</code>

### `2`: Wrap After Even Pages
<details><summary>The final result will look like this:</summary>

```
21
43
65
87
9
```
or
```
21
43
65
87
```

</details>
- the pages are right to left because that is just how manga works
- the alignment is done using <code>&lt;table&gt;</code>
