import argparse
import re
from pathlib import Path

import requests


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_dir", type=Path, required=True)
    parser.add_argument("-t", "--token", type=str, required=True)
    parser.add_argument(
        "--study-id", type=str, required=True, help="ID of existing lichess study"
    )
    parser.add_argument(
        "--colour", type=str, default="white", choices=["white", "black"]
    )

    args = parser.parse_args()
    return args


def get_index(p: Path) -> int:
    match re.findall(r"\d+", p.stem):
        case [e, *_]:
            return int(e)
        case _:
            return -1


class TokenSession(requests.Session):
    """Session capable of personal API token authentication.

    :param token: personal API token
    """

    def __init__(self, token: str):
        super().__init__()
        self.token = token
        self.headers = {"Authorization": f"Bearer {token}"}


def main():
    args = parse_args()
    pgns = list(args.input_dir.glob("**/*.pgn"))
    pgns = sorted(pgns, key=get_index)

    session = TokenSession(args.token)

    resp = session.get("https://lichess.org/api/account")
    resp.raise_for_status()
    account = resp.json()
    print(f"Connected to {account['username']}'s account")

    for pgn in pgns:
        name = pgn.stem
        payload = {
            "name": name,
            "pgn": open(pgn, "r").read(),
            "orientation": args.colour,
        }
        resp = session.post(
            f"https://lichess.org/api/study/{args.study_id}/import-pgn", json=payload
        )
        resp.raise_for_status()
        print(f"Created chapter {name}")


if __name__ == "__main__":
    main()
