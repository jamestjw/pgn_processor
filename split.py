import argparse
from pathlib import Path
from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_pgn", type=Path, required=True)
    parser.add_argument("-o", "--output_dir", type=Path, required=True)

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    if not args.output_dir.exists():
        args.output_dir.mkdir(parents=True)

    process_pgn_file(args.input_pgn, args.output_dir)


def process_pgn_file(filename, output_dir: Path):
    with open(filename, "r") as f:
        curr_game = []
        for line in tqdm(f):
            if "[Event" in line:
                if len(curr_game) != 0:
                    save_game(curr_game, output_dir)
                curr_game = [line]
            else:
                curr_game.append(line)
        # Handle last game
        if len(curr_game) != 0:
            save_game(curr_game, output_dir)


def save_game(game: list, output_dir):
    white = next(filter(lambda x: x.startswith("[White"), game)).split('"')[1]
    black = next(filter(lambda x: x.startswith("[Black"), game)).split('"')[1]
    output_name = f"{white} -- {black}.pgn".replace("/", " or ")
    game_txt = "".join(game)

    save_path = output_dir / output_name
    with open(save_path, "w") as fout:
        fout.write(game_txt)


if __name__ == "__main__":
    main()
