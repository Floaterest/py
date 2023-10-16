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
        /// path to look for images (recursive)
        path: PathBuf,
    },
    Renm {
        /// root
        path: PathBuf,
    },
}

fn main() -> Result<()> {
    let args = Args::parse();
    match args.command {
        Command::Html { path, wrap } => html::run(&path, wrap)?,
        Command::Renm { path } => renm::run(&path)?,
    }
    Ok(())
}
