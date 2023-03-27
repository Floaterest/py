mod html;

use std::{error::Error, path::PathBuf};

use clap::{Parser, Subcommand, ValueEnum};


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
}

#[derive(ValueEnum, Debug, Clone)]
pub enum Wrap {
    /// no wrap
    #[clap(alias = "0")]
    NoWrap,
    /// wrap after odd pages
    #[clap(alias = "1")]
    WrapOdd,
    /// wrap after even pages
    #[clap(alias = "2")]
    WrapEven,
    #[clap(alias = "g")]
    /// guess between odd and even
    Guess,
}

fn main() -> Result<(), Box<dyn Error>> {
    let args = Args::parse();
    match args.command {
        Command::Html { path, wrap } => html::run(path, wrap)?,
    }
    Ok(println!("Hello, world!"))
}
