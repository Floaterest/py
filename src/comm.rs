use std::{io::Result, path::PathBuf};

type PB = PathBuf;

/// apply f to files in each folder recursively, then flatten right associative
pub fn tree<T, F: Fn(&PB, &[PB]) -> Result<T>>(path: &PB, f: &mut F) -> Result<Vec<T>> {
    let entries: Vec<_> = path.read_dir()?.flat_map(Result::ok).map(|entry| entry.path()).collect();
    let files: Vec<_> = entries.clone().into_iter().filter(|path| path.is_file()).collect();
    let mut result = Vec::with_capacity(entries.len());
    for path in entries.into_iter().filter(|path| path.is_dir()) {
        result.extend(tree(&path, f)?);
    }
    result.push(f(path, &files)?);
    Ok(result)
}

/// check if path is image (by extension)
pub fn is_image(path: &&PB) -> bool {
    let ext = match path.extension() {
        Some(ext) => ext,
        None => return false,
    };
    let ext = match ext.to_str() {
        Some(ext) => ext,
        None => return false,
    };
    matches!(ext.to_lowercase().as_str(), "png" | "jpg" | "jpeg" | "gif" | "avif" | "webp")
}
