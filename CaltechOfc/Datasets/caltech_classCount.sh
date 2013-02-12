#!/usr/bin/env bash

find `pwd`/Caltech101 -name '*.jpg' > tmp.txt
classes=`ls -l ./Caltech101/ | grep ^d | tr -s ' ' '~' | cut -d '~' -f 9`
for class in $classes; do
    echo $class `grep -c -e /$class/ < tmp.txt`
done

echo ${classes} | wc -w

rm tmp.txt
