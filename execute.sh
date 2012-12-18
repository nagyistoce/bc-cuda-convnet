#!/bin/sh

# Starts training neural net

caltech(){
python convnet.py --data-path=./Datasets/Caltech101 \
                  --save-path=./STORAGE/CALTECH \
                  --test-range=6-7  \
                  --train-range=1-5 \
                  --layer-def=./example-layers/caltech.cfg \
                  --layer-params=./example-layers/caltech-params.cfg \
                  --data-provider=caltech101 \
                  --test-freq=2 \
                  --epochs=10
}

cifar(){
python convnet.py   --data-path=./Datasets/CIFAR \
                    --save-path=/STORAGE/CIFAR \
                    --test-range=2 \
                    --train-range=1 \
                    --layer-def=./example-layers/layers-conv-local-13pct.cfg \
                    --layer-params=./example-layers/layer-params-conv-local-13pct.cfg \
                    --data-provider=cifar \
                    --test-freq=13 \
                    --crop-border=4 \
                    --epochs=100
}

caltech

exit 0
