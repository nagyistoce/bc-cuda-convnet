#!/usr/bin/env python

#############################################################################################
# Changes: 8.4 2013
# Author: Milan Munzar, xmunza00@stud.fit.vutbr.cz
# Creating pickled batches from CALTECH101 datasets

import sys
import os
import cPickle
import Image
import ImageOps
import numpy

#############################################################################################
# parsing arguments
patches = 0
if ( '-p' in sys.argv ):
    patches = 1
reflections = 0
if ( '-r' in sys.argv ):
    reflections = 1

#############################################################################################
# defining mean and deviation normalization
data_mean = 0
data_stddev = 0
num_pics = 0

#############################################################################################
# preprocessing
img_size = 140

#############################################################################################
# creating pickled batches
metaFile = open("data.meta", "r")
batchMetaLine = metaFile.read().splitlines()
batchNumber = 0
META_DATA = dict()
print "Preprocessing images"
for line in batchMetaLine:
    metaData = line.split(" ")
    print metaData
    META_DATA['data_batch_%i' % batchNumber] = dict()
    images = []
    labels = []
    batchFile = open(metaData[1], "r")
    batchItems = batchFile.read().splitlines()
    for batchItem in batchItems:
        # open image
        item = batchItem.split(" ")
        image = Image.open(item[0])
        if image.mode is not 'RGB':
            image = image.convert('RGB')
        # grayscale image
        image = ImageOps.grayscale(image)
        image.thumbnail((img_size, img_size), Image.ANTIALIAS)
        image = image.crop((0, 0, img_size, img_size))
        array = numpy.asarray(image)
        images.append(array.flatten())
        labels.append(item[1])
        data_mean = data_mean + array.mean()
        data_stddev = data_stddev if ( data_stddev > array.std() ) else array.std() 
        # reflection
        if ( reflections ):
            images.append(numpy.fliplr(array).flatten())
            labels.append(item[1])
            data_mean = data_mean + array.mean()
            data_stddev = data_stddev if ( data_stddev > array.std() ) else array.std()
    # adding data to dict               
    META_DATA['data_batch_%i' % batchNumber]['data'] = numpy.array(images)
    META_DATA['data_batch_%i' % batchNumber]['labels'] = numpy.array(labels, dtype=numpy.uint8)
    if ( reflections ):
        META_DATA['data_batch_%i' % batchNumber]['num_cases_per_batch'] = int(metaData[0]) * 2
        num_pics = num_pics + int(metaData[0]) * 2
    else:
        META_DATA['data_batch_%i' % batchNumber]['num_cases_per_batch'] = metaData[0]
        num_pics = num_pics + int(metaData[0])     
    batchNumber += 1
    batchFile.close()

#############################################################################################
# mean and std deviation 
data_mean = data_mean / num_pics
print "Pic count:           %i" % num_pics
print "Data mean:           %f" % data_mean
print "Standard deviation:  %f" % data_stddev
META_DATA['data_mean'] = data_mean
META_DATA['standard_deviation'] = data_stddev
META_DATA['image_size'] = img_size

#############################################################################################
# label names    
labels_meta = open("labels.meta", "r")
label_names = []
for label in labels_meta:
    label_names.append(label)
META_DATA['label_names'] = numpy.array(label_names)

#############################################################################################
# pickling
meta_file = open("./Caltech101/batches.meta", "wb")
cPickle.dump(META_DATA, meta_file, protocol=cPickle.HIGHEST_PROTOCOL)
meta_file.close()
labels_meta.close()


# EOF
#############################################################################################

