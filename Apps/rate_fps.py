import numpy as np
import cv2

'''
Modifica la cantidad de fps y tamano del video.
Seteado ahora en dividir a 1/3 los fps
'''

video = '../data/videos/large1.mp4'
out = 'large1-10fps.mp4'
x,y,h,w = 0,0,720,1280


# Open the video
cap = cv2.VideoCapture(video)

# Initialize frame counter
cnt = 0

# Some characteristics from the original video
w_frame, h_frame = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps, frames = cap.get(cv2.CAP_PROP_FPS), cap.get(cv2.CAP_PROP_FRAME_COUNT)


# Here you can define your croping values
# x,y,h,w = 350,200,720,1280
# output
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
#out = cv2.VideoWriter('720x1280-x350-y200_originalfps.mp4', fourcc, fps, (w, h))
out = cv2.VideoWriter(out, fourcc, fps/3, (w, h))

frames_mid_eliminate=0

# Now we start
while(cap.isOpened()):
    ret, frame = cap.read()
    cnt += 1 # Counting frames
    
    # Avoid problems when video finish
    if ret==True:
        if frames_mid_eliminate != 0:
            frames_mid_eliminate+=1
            if frames_mid_eliminate == 3:
                frames_mid_eliminate=0
            continue

        frames_mid_eliminate+=1
        # Croping the frame
        crop_frame = frame[y:y+h, x:x+w]

        # Percentage

        # Saving from the desired frames
        #if 15 <= cnt <= 90:
        #    out.write(crop_frame)

        # I see the answer now. Here you save all the video
        out.write(crop_frame)

        # Just to see the video in real time          
        cv2.imshow('frame',frame)
        cv2.imshow('croped',crop_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break


cap.release()
out.release()
cv2.destroyAllWindows()