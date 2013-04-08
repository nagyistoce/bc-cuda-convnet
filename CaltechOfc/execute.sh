#!/bin/sh

#############################################################################################
# starts training neural net with desirable parameters

#############################################################################
# providers
cifar(){
python convnet.py   --data-path=./Datasets/CIFAR \
                    --save-path=./STORAGE/CIFAR \
                    --test-range=2 \
                    --train-range=1 \
                    --layer-def=./example-layers/layers-conv-local-13pct.cfg \
                    --layer-params=./example-layers/layer-params-conv-local-13pct.cfg \
                    --data-provider=cifar \
                    --test-freq=13 \
                    --crop-border=4 \
                    --epochs=100
}

caltechNormalized(){
python convnet.py --data-path=./Datasets/Caltech101 \
                  --save-path=./Storage/Caltech_8 \
                  --test-range=3-4 \
                  --train-range=0-2 \
                  --layer-def=./Datasets/Caltech101/2D.cfg \
                  --layer-params=./Datasets/Caltech101/2P.cfg \
                  --data-provider=caltech101-normalized \
                  --test-freq=10 \
                  --epochs=200
}

caltech(){
python convnet.py --data-path=./Datasets/Caltech101 \
                  --save-path=./Storage/Caltech_2_NormRef \
                  --test-range=3-4 \
                  --train-range=0-2 \
                  --layer-def=./Datasets/Caltech101/2D.cfg \
                  --layer-params=./Datasets/Caltech101/2P.cfg \
                  --data-provider=caltech101 \
                  --test-freq=10 \
                  --epochs=200
}

#############################################################################
# start training neural net with desired data provider
caltechNormalized

exit
# EXIT
#############################################################################################


