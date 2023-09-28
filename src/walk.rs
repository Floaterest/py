use std::{fs::DirEntry, path::PathBuf, io::Result};

pub fn walk<T, F: Fn(&PathBuf, &[PathBuf]) -> Result<T>>(path: &PathBuf, f: &mut F) -> Result<T> {
    let entries: Vec<_> = path.read_dir()?.flatten().collect();
    let is_file = |entry: &&DirEntry| matches!(entry.file_type(), Ok(ty) if ty.is_file());
    let is_dir = |entry: &&DirEntry| matches!(entry.file_type(), Ok(ty) if ty.is_dir());
    for entry in entries.iter().filter(is_dir) {
        walk(&entry.path(), f)?;
    }
    f(path, &entries.iter().filter(is_file).map(|entry| entry.path()).collect::<Vec<_>>())
}
