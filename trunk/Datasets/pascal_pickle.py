#!/usr/bin/env python

# Creating pickled batches from PASCAL dataset

import cPickle
import Image
import numpy
import xml.etree.ElementTree as et

pascal_objects = ('person', 'bird', 'cat', 'cow', 'dog', 'horse', 'sheep',
'aeroplane', 'bicycle', 'boat', 'bus', 'car', 'motorbike', 'train', 'bottle',
'chair', 'diningtable', 'pottedplant', 'sofa', 'tvmonitor')


PICKLE_DATA = dict()
f_meta = open('data.meta', 'r')
meta_lines = f_meta.read().splitlines()
curr_batchnum = 0
for meta in meta_lines:
    meta = meta.split(' ')
    f_batch = open(meta[1], 'r')
    batch_lines = f_batch.read().splitlines()
    images = []
    labels = []
    PICKLE_DATA['data_batch_%i' % curr_batchnum] = dict()
    for item in batch_lines:
        item = item.split(' ')
        images.append(item[1])
        xml_root = et.parse(item[0]).getroot()
        xml_object = xml_root.find('object')
        labels.append (pascal_objects.index(xml_object.find('name').text))       
    PICKLE_DATA['data_batch_%i' % curr_batchnum]['data'] = numpy.array(images)
    PICKLE_DATA['data_batch_%i' % curr_batchnum]['labels'] = numpy.array(labels, dtype=numpy.uint8)
    curr_batchnum += 1
    f_batch.close()

PICKLE_DATA['num_cases_per_batch'] = meta[0]
label_names = list(pascal_objects)
PICKLE_DATA['label_names'] = numpy.array(label_names)
file_pickle = open("./PASCAL/batches.meta", "wb")
cPickle.dump(PICKLE_DATA, file_pickle, protocol=cPickle.HIGHEST_PROTOCOL)

file_pickle.close()
f_meta.close()

print 'Created %i batches' % curr_batchnum

