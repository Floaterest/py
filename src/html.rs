use std::{cmp::Reverse, collections::BinaryHeap, error::Error, fs, path::PathBuf};

use maud::{html, DOCTYPE};

use crate::Wrap;

fn is_image(path: &PathBuf) -> bool {
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

pub fn run(d: PathBuf, wrap: Wrap) -> Result<(), Box<dyn Error>> {
    // get images
    let mut images: Vec<_> = fs::read_dir(&d)?
        .flatten()
        .map(|e| e.path())
        .filter(is_image)
        .flat_map(|p| p.file_name().and_then(|p| p.to_str()).and_then(|p| Some(p.to_owned())))
        .collect();
    images.sort();

    fs::write(
        d.join("index.html"),
        html! {
            (DOCTYPE)
            head {
                meta charset="utf8";
                title { ("title") }
            }
            body {
                @for image in images.iter() {
                    img alt=(image) src=(image) {}
                }
            }
        }
        .into_string(),
    )?;
    Ok(())
}
