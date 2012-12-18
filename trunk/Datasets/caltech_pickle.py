#!/usr/bin/env python

# Creating pickled batches from CALTECH101 datasets

import cPickle
import Image
import numpy as n

metaFile = open("data.meta", "r")
batchMetaLine = metaFile.read().splitlines()
batchNumber = 0
for line in batchMetaLine:
    metaData = line.split(" ")
    batchFile = open(metaData[1], "r")
    batchItems = batchFile.read().splitlines()
    images = []
    labels = []
    for batchItem in batchItems:
        item = batchItem.split(" ")
        labels.append(item[1])
        image = Image.open(item[0]).crop((0, 0, 200, 200))
        if image.mode is not 'RGB':
            image = image.convert('RGB')
        images.append(n.asarray(image).flatten())
    dataDic = dict()
    dataDic['data'] = n.array(images).T
    dataDic['labels'] = n.array(labels)
    print dataDic['data'].shape      
    pickledBatch = open("./Caltech101/data_batch_%i" % batchNumber, "wb")
    cPickle.dump(dataDic, pickledBatch, protocol=cPickle.HIGHEST_PROTOCOL)
    pickledBatch.close()
    batchNumber += 1

labels_meta = open("labels.meta", "r")
meta_file = open("./Caltech101/batches.meta", "wb")
meta_data = dict()
meta_data['num_cases_per_batch'] = dataDic['data'].shape[1]

label_names = []
for label in labels_meta:
    label_names.append(label)
meta_data['label_names'] = n.array(label_names)
cPickle.dump(meta_data, meta_file, protocol=cPickle.HIGHEST_PROTOCOL)
meta_file.close()

