use image;
use regex::Regex;
use std::{error::Error, fs, io::Result, path::PathBuf};

use crate::comm::tree;

/// split landscape image into left and right halves
fn split(path: &PathBuf) -> std::result::Result<(), Box<dyn Error>> {
    let (w, h) = image::image_dimensions(path)?;
    if w < h {
        // not landscape
        return Ok(());
    }
    let base = path.file_stem().unwrap().to_str().unwrap();
    let parent = path.parent().unwrap();
    let ext = path.extension().unwrap();
    let re = Regex::new(r"(.*)(\d{3}[a-z]*)-(\d{3}[a-z]*).*")?;
    let (a, b) = if let Some(caps) = re.captures(base) {
        let base = &caps[1];
        let a = &caps[2];
        let b = &caps[3];
        ([base, a].concat(), [base, b].concat())
    } else {
        ([base, "a"].concat(), [base, "b"].concat())
    };
    let (mut a, mut b) = (PathBuf::from(a), PathBuf::from(b));
    a.set_extension(ext);
    b.set_extension(ext);
    println!("{} -> {} {}", path.to_str().unwrap(), a.to_str().unwrap(), b.to_str().unwrap());
    let (a, b) = (parent.join(a), parent.join(b));
    let i = image::open(path)?;
    i.crop_imm(0, 0, w / 2, h).save(b)?;
    i.crop_imm(w / 2, 0, w, h).save(a)?;

    fs::remove_file(path)?;
    Ok(())
}

pub fn run(path: &PathBuf) -> Result<()> {
    let _ = tree(path, &mut |_, files| Ok(files.iter().flat_map(split).collect::<Vec<_>>()))?;
    Ok(())
}
