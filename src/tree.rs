use std::{io::Result, iter::once, path::PathBuf};

type PB = PathBuf;

/// apply f to files in each folder recursively, then flatten right associative
pub fn tree<T, F: Fn(&PB, &[PB]) -> Result<T>>(path: &PB, f: &mut F) -> Result<Vec<T>> {
    let entries: Vec<_> = path.read_dir()?.flat_map(Result::ok).map(|entry| entry.path()).collect();
    let files: Vec<_> = entries.clone().into_iter().filter(|path| path.is_file()).collect();
    let once = once(f(path, &files)?);
    let result: Vec<_> = entries
        .into_iter()
        .filter(|path| path.is_dir())
        .flat_map(|path| tree(&path, f).ok())
        .flatten()
        .chain(once)
        .collect();
    Ok(result)
}
