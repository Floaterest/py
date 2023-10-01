use crate::tree::tree;
use itertools::Itertools;
use std::fs::DirBuilder;
use std::io::Result;
use std::path::{Path, PathBuf};
use std::{fs, iter};

const PATH: &str = "/tmp/tree.txt";

fn input(path: &PathBuf) -> Result<Vec<PathBuf>> {
    let mut line = String::new();
    loop {
        std::io::stdin().read_line(&mut line)?;
        let content = fs::read_to_string(path)?;
        let content: Vec<_> = content.split("\n").map(PathBuf::from).collect();
        let mut dup = content.iter().duplicates();
        if let Some(d) = dup.next() {
            println!("{} contains duplicates! Press enter to continue: ", path.to_str().unwrap());
            for line in iter::once(d).chain(dup) {
                println!("{}", line.to_str().unwrap());
            }
        } else {
            return Ok(content);
        }
    }
}

pub fn run(path: &PathBuf) -> Result<()> {
    let xs = tree(path, &mut |_, files| Ok(files.to_vec()))?;
    let xs: Vec<_> = xs.into_iter().flatten().sorted().collect();
    let t = xs.iter().flat_map(|p| p.strip_prefix(path).ok()).flat_map(|p| p.to_str()).join("\n");
    fs::write(PATH, t)?;
    println!("Tree written to {PATH}, press enter to continue: ");
    let ys = input(&PathBuf::from(PATH))?;
    let ys: Vec<_> = ys.iter().map(|p| Path::join(path, p)).collect();
    for (x, y) in iter::zip(xs.iter(), ys.iter()) {
        let (sx, sy) = (x.strip_prefix(path).unwrap(), y.strip_prefix(path).unwrap());
        let (sx, sy) = (sx.to_str().unwrap(), sy.to_str().unwrap());
        if x == y {
            println!("Skip {sx}");
            continue;
        }
        if let Some(parent) = y.parent() {
            DirBuilder::new().recursive(true).create(parent)?;
        }
        fs::rename(x, y)?;
        println!("{sx} -> {sy}");
    }
    Ok(())
}
