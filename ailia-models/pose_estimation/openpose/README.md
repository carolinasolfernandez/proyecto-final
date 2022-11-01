# OpenPose

## Input

![Input](input.jpg)

(Image from https://pixabay.com/ja/photos/%E5%A5%B3%E3%81%AE%E5%AD%90-%E7%BE%8E%E3%81%97%E3%81%84-%E8%8B%A5%E3%81%84-%E3%83%9B%E3%83%AF%E3%82%A4%E3%83%88-5204299/)

Input shape : (1, 3, 240, 320)  
Range : [0, 255]

## Output

![Output](output.png)

- Confidence : (1, 19, 30, 40)
- Range : [0, 1.0]

## Note

OPENPOSE: MULTIPERSON KEYPOINT DETECTION
SOFTWARE LICENSE AGREEMENT
ACADEMIC OR NON-PROFIT ORGANIZATION NONCOMMERCIAL RESEARCH USE ONLY


## Usage

Automatically downloads the onnx and prototxt files on the first run.
It is necessary to be connected to the Internet while downloading.

For the sample image,
``` bash
$ python3 openpose.py
```

If you want to specify the input image, put the image path after the `--input` option.  
You can use `--savepath` option to change the name of the output file to save.
```bash
$ python3 openpose.py --input IMAGE_PATH --savepath SAVE_IMAGE_PATH
```

By adding the `--video` option, you can input the video.
If you pass `0` as an argument to VIDEO_PATH, you can use the webcam input instead of the video file.
```bash
$ python3 openpose.py --video VIDEO_PATH
```

Also you can set detection threshold by adding the `--threshold` option.
Default value is 0.3.

```bash
$ python3 openpose.py --threshold 0.2
```

By adding the `--single_scale` option, you can use single scale detection for performance.

```bash
$ python3 openpose.py --single_scale
```


## Reference

[Code repo for realtime multi-person pose estimation in CVPR'17 (Oral)](https://github.com/ZheC/Realtime_Multi-Person_Pose_Estimation)

## Framework

Caffe

## Model Format

CaffeModel

## Netron

[pose_deploy.prototxt](https://netron.app/?url=https://storage.googleapis.com/ailia-models/openpose/pose_deploy.prototxt)

