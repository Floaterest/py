use crate::comm::{is_image, tree};
use children::BodyChild;
use clap::ValueEnum;
use html::{
    content::Section,
    metadata::Head,
    root::*,
    text_content::{Division, Paragraph},
};
use image::{GenericImageView, Rgba, imageops};
use include_dir::{Dir, include_dir};
use itertools::Itertools;
use std::{collections::VecDeque, error::Error, fs, io::Result, path::PathBuf};

static ASSETS: Dir<'_> = include_dir!("$CARGO_MANIFEST_DIR/assets");

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
    /// no wrap, group by chapters
    #[clap(alias = "c")]
    Chapter,
}

/// guess the wrapping
fn guess(path: &[String]) -> std::result::Result<Wrap, Box<dyn Error>> {
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

/// even wrapping
fn even(images: Vec<String>) -> VecDeque<BodyChild> {
    images
        .into_iter()
        .tuple_windows()
        .map(|(r, l)| Paragraph::builder().image(|img| img.src(r)).image(|img| img.src(l)).build())
        .map(|e| e.into())
        .collect()
}

/// odd wrapping
fn odd(images: Vec<String>) -> VecDeque<BodyChild> {
    let p = Paragraph::builder().image(|img| img.src(images[0].clone())).build();
    let mut v = even(images.into_iter().skip(1).collect());
    v.push_front(p.into());
    v
}

/// no wrap, group by chapter
fn chapter(images: Vec<String>) -> VecDeque<BodyChild> {
    let pred = |p1: &String| {
        let p = PathBuf::from(p1);
        let s = p.file_stem()?.to_str()?.to_string();
        Some(s[..s.len() - 4].to_string())
    };
    let mut v = VecDeque::new();
    for (k, imgs) in &images.into_iter().chunk_by(|p| pred(p).unwrap_or(String::new())) {
        let mut s = Section::builder();
        s.id(k);
        for img in imgs {
            s.image(|i| i.src(img));
        }
        v.push_back(s.build().into());
    }
    v
}

/// write index.html if image exists recursively
fn index(path: &PathBuf, entries: &[PathBuf], wrap: Wrap) -> Result<Vec<()>> {
    let empty = Vec::new();
    let images: Vec<_> = entries
        .iter()
        .filter(is_image)
        .filter_map(|i| i.to_str())
        .map(String::from)
        .sorted()
        .collect();

    // don't write index.html if images
    println!("{} images in {}", images.len(), &path.to_str().unwrap_or(""));
    if images.len() == 0 {
        return Ok(empty);
    }

    let wrap = if wrap == Wrap::Guess { guess(&images[50..60]).unwrap() } else { wrap };
    let title = path.file_name();
    let title = title.and_then(|p| p.to_str()).unwrap_or("Title");
    let style = ASSETS
        .get_file(match wrap {
            Wrap::Odd | Wrap::Even | Wrap::Guess => "wrap.css",
            Wrap::None => "zero.css",
            Wrap::Chapter => "chapter.css",
        })
        .unwrap()
        .contents_utf8()
        .unwrap()
        .to_owned();
    let style = style + ASSETS.get_file("style.css").unwrap().contents_utf8().unwrap();

    let head = Head::builder()
        .meta(|meta| meta.charset("utf8"))
        .title(|t| t.text(String::from(title)))
        .style(|s| s.text(style))
        .build();

    let body = Body::builder()
        .extend(match wrap {
            Wrap::None => images
                .into_iter()
                .map(|i| Division::builder().image(|img| img.src(i)).build())
                .map(|e| e.into())
                .collect(),
            Wrap::Even => even(images),
            Wrap::Odd => odd(images),
            Wrap::Chapter => chapter(images),
            Wrap::Guess => unreachable!(),
        })
        .script(|script| {
            if wrap == Wrap::Chapter {
                script.text(ASSETS.get_file("chapter.js").unwrap().contents_utf8().unwrap())
            } else {
                script
            }
        })
        .build();

    let mut html = Html::builder();
    html.push(head);
    html.push(body);
    let s = format!("{:?}", html.build());
    fs::write(path.join("index.html"), s)?;
    Ok(empty)
}

pub fn run(path: &PathBuf, wrap: Wrap) -> Result<()> {
    let _ = tree(path, &mut |path, files| index(path, files, wrap))?;
    Ok(())
}
