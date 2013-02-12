#!/usr/bin/env python

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
    batchFile = open(metaData[1], "r")
    batchItems = batchFile.read().splitlines()
    META_DATA['data_batch_%i' % batchNumber] = dict()
    images = []
    labels = []
    for batchItem in batchItems:
        item = batchItem.split(" ")
        images.append(item[0])
        labels.append(item[1])
    META_DATA['data_batch_%i' % batchNumber]['data'] = n.array(images)
    META_DATA['data_batch_%i' % batchNumber]['labels'] = n.array(labels, dtype=n.uint8)
    batchNumber += 1
    batchFile.close()
    
labels_meta = open("labels.meta", "r")
meta_file = open("./Caltech101/batches.meta", "wb")
META_DATA['num_cases_per_batch'] = metaData[0]
label_names = []
for label in labels_meta:
    label_names.append(label)
META_DATA['label_names'] = n.array(label_names)

cPickle.dump(META_DATA, meta_file, protocol=cPickle.HIGHEST_PROTOCOL)
meta_file.close()
labels_meta.close()
