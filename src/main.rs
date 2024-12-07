#![recursion_limit = "512"]
mod comm;
mod html;
mod renm;
mod splt;

use std::{io::Result, path::PathBuf};

use clap::{Parser, Subcommand};
use html::Wrap;

#[derive(Parser, Debug)]
#[command(version = "2024-12-06")]
struct Args {
    #[command(subcommand)]
    command: Command,
}

#[derive(Subcommand, Debug)]
enum Command {
    Html {
        /// wrap option
        #[arg(short, long, default_value = "0")]
        wrap: Wrap,
        /// paths to look for images (recursive)
        #[arg(default_value = ".")]
        paths: Vec<PathBuf>,
    },
    Renm {
        /// root
        path: PathBuf,
        /// file to write tree
        tree: PathBuf,
    },
    Splt {
        /// root
        path: PathBuf,
    },
}

fn main() -> Result<()> {
    let args = Args::parse();
    match args.command {
        Command::Html { paths, wrap } => {
            for path in paths.iter() {
                html::run(&path, wrap)?
            }
        }
        Command::Renm { path, tree } => renm::run(&path, &tree)?,
        Command::Splt { path } => splt::run(&path)?,
    }
    Ok(())
}
