use std::{io::Result, path::PathBuf};

type PB = PathBuf;

/// apply f to files in each folder recursively, then flatten right associative
pub fn tree<T, F: Fn(&PB, &[PathBuf]) -> Result<T>>(path: &PB, f: &mut F) -> Result<Vec<T>> {
    let paths: Vec<_> = path.read_dir()?.flat_map(Result::ok).map(|entry| entry.path()).collect();
    let mut result = Vec::with_capacity(paths.len());
    let (files, paths): (Vec<_>, Vec<_>) = paths.into_iter().partition(|e| e.is_file());
    let files: Vec<_> = files
        .into_iter()
        .filter_map(|f| f.file_name().and_then(|f| f.to_str()).map(PathBuf::from))
        .collect();
    for path in paths.into_iter().filter(|path| path.is_dir()) {
        result.extend(tree(&path, f)?);
    }
    result.push(f(path, &files)?);
    Ok(result)
}

/// check if file is image (by extension)
pub fn is_image(path: &&PathBuf) -> bool {
    path.extension()
        .and_then(|ext| ext.to_str())
        .map(|ext| {
            matches!(ext.to_lowercase().as_str(), "png" | "jpg" | "jpeg" | "gif" | "avif" | "webp")
        })
        .unwrap_or(false)
}
