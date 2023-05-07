import re
import argparse
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_dir", type=Path, required=True)

    args = parser.parse_args()
    return args


def get_pgn_name(p: Path) -> str:
    # Remove trailing numbers, e.g. #1
    return re.sub(r" #\d+$", "", p.stem)


def main():
    args = parse_args()
    pgns = list(args.input_dir.glob("**/*.pgn"))
    names = {get_pgn_name(p) for p in pgns}

    for name in names:
        print(name)


if __name__ == "__main__":
    main()
