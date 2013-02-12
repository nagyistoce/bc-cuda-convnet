#!/usr/bin/env python

# Author: Milan Munzar, xmunza00@stud.fit.vutbr.cz
# Creating pickled batches from CALTECH101 datasets

import cPickle
import Image
import numpy as n

metaFile = open("data.meta", "r")
batchMetaLine = metaFile.read().splitlines()
batchNumber = 0
META_DATA = dict()
for line in batchMetaLine:
    metaData = line.split(" ")
    print metaData
    META_DATA['data_batch_%i' % batchNumber] = dict()
    META_DATA['data_batch_%i' % batchNumber]['num_cases_per_batch'] = metaData[0]
    images = []
    labels = []
    batchFile = open(metaData[1], "r")
    batchItems = batchFile.read().splitlines()
    for batchItem in batchItems:
        item = batchItem.split(" ")
        images.append(item[0])
        labels.append(item[1])
    META_DATA['data_batch_%i' % batchNumber]['data'] = n.array(images)
    META_DATA['data_batch_%i' % batchNumber]['labels'] = n.array(labels, dtype=n.uint8)
    batchNumber += 1
    batchFile.close()
    
labels_meta = open("labels.meta", "r")
label_names = []
for label in labels_meta:
    label_names.append(label)
META_DATA['label_names'] = n.array(label_names)

meta_file = open("./Caltech101/batches.meta", "wb")
cPickle.dump(META_DATA, meta_file, protocol=cPickle.HIGHEST_PROTOCOL)
meta_file.close()
labels_meta.close()
