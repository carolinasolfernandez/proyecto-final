#! usr/bin/bash

# sh pipe_multiple.sh

video=large1

## declare an array variable
declare -a arr=("object_detection/yolov3" "object_detection/yolov7" "object_detection/yolox" "object_tracking/siam-mot")

## now loop through the above array
for model in "${arr[@]}"
do
   sh pipeline.sh -i ../data/videos/$video.mp4 -g ../data/gt/$video.txt -m "$model"
   sleep 15 # para recuperar recursos - cpu, ram, gpu y que las stats no den mal
   # or do whatever with individual element of the array
done