#! usr/bin/bash

# sh pipe_multiple.sh

## declare an array variable
declare -a arr=("object_detection/pedestrian_detection" "object_detection/yolox" "object_detection/yolov1-tiny" "object_detection/yolov2" "object_detection/yolov3" "object_tracking/siam-mot")

## now loop through the above array
for model in "${arr[@]}"
do
   sh pipeline.sh -i ../data/videos/large1.mp4 -g ../data/gt/large1.txt -m "$model"
   # or do whatever with individual element of the array
done