set -e

# path to individual pgn
PGN=$1
OUT_DIR=$2

mkdir -p "$OUT_DIR/individuals" "$OUT_DIR/merged"

python split.py -i "$PGN" -o "$OUT_DIR/individuals"

python get-uniques.py -i "$OUT_DIR/individuals" --chapter_name | while read -r name; do
    echo "Merging $name"
    python merge-pgn.py -i "$OUT_DIR/individuals/$name*" -o "$OUT_DIR/merged/$name.pgn"
done
