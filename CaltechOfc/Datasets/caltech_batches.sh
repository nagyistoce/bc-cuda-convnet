#!/usr/bin/env bash

# Author: Milan Munzar, xmunza00@stud.fit.vutbr.cz
# Creating batches from Caltech101 images using it's methodology
# 3 training batches 2 testing


# initialization
training_count=30
testing_count=20
files="data.meta labels.meta training.txt testing.txt training_* testing_*"
rm -f $files
rm -f tmp_training.txt
rm -f tmp_testing.txt

# findinng images && recognizing classes
find `pwd`/Caltech101 -name '*.jpg' > tmp.txt
cat tmp.txt | sort -R > tmp1.txt
classes=`ls -l ./Caltech101/ | grep ^d | tr -s ' ' '~' | cut -d '~' -f 9`

# spliting images into training and testing set
id=0
for class in $classes; do
  train=$training_count
  test=$testing_count
  for item in `grep -e /$class/ < tmp1.txt`; do
    if [ $train -gt 0 ]; then
      echo $item $id >> tmp_training.txt
      ((train=train-1))
    elif [ $test -gt 0 ]; then
      echo $item $id >> tmp_testing.txt
      ((test=test-1))
    else
      break
    fi
  done
((id=id+1))
done

cat tmp_training.txt | sort -R > training.txt
cat tmp_testing.txt | sort -R > testing.txt

size=$(wc -l training.txt | awk -F " " '{print $1}')
split -d -l $((size/3)) training.txt training_
size=$(wc -l testing.txt | awk -F " " '{print $1}')
split -d -l $((size/2)) testing.txt testing_

# creating meta files
wc -l training_* | head -n-1 | sed 's/^ *//' >> data.meta
wc -l testing_* | head -n-1 | sed 's/^ *//' >> data.meta
ls -l --full-time ./Caltech101/ | grep ^d | tr -s ' ' '~' | cut -d '~' -f 9 > labels.meta

# pickle batches
python caltech_pickle.py

# clearing junk
rm tmp.txt
rm tmp1.txt
rm tmp_training.txt
rm tmp_testing.txt
rm $files

exit

