#!/bin/bash

# $1 es el stats
# $2 es el directorio donde están los genomas
extract_code(){
awk -F'[_.;]' '{print $1 "_" $2}' 
}

tail -n +2 "$1" |
extract_code > codes.txt