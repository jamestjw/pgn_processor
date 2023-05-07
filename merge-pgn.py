# Note: Inspired by https://github.com/permutationlock/merge-pgn
# Author: Aven Bross
#
# Description: A simple tool to merge several pgn games into a single game with
# variations.

import chess.pgn
import sys
import argparse
from pathlib import Path
import glob
import re


# Sort based on i first, break ties using filename
def path_sort_key(p: Path):
    last = p.stem.split()[-1]
    m = re.search(r"#(\d)+", last)
    if last.isnumeric():
        i = int(last)
    # elif (m := re.search(r"#(\d)+", last)):
    elif m:
        i = int(m.groups(0)[0])
    else:
        i = 0
    return (i, p.stem)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input_pattern", type=str, required=True, help="Glob pattern for pgns"
    )
    parser.add_argument("-o", "--output_path", type=Path, required=True)

    args = parser.parse_args()

    games = []
    files = [p for p in glob.glob(args.input_pattern) if p.endswith(".pgn")]
    # Assume that better variations come last
    files.sort(key=lambda x: path_sort_key(Path(x)), reverse=True)

    if len(files) == 0:
        print(f"0 files detected for pattern {args.input_pattern}")
        return

    for file in files:
        if not file.endswith(".pgn"):
            continue

        print(f"Processing {file}")

        pgn = open(file, encoding="utf-8-sig")
        game = chess.pgn.read_game(pgn)
        while game is not None:
            games.append(game)
            game = chess.pgn.read_game(pgn)

    master_node = chess.pgn.Game()

    mlist = []
    for game in games:
        mlist.extend(game.variations)

    variations = [(master_node, mlist)]
    done = False
    while not done:
        newvars = []
        done = True
        for vnode, nodes in variations:
            newmoves = {}
            for node in nodes:
                if node.move is None:
                    continue
                elif node.move not in list(newmoves):
                    nvnode = vnode.add_variation(node.move, comment=node.comment)
                    if len(node.variations) > 0:
                        done = False
                    newvars.append((nvnode, node.variations))
                    newmoves[node.move] = len(newvars) - 1
                else:
                    nvnode, nlist = newvars[newmoves[node.move]]
                    if len(node.variations) > 0:
                        done = False
                    nlist.extend(node.variations)
                    newvars[newmoves[node.move]] = (nvnode, nlist)
        variations = newvars

    with open(args.output_path, "w") as fout:
        print(master_node, file=fout)


if __name__ == "__main__":
    main()
