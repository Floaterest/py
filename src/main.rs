#![recursion_limit = "512"]
mod html;
mod renm;
mod tree;

use std::{io::Result, path::PathBuf};

use clap::{Parser, Subcommand};
use html::Wrap;

#[derive(Parser, Debug)]
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
        paths: Vec<PathBuf>,
    },
    Renm {
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
        Command::Renm { path } => renm::run(&path)?,
    }
    Ok(())
}
