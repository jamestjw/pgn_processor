# pgn_processor

## Split
Split up a PGN file that contains multiple games.

```bash
python split.py -i "input.pgn" -o "output_dir"
```

## Merge
Merge multiple PGNs into a single file by merging variations. Uses a `glob` pattern to find PGN files.
```bash
python merge-pgn.py -i "pgn_dir/*pgn_pattern*" -o "output.pgn"
```
