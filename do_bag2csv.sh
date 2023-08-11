#!/bin/bash


file_prefix="c7_orb_stereo"
folder="orb"
folder="$folder/$file_prefix" # later add /$file_prefix_XX.* (see below)
#results in data of form */$folder/$file_prefix/$file_prefix_XX.*


for i in $(seq $1 1 $2)
do
    python3 bag2csv.py bags/$folder/$file_prefix"_"$i.bag gt
    python3 bag2csv.py bags/$folder/$file_prefix"_"$i.bag orb
done

for i in $(seq $1 1 $2)
do
    python3 rotate_coor.py \
    csv/$folder/$file_prefix"_"$i-gt.csv \
    csv/$folder/$file_prefix"_"$i-orb.csv
done
