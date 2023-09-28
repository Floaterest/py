use std::{fs::DirEntry, io::Result, path::PathBuf};

pub fn walk<T, I, F>(path: &PathBuf, f: &mut F) -> Result<I>
where
    I: Iterator<Item = T>,
    F: Fn(&PathBuf, &[PathBuf]) -> Result<I>,
{
    let entries: Vec<_> = path.read_dir()?.flatten().collect();
    let is_file = |entry: &&DirEntry| matches!(entry.file_type(), Ok(ty) if ty.is_file());
    let is_dir = |entry: &&DirEntry| matches!(entry.file_type(), Ok(ty) if ty.is_dir());
    for entry in entries.iter().filter(is_dir) {
        walk(&entry.path(), f)?;
    }
    f(path, &entries.iter().filter(is_file).map(|entry| entry.path()).collect::<Vec<_>>())
}
