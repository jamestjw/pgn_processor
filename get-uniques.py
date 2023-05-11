import re
import argparse
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_dir", type=Path, required=True)
    parser.add_argument("--chapter_name", action="store_true")

    args = parser.parse_args()
    return args


def get_pgn_name(p: Path) -> str:
    # Remove trailing numbers, e.g. #1
    return re.sub(r" #\d+$", "", p.stem)


def get_chapter_name(p: Path) -> str:
    return p.stem.split("-")[0].strip()


def main():
    args = parse_args()
    pgns = list(args.input_dir.glob("**/*.pgn"))
    getter = get_chapter_name if args.chapter_name else get_pgn_name
    names = {getter(p) for p in pgns}

    for name in names:
        print(name)


if __name__ == "__main__":
    main()
