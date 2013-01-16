#!/usr/bin/env bash

name="TMP_batch_"

batchesCount=10
while getopts  "n:d" flag
do
  case $flag in
     n) nflag=1
        batchesCount=$OPTARG;;
     d)
        rm -vf $name*
        exit 0
   esac
done

i=0
find `pwd`/Caltech101 -name '*.jpg' > tmp.txt
classes=`ls -l ./Caltech101/ | grep ^d | tr -s ' ' ':' | cut -d ':' -f 9 | tail -n +2`
for class in $classes; do
    for item in `grep $class < tmp.txt`; do
        echo "$item $i" >> tmp1.txt
    done
    ((i=i+1))
done

cat tmp1.txt |sort -R > tmp.txt

imagesCount=`wc -l tmp.txt | cut -d " " -f 1`
((batchSize=imagesCount/batchesCount))

split -d -l $batchSize tmp.txt ./$name
rm tmp.txt
rm tmp1.txt

wc -l $name* |sed 's/^ *//' | head -n -2 > data.meta
ls -l --full-time ./Caltech101/ | grep ^d | tr -s ' ' '~' | cut -d '~' -f 9 > labels.meta


python caltech_pickle.py

rm $name*
rm -f data.meta
rm -f labels.meta

exit 0

