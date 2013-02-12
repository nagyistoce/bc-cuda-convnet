#!/usr/bin/env bash

batches_count=5

path=`pwd`/PASCAL
files=`find $path/Annotations -name '*.xml'`
for item in $files; do
    tmp_item=`echo $item|sed s/\.xml$/.jpg/g|sed s/Annotations/JPEGImages/g`
    echo $item $tmp_item >> tmp_pascal.txt
done

image_count=`wc -l tmp_pascal.txt| cut -d " " -f 1`
((batches_size=image_count/batches_count))
split -d -l $batches_size tmp_pascal.txt pascal_batch_
wc -l pascal_batch_* |sed 's/^ *//' | head -n -2 > data.meta

python pascal_pickle.py

rm pascal_batch_*
rm tmp_pascal.txt
rm data.meta
