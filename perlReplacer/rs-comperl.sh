#!/bin/bash

out_dir=./
tmp_dir=/tmp/
diff_file="$out_dir""diff_file"
diffs_file="$out_dir""diffs_file"

tmperlfile="$out_dir""tmperlfile"
tmprsfile="$out_dir"tmpfile-rs

scripts_dir="$(dirname "$0")"
scripts_dir="$(realpath "$scripts_dir")"/

"$scripts_dir"count_fasta_cnsg.pl -i 100 "$@" > "$tmperlfile" 2> /dev/null
tail -n 13 "$tmperlfile" > "$tmp_dir"tmpfile && mv "$tmp_dir"tmpfile "$tmperlfile"

count-fasta-rs "$@" > "$tmprsfile"

diff -w "$tmperlfile" "$tmprsfile" > "$diff_file"

lines=$(wc -l "$diff_file" | awk '{print $1}')
if [[ "$lines" -gt 4  ]]
then
    echo "We have a problem:"
    echo "$@"
    cat "$diff_file" >> "$diffs_file"
else
    true
fi