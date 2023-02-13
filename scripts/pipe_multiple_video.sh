#! usr/bin/bash

# sh pipe_multiple_video.sh

videoName=large1

## declare an array variable
declare -a arr=("out11.mp4" "out12.mp4" "out21.mp4" "out22.mp4")

## now loop through the above array
for videoPart in "${arr[@]}"
do
   sh pipeline.sh -i ../data/videos/large1-matrix/$videoPart -g ../data/gt/$video.txt -m "object_tracking/siam-mot"
   # or do whatever with individual element of the array
done