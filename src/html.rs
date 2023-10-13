use std::{error::Error, fs, path::PathBuf};

use image::{imageops, GenericImageView, Rgba};

const STYLE: &str = include_str!("./style.css");
const WRAP: &str = include_str!("./wrap.css");
use maud::{html, DOCTYPE};

use crate::Wrap;

/// minify css
fn minify(css: &str) -> String {
    css.replace(|ch| matches!(ch, '\n' | '\t'), "")
}

/// check if path is image (by extension)
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

/// get basename of path
fn basename<'a>(path: &'a &'a PathBuf) -> Option<&'a str> {
    path.file_name().and_then(|p| p.to_str()).and_then(|p| Some(p))
}

fn guess(path: &[&PathBuf]) -> Result<Wrap, Box<dyn Error>> {
    let (mut ol, mut or, mut el, mut er) = (0, 0, 0, 0);
    for (i, p) in path.iter().enumerate() {
        let img = image::open(p)?;
        let (w, h) = img.dimensions();
        let left = imageops::crop_imm(&img, 0, 0, 1, h);
        let right = imageops::crop_imm(&img, w - 1, 0, 1, h);
        let (l, r) = if i % 2 == 0 { (&mut el, &mut er) } else { (&mut ol, &mut or) };
        if left.pixels().all(|(_, _, Rgba(c))| c.iter().all(|&n| n > 200)) {
            println!("{:?} has left white", &p);
            *r += 1;
        }
        if right.pixels().all(|(_, _, Rgba(c))| c.iter().all(|&n| n > 200)) {
            println!("{:?} has right white", &p);
            *l += 1;
        }
    }
    if or > ol && el > er {
        Ok(Wrap::Odd)
    } else if ol > or && er > el {
        Ok(Wrap::Even)
    } else {
        dbg!(ol, or, el, er);
        Err("can't guess wrap".into())
    }
}

/// write index.html if image exists recursively
pub fn run(d: &PathBuf, wrap: Wrap) -> Result<(), Box<dyn Error>> {
    // get images
    let paths: Vec<_> = fs::read_dir(&d)?.flatten().map(|e| e.path()).collect();
    let mut images: Vec<_> = paths.iter().filter(is_image).collect();
    images.sort_by_key(|p| p.to_str());

    // run on nested directories
    for d in paths.iter().filter(|p| p.is_dir()) {
        run(d, wrap.clone())?;
    }

    // don't write index.html if images
    println!("{} images in {}", images.len(), &d.to_str().unwrap_or(""));
    if images.len() == 0 {
        return Ok(());
    }

    let wrap = if wrap == Wrap::Guess { guess(&images[50..60])? } else { wrap };

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
                @if wrap == Wrap::Odd {
                    img {}
                }
                @for image in images.iter().flat_map(basename) {
                    img alt=(image) src=(image) {}
                }
            }
        }
        .into_string(),
    )?)
}
