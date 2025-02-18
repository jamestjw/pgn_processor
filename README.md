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

## Create study
After merging the PGNs, you might want to create a study out of it

```bash
python create_study.py -i <pgn-dir> -t $LICHESS_TOKEN --study-id <study-id> --colour <white/black>
```
