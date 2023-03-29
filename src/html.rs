use std::{error::Error, fs, path::PathBuf};

const STYLE: &str = include_str!("./style.css");
const WRAP: &str = include_str!("./wrap.css");
use maud::{html, DOCTYPE};

use crate::Wrap;

fn minify(css: &str) -> String {
    css.replace(|ch| matches!(ch, '\n' | '\t'), "")
}

fn is_image(path: &&PathBuf) -> bool {
    let ext = match path.extension() {
        Some(ext) => ext,
        None => return false,
    };
    let ext = match ext.to_str() {
        Some(ext) => ext,
        None => return false,
    };
    matches!(ext, "png" | "jpg" | "jpeg" | "gif" | "avif")
}

fn basename(path: &PathBuf) -> Option<&str> {
    path.file_name().and_then(|p| p.to_str()).and_then(|p| Some(p))
}

pub fn run(d: &PathBuf, wrap: &Wrap) -> Result<(), Box<dyn Error>> {
    // get images
    let paths: Vec<_> = fs::read_dir(&d)?.flatten().map(|e| e.path()).collect();
    let mut images: Vec<_> = paths.iter().filter(is_image).flat_map(basename).collect();
    images.sort();

    // run on nested directories
    for d in paths.iter().filter(|p| p.is_dir()) {
        run(d, wrap)?;
    }

    // don't write index.html if images
    println!("{} images in {}", images.len(), &d.to_str().unwrap_or(""));
    if images.len() == 0 {
        return Ok(());
    }

    Ok(fs::write(
        d.join("index.html"),
        html! {
            (DOCTYPE)
            head {
                meta charset="utf8";
                title { (d.file_name().and_then(|p|p.to_str()).unwrap_or("title")) }
                style { (minify(STYLE)) }
                @if matches!(wrap, Wrap::Odd | Wrap::Even) {
                    style { (minify(WRAP)) }
                }
            }
            body {
                // dummy image for odd wrapping
                @if wrap == &Wrap::Odd {
                    img {}
                }
                @for image in images.iter() {
                    img alt=(image) src=(image) {}
                }
            }
        }
        .into_string(),
    )?)
}
