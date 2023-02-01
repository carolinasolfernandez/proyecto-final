import cv2
import os

# Define the location of the images
images_folder = "MOT17-09"

# Define the location and name of the output video file
video_file = "MOT17-09.mp4"

# Get a list of the images
images = [img for img in os.listdir(images_folder) if img.endswith(".jpg")]
images = sorted(images, key=lambda x: int(x.split(".")[0]))

# Read the first image to get its size
frame = cv2.imread(os.path.join(images_folder, images[0]))
height, width, channels = frame.shape

# Define the video codec and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(video_file, fourcc, 30.0, (width, height))

# Write the frames to the video
for image_name in images:
    frame = cv2.imread(os.path.join(images_folder, image_name))
    out.write(frame)

# Release the VideoWriter object
out.release()