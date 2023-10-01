use crate::tree::tree;
use itertools::Itertools;
use std::fs::{read_dir, read_to_string, rename, write};
use std::fs::{remove_dir, DirBuilder};
use std::io::Result;
use std::path::{Path, PathBuf};

const PATH: &str = "/tmp/tree.txt";

pub fn run(path: &PathBuf) -> Result<()> {
    let bs = tree(path, &mut |_, files| Ok(files.to_vec()))?;
    let bs: Vec<_> = bs.iter().flatten().flat_map(|p| p.strip_prefix(path).ok()).sorted().collect();
    write(PATH, bs.iter().flat_map(|b| b.to_str()).join("\n"))?;
    println!("Press enter to continue: ");
    let mut line = String::new();
    std::io::stdin().read_line(&mut line)?;
    let mut dest = read_to_string(PATH)?;
    let mut cs: Vec<_> = dest.split("\n").collect();
    loop {
        let mut dup = cs.iter().duplicates();
        if let Some(d) = dup.next() {
            println!("{PATH} contains duplicates!");
            println!("{d}");
            for line in dup {
                println!("{line}");
            }
            std::io::stdin().read_line(&mut line)?;
            dest = read_to_string(PATH)?;
            cs = dest.split("\n").collect();
            continue;
        }
        break;
    }
    for (bp, c) in bs.iter().zip(cs.iter()) {
        let b = bp.to_str().unwrap();
        if &b == c {
            println!("Skip {b}");
            continue;
        }
        let (bc, cc) = (Path::join(path, b), Path::join(path, c));
        if let Some(parent) = cc.parent() {
            DirBuilder::new().recursive(true).create(parent)?;
        }
        rename(bc, cc)?;
        println!("{b} -> {c}");
    }
    for d in bs.iter().map(|b| b.parent()).dedup() {
        if read_dir(d)?.next().is_none() {
            remove_dir(d)?;
            println!("Remove {}", d.to_str().unwrap());
        }
    }
    Ok(())
}
