#! usr/bin/bash

# sh pipe_multiple.sh

## declare an array variable
declare -a arr=("object_detection/yolov3" "object_detection/yolov7" "object_detection/yolox" "object_tracking/siam-mot")

## now loop through the above array
for model in "${arr[@]}"
do
   sh pipeline.sh -i ../data/videos/59.mp4 -g ../data/gt/59.txt -m "$model"
   # or do whatever with individual element of the array
done