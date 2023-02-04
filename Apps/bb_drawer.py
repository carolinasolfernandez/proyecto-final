import csv
import cv2

GT="../data/gt/59.txt"
video="../data/videos/59.mp4"
videoOut="../data/videos/59-bb.mp4"

# Read the ground truth data from a CSV file
with open(GT, "r") as file:
    reader = csv.reader(file)
    data = [row for row in reader]

# Load the video
cap = cv2.VideoCapture(video)

# Get the video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Create a VideoWriter object to save the output video
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(videoOut, fourcc, fps, (frame_width, frame_height))

# Loop through each frame of the video
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Draw the bounding boxes for the detections in this frame
    for i, row in enumerate(data):
        if int(row[0]) == int(cap.get(cv2.CAP_PROP_POS_FRAMES)):
            x = int(float(row[2]))
            y = int(float(row[3]))
            w = int(float(row[4]))
            h = int(float(row[5]))
            z = int(float(row[9]))
            id = int(row[1])
            if z == 0:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            else:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Add the id to the top of the bounding box
            cv2.putText(frame, str(id), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Write the frame with the bounding boxes to the output video
    out.write(frame)

# Clean up
cap.release()
out.release()
cv2.destroyAllWindows()