#!/bin/bash

# $1 is the filtered filenames file
# $2 is the directory where GENOMIC is

out_dir=$(realpath "${2}")"/"
input_dir="$out_dir"GENOMIC/
output_dir="$out_dir""GENOMIC_r"/
mkdir -p "$output_dir"

extract_code(){
    awk -F';' '{print $1}'
}



xargs -I {} ln "$input_dir"{} "$output_dir"{} < "$1"