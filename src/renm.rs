use crate::tree::tree;
use itertools::Itertools;
use std::{fs, fs::DirBuilder, io::Result, iter, path::PathBuf};

const PATH: &str = "/tmp/tree.txt";

/// read paths until no duplicates
fn input(path: &PathBuf) -> Result<Vec<String>> {
    let mut line = String::new();
    loop {
        std::io::stdin().read_line(&mut line)?;
        let content = fs::read_to_string(path)?;
        let content: Vec<_> = content.split("\n").map(String::from).collect();
        let mut dup = content.iter().filter(|s| !s.is_empty()).duplicates();
        if let Some(d) = dup.next() {
            println!("{} contains duplicates! Press enter to continue: ", path.to_str().unwrap());
            for line in iter::once(d).chain(dup) {
                println!("{line}");
            }
        } else {
            return Ok(content);
        }
    }
}

pub fn run(path: &PathBuf) -> Result<()> {
    // get paths and write to file
    let xs = tree(path, &mut |_, files| Ok(files.to_vec()))?;
    let xs: Vec<_> = xs.into_iter().flatten().sorted().collect();
    let t = xs.iter().flat_map(|p| p.strip_prefix(path).ok()).flat_map(|p| p.to_str()).join("\n");
    fs::write(PATH, t)?;
    println!("Tree written to {PATH}, press enter to continue: ");
    // read path from file
    let ys = input(&PathBuf::from(PATH))?;
    if ys.len() != xs.len() {
        panic!("Not same length!");
    }

    for (x, sy) in iter::zip(xs.iter(), ys.iter()) {
        if sy.is_empty() {
            println!("Remove {}", x.to_str().unwrap());
            fs::remove_file(x)?;
            continue;
        }
        let y = path.join(sy);
        let sx = x.strip_prefix(path).unwrap().to_str().unwrap();
        if x == &y {
            println!("Skip {sx}");
            continue;
        }
        if let Some(parent) = y.parent() {
            DirBuilder::new().recursive(true).create(parent)?;
        }
        fs::rename(x, &y)?;
        println!("{sx} -> {sy}");
    }

    // remove empty dir
    tree(path, &mut |dir, _| match dir.read_dir()?.next() {
        Some(_) => Ok(()),
        None => {
            println!("Remove {}", dir.to_str().unwrap());
            fs::remove_dir(dir)
        }
    })?;
    Ok(())
}
