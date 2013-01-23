#!/bin/sh

# Starts training neural net

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

caltech_test(){
python convnet.py --data-path=./Datasets/Caltech101 \
                  --save-path=./STORAGE/CALTECH \
                  --test-range=5-6  \
                  --train-range=1-4 \
                  --layer-def=./example-layers/layers-19pct.cfg \
                  --layer-params=./example-layers/layer-params-19pct.cfg \
                  --data-provider=caltech101 \
                  --test-freq=2 \
                  --epochs=10
}

caltech_1(){
python convnet.py --data-path=./Datasets/Caltech101 \
                  --save-path=./Storage/Caltech_1 \
                  --test-range=5-6  \
                  --train-range=1-4 \
                  --layer-def=./Datasets/Caltech101/1D.cfg \
                  --layer-params=./Datasets/Caltech101/1P.cfg \
                  --data-provider=caltech101 \
                  --test-freq=15 \
                  --epochs=10
}

caltech_2(){
python convnet.py --data-path=./Datasets/Caltech101 \
                  --save-path=./Storage/Caltech_2 \
                  --test-range=5-6  \
                  --train-range=1-4 \
                  --layer-def=./Datasets/Caltech101/2D.cfg \
                  --layer-params=./Datasets/Caltech101/2P.cfg \
                  --data-provider=caltech101 \
                  --test-freq=15 \
                  --epochs=10
}

caltech_1

exit 0
