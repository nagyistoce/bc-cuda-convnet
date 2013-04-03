# Copyright (c) 2011, Alex Krizhevsky (akrizhevsky@gmail.com)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# - Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# 
# - Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from data import *
import numpy.random as nr
import numpy as n
import random as r
import cPickle
import Image
import ImageOps 
 
##########################################################################################################
# Caltech101 provider: 3.4.2013, xmunza00@stud.fit.vutbr.cz
# grayscale - scale preservation - left/right reflections

class CALTECH101DataProvider(LabeledDataProvider):
    def __init__(self, data_dir, batch_range, init_epoch=1, init_batchnum=None, dp_params={}, test=False):
        LabeledDataProvider.__init__(self, data_dir, batch_range, init_epoch, init_batchnum, dp_params, test)
        self.img_size = 140
        batch_file = open(data_dir + '/batches.meta', 'rb')
        self.batch_dict = cPickle.load(batch_file)
        batch_file.close()
                
    def get_next_batch(self):
        datadic = dict(); images = []; labels = []
        for i in range(int(self.batch_dict['num_cases_per_batch'])):
            image = Image.open(self.batch_dict['data_batch_%i' % self.curr_batchnum]['data'][i])
            if image.mode is not 'RGB':
                image = image.convert('RGB')
            # grayscale thumbnail
            image = ImageOps.grayscale(image)
            image.thumbnail((self.img_size, self.img_size), Image.ANTIALIAS)
            image = image.crop((0, 0, self.img_size, self.img_size))
            images.append(n.asarray(image).flatten())
            labels.append(self.batch_dict['data_batch_%i' % self.curr_batchnum]['labels'][i])
            # left/right reflection
            if not self.test: 
                images.append(n.fliplr(n.asarray(image)).flatten())
                labels.append(self.batch_dict['data_batch_%i' % self.curr_batchnum]['labels'][i])
                                               
        datadic['data'] = n.array(images, dtype=n.single, order='C').T
        datadic['labels'] = n.array(labels, dtype=n.single, order='C')
        datadic['data'] = n.require(datadic['data'], dtype=n.single, requirements='C')
        datadic['labels'] = n.require(datadic['labels'].reshape((1, datadic['data'].shape[1])), dtype=n.single, requirements='C')
        epoch, batchnum = self.curr_epoch, self.curr_batchnum
        self.advance_batch()
        return epoch, batchnum, [datadic['data'], datadic['labels']]
        
    # Returns the dimensionality of the two data matrices returned by get_next_batch
    # idx is the index of the matrix. 
    def get_data_dims(self, idx=0):
        return self.img_size**2 if idx == 0 else 1
        
    def get_plottable_data(self, data):
        return n.require(data.T.reshape(data.shape[1], 3, self.img_size, self.img_size).swapaxes(1,3).swapaxes(1,2) / 255.0, dtype=n.single)
        
# end class
##########################################################################################################

##########################################################################################################
# Caltech101 provider: 3.4.2013, xmunza00@stud.fit.vutbr.cz
# grayscale - resize - random patches - left-right reflections

class CroppedCALTECH101DataProvider(LabeledDataProvider):
    def __init__(self, data_dir, batch_range, init_epoch=1, init_batchnum=None, dp_params={}, test=False):
        LabeledDataProvider.__init__(self, data_dir, batch_range, init_epoch, init_batchnum, dp_params, test)
        self.img_size = 140
        self.border_size = dp_params['crop_border']
        self.inner_size = self.img_size - self.border_size * 2
        batch_file = open(data_dir + '/batches.meta', 'rb')
        self.batch_dict = cPickle.load(batch_file)
        batch_file.close()
    
    def get_next_batch(self):
        datadic = dict(); images = []; labels = []
        for i in range(int(self.batch_dict['num_cases_per_batch'])):
            image = Image.open(self.batch_dict['data_batch_%i' % self.curr_batchnum]['data'][i])
            if image.mode is not 'RGB':
                image = image.convert('RGB')
            image = image.resize((self.img_size,self.img_size), Image.ANTIALIAS)
            image = ImageOps.grayscale(image)
            if not self.test:
                # appending center patch with reflection
                image_cropped = image.crop((self.border_size, self.border_size, self.img_size - self.border_size, self.img_size - self.border_size))
                images.append(n.asarray(image_cropped).flatten())
                labels.append(self.batch_dict['data_batch_%i' % self.curr_batchnum]['labels'][i])
                images.append(n.fliplr(n.asarray(image_cropped)).flatten())
                labels.append(self.batch_dict['data_batch_%i' % self.curr_batchnum]['labels'][i])
                # appending next 10 random patches from image with reflections
                for x in xrange(10):
                    # random image patches
                    startY, startX = nr.randint(0,self.border_size*2 + 1), nr.randint(0,self.border_size*2 + 1)
                    endY, endX = startY + self.inner_size, startX + self.inner_size
                    image_cropped = image.crop((startX, startY, endX, endY))
                    images.append(n.asarray(image_cropped).flatten())
                    labels.append(self.batch_dict['data_batch_%i' % self.curr_batchnum]['labels'][i])
                    # append left-righ reflections with 50% probability
                    if nr.randint(2) == 0:
                        images.append(n.fliplr(n.asarray(image_cropped)).flatten())
                        labels.append(self.batch_dict['data_batch_%i' % self.curr_batchnum]['labels'][i])
            else:
                # testing on center patches
                image_cropped = image.crop((self.border_size, self.border_size, self.img_size - self.border_size, self.img_size - self.border_size))
                images.append(n.asarray(image_cropped).flatten())
                labels.append(self.batch_dict['data_batch_%i' % self.curr_batchnum]['labels'][i])
                                              
        datadic['data'] = n.array(images, dtype=n.single, order='C').T
        datadic['labels'] = n.array(labels, dtype=n.single, order='C')
        datadic['data'] = n.require(datadic['data'], dtype=n.single, requirements='C')
        datadic['labels'] = n.require(datadic['labels'].reshape((1, datadic['data'].shape[1])), dtype=n.single, requirements='C')
        epoch, batchnum = self.curr_epoch, self.curr_batchnum
        self.advance_batch()
        return epoch, batchnum, [datadic['data'], datadic['labels']]    
        
    # Returns the dimensionality of the two data matrices returned by get_next_batch
    # idx is the index of the matrix. 
    def get_data_dims(self, idx=0):
        return self.inner_size**2 if idx == 0 else 1
        
    def get_plottable_data(self, data):
        return n.require(data.T.reshape(data.shape[1], 3, self.img_size, self.img_size).swapaxes(1,3).swapaxes(1,2) / 255.0, dtype=n.single)

# end class
##########################################################################################################
           
class CIFARDataProvider(LabeledMemoryDataProvider):
    def __init__(self, data_dir, batch_range, init_epoch=1, init_batchnum=None, dp_params={}, test=False):
        LabeledMemoryDataProvider.__init__(self, data_dir, batch_range, init_epoch, init_batchnum, dp_params, test)
        self.data_mean = self.batch_meta['data_mean']
        self.num_colors = 3
        self.img_size = 32
        # Subtract the mean from the data and make sure that both data and
        # labels are in single-precision floating point.
        for d in self.data_dic:
            # This converts the data matrix to single precision and makes sure that it is C-ordered
            d['data'] = n.require((d['data'] - self.data_mean), dtype=n.single, requirements='C')
            d['labels'] = n.require(d['labels'].reshape((1, d['data'].shape[1])), dtype=n.single, requirements='C')

    def get_next_batch(self):
        epoch, batchnum, datadic = LabeledMemoryDataProvider.get_next_batch(self)
        return epoch, batchnum, [datadic['data'], datadic['labels']]

    # Returns the dimensionality of the two data matrices returned by get_next_batch
    # idx is the index of the matrix. 
    def get_data_dims(self, idx=0):
        return self.img_size**2 * self.num_colors if idx == 0 else 1
    
    # Takes as input an array returned by get_next_batch
    # Returns a (numCases, imgSize, imgSize, 3) array which can be
    # fed to pylab for plotting.
    # This is used by shownet.py to plot test case predictions.
    def get_plottable_data(self, data):
        return n.require((data + self.data_mean).T.reshape(data.shape[1], 3, self.img_size, self.img_size).swapaxes(1,3).swapaxes(1,2) / 255.0, dtype=n.single)
    
class CroppedCIFARDataProvider(LabeledMemoryDataProvider):
    def __init__(self, data_dir, batch_range=None, init_epoch=1, init_batchnum=None, dp_params=None, test=False):
        LabeledMemoryDataProvider.__init__(self, data_dir, batch_range, init_epoch, init_batchnum, dp_params, test)

        self.border_size = dp_params['crop_border']
        self.inner_size = 32 - self.border_size*2
        self.multiview = dp_params['multiview_test'] and test
        self.num_views = 5*2
        self.data_mult = self.num_views if self.multiview else 1
        self.num_colors = 3
        
        for d in self.data_dic:
            d['data'] = n.require(d['data'], requirements='C')
            d['labels'] = n.require(n.tile(d['labels'].reshape((1, d['data'].shape[1])), (1, self.data_mult)), requirements='C')
        
        self.cropped_data = [n.zeros((self.get_data_dims(), self.data_dic[0]['data'].shape[1]*self.data_mult), dtype=n.single) for x in xrange(2)]

        self.batches_generated = 0
        self.data_mean = self.batch_meta['data_mean'].reshape((3,32,32))[:,self.border_size:self.border_size+self.inner_size,self.border_size:self.border_size+self.inner_size].reshape((self.get_data_dims(), 1))

    def get_next_batch(self):
        epoch, batchnum, datadic = LabeledMemoryDataProvider.get_next_batch(self)

        cropped = self.cropped_data[self.batches_generated % 2]

        self.__trim_borders(datadic['data'], cropped)
        cropped -= self.data_mean
        self.batches_generated += 1
        return epoch, batchnum, [cropped, datadic['labels']]
        
    def get_data_dims(self, idx=0):
        return self.inner_size**2 * 3 if idx == 0 else 1

    # Takes as input an array returned by get_next_batch
    # Returns a (numCases, imgSize, imgSize, 3) array which can be
    # fed to pylab for plotting.
    # This is used by shownet.py to plot test case predictions.
    def get_plottable_data(self, data):
        return n.require((data + self.data_mean).T.reshape(data.shape[1], 3, self.inner_size, self.inner_size).swapaxes(1,3).swapaxes(1,2) / 255.0, dtype=n.single)
    
    def __trim_borders(self, x, target):
        y = x.reshape(3, 32, 32, x.shape[1])

        if self.test: # don't need to loop over cases
            if self.multiview:
                start_positions = [(0,0),  (0, self.border_size*2),
                                   (self.border_size, self.border_size),
                                  (self.border_size*2, 0), (self.border_size*2, self.border_size*2)]
                end_positions = [(sy+self.inner_size, sx+self.inner_size) for (sy,sx) in start_positions]
                for i in xrange(self.num_views/2):
                    pic = y[:,start_positions[i][0]:end_positions[i][0],start_positions[i][1]:end_positions[i][1],:]
                    target[:,i * x.shape[1]:(i+1)* x.shape[1]] = pic.reshape((self.get_data_dims(),x.shape[1]))
                    target[:,(self.num_views/2 + i) * x.shape[1]:(self.num_views/2 +i+1)* x.shape[1]] = pic[:,:,::-1,:].reshape((self.get_data_dims(),x.shape[1]))
            else:
                pic = y[:,self.border_size:self.border_size+self.inner_size,self.border_size:self.border_size+self.inner_size, :] # just take the center for now
                target[:,:] = pic.reshape((self.get_data_dims(), x.shape[1]))
        else:
            for c in xrange(x.shape[1]): # loop over cases
                startY, startX = nr.randint(0,self.border_size*2 + 1), nr.randint(0,self.border_size*2 + 1)
                endY, endX = startY + self.inner_size, startX + self.inner_size
                pic = y[:,startY:endY,startX:endX, c]
                if nr.randint(2) == 0: # also flip the image with 50% probability
                    pic = pic[:,:,::-1]
                target[:,c] = pic.reshape((self.get_data_dims(),))
    
class DummyConvNetDataProvider(LabeledDummyDataProvider):
    def __init__(self, data_dim):
        LabeledDummyDataProvider.__init__(self, data_dim)
        
    def get_next_batch(self):
        epoch, batchnum, dic = LabeledDummyDataProvider.get_next_batch(self)
        
        dic['data'] = n.require(dic['data'].T, requirements='C')
        dic['labels'] = n.require(dic['labels'].T, requirements='C')
        
        return epoch, batchnum, [dic['data'], dic['labels']]
    
    # Returns the dimensionality of the two data matrices returned by get_next_batch
    def get_data_dims(self, idx=0):
        return self.batch_meta['num_vis'] if idx == 0 else 1
        
