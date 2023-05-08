set -e

# directory containing individual PGNS
PGNS=$1
OUT_DIR=$2

mkdir -p $OUT_DIR

python get-uniques.py -i $1 | while read -r name; do
    echo "$name"
    python merge-pgn.py -i "$PGNS/$name*" -o "$OUT_DIR/$name.pgn"
done
