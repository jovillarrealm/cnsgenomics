#!/bin/bash

# $1 is the filtered stats file
# $2 is the directory where GENOMIC is 
out_dir=$(realpath "${2}")"/"
output_dir="$out_dir""GENOMIC_f"
mkdir -p "$out_dir" "$output_dir"

extract_code(){
    awk -F';' '{print $1}'
}



tail -n +2 "$1" |
extract_code |
tee names.txt |
xargs -I {} ln "$out_dir"GENOMIC/{} "$output_dir"/{}

