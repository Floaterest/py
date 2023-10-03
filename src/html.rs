use crate::tree::tree;
use clap::ValueEnum;
use html::{metadata::Head, root::*};
use image::{imageops, GenericImageView, Rgba};
use std::{error::Error, fs, io::Result, path::PathBuf};

const STYLE: &str = include_str!("./style.css");
const WRAP: &str = include_str!("./wrap.css");

#[derive(ValueEnum, Debug, Clone, PartialEq, Copy)]
pub enum Wrap {
    /// no wrap
    #[clap(alias = "0")]
    None,
    /// wrap after odd pages
    #[clap(alias = "1")]
    Odd,
    /// wrap after even pages
    #[clap(alias = "2")]
    Even,
    #[clap(alias = "g")]
    /// guess between odd and even
    Guess,
}

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
fn basename(path: &PathBuf) -> String {
    // path.file_name().and_then(|p| p.to_str()).and_then(|p| Some(p))
    let s = path.file_name().unwrap();
    let s = s.to_str().unwrap();
    String::from(s)
}

fn guess(path: &[&PathBuf]) -> std::result::Result<Wrap, Box<dyn Error>> {
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
fn index(path: &PathBuf, entries: &[PathBuf], wrap: Wrap) -> Result<Vec<()>> {
    let empty = Vec::new();
    let mut images: Vec<_> = entries.iter().filter(is_image).collect();
    images.sort_by_key(|path| path.to_str());

    // don't write index.html if images
    println!("{} images in {}", images.len(), &path.to_str().unwrap_or(""));
    if images.len() == 0 {
        return Ok(empty);
    }

    let wrap = if wrap == Wrap::Guess { guess(&images[50..60]).unwrap() } else { wrap };
    let title = path.file_name();
    let title = title.and_then(|p| p.to_str()).unwrap_or("Title");

    let mut head = Head::builder();
    head.meta(|meta| meta.charset("utf8"));
    head.title(|t| t.text(String::from(title)));
    head.style(|style| style.text(minify(STYLE)));
    if matches!(wrap, Wrap::Odd | Wrap::Even) {
        head.style(|style| style.text(minify(WRAP)));
    }

    let mut body = Body::builder();
    // dummy image for odd wrapping
    if matches!(wrap, Wrap::Odd) {
        body.image(|img| img);
    }
    for src in images.iter() {
        let src = basename(&PathBuf::from(src));
        body.image(|img| img.alt(src.clone()).src(src));
    }

    let mut html = Html::builder();
    html.push(head.build());
    html.push(body.build());
    fs::write(path.join("index.html"), html.build().to_string())?;
    Ok(empty)
}

pub fn run(path: &PathBuf, wrap: Wrap) -> Result<()> {
    let _ = tree(path, &mut |path, files| index(path, files, wrap))?;
    Ok(())
}
