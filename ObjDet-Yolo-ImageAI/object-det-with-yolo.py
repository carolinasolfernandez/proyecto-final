# -*- coding: utf-8 -*-
"""
Created on Tue May 10 21:15:53 2022

@author: ngloc
"""

from imageai.Detection import VideoObjectDetection

vid_obj_detect = VideoObjectDetection()

vid_obj_detect.setModelTypeAsYOLOv3()

vid_obj_detect.setModelPath(r"D:/UTN/CamIA/Test/3.object-det-with-yolo/yolo.h5")
vid_obj_detect.loadModel()


detected_vid_obj = vid_obj_detect.detectObjectsFromVideo(
    input_file_path =  r"D:/UTN/CamIA/Test/10sec2340x1080_ImagenRecortada.mp4",
    output_file_path = r"D:/UTN/CamIA/Test/3.object-det-with-yolo/24fpstest_10sec2340x1080_ImagenRecortada_procesado.mp4",
    frames_per_second=24,
    log_progress=True,
    return_detected_frame = True
)