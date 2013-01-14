#!/bin/sh

# Starts training neural net

#Available layers
#caltech.cfg             layer-params-80sec.cfg             layer-params.gc.cfg  layers-conv-local-11pct.cfg
#caltech-params.cfg      layer-params-conv-local-11pct.cfg  layers-18pct.cfg     layers-conv-local-13pct.cfg
#layer-params-18pct.cfg  layer-params-conv-local-13pct.cfg  layers-19pct.cfg     layers-example.cfg
#layer-params-19pct.cfg  layer-params-example.cfg           layers-80sec.cfg     layers.gc.cfg

pascal(){
python convnet.py --data-path=./Datasets/PASCAL \
                  --save-path=./STORAGE/PASCAL \
                  --test-range=5-6  \
                  --train-range=1-4 \
                  --layer-def=./example-layers/layers-19pct.cfg \
                  --layer-params=./example-layers/layer-params-19pct.cfg \
                  --data-provider=caltech101 \
                  --test-freq=2 \
                  --epochs=10
}

caltech(){
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

pascal

exit 0
