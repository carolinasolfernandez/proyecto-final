import numpy as np
import cv2

video = '../data/videos/large1.mp4'
out = 'out.mp4'

start_frame=1720
last_frame=1720
x,y,w,h =1145,	43,	56,	163

  #108 -> reconocido 0.428 OK
#x,y,w,h = 702,	368,	24,	39  #108 -> reconocido 0.428 OK
#x,y,w,h = 612,	1,	50,	108 #112 0.52 -> No son piernas NOK
#x,y,w,h = 1146,	33,	58,	209 #123 0.57 -> no Reconocido OK
#x,y,w,h = 614,	327,	141,	180 #115 0.58 -> Reconocido OK
#x,y,w,h = 544,	96,	123,	287 #110 0.60 -> reconocido OK
#x,y,w,h = 267,	136,	146,	233 #23 0.97
#x,y,w,h = 1152,	24,	124,	227 #101 0.97
#x,y,w,h = 623,	287,	242,	232 #122 0.97
#x,y,w,h = 1036,	424,	214,	285 #2 0.98
#x,y,w,h = 1011,	108,	158,	214 #120 0.99


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
out = cv2.VideoWriter(out, fourcc, fps, (w, h))


# Now we start
while(cap.isOpened()):
    ret, frame = cap.read()

    cnt += 1 # Counting frames

    # Avoid problems when video finish
    if ret==True:
        if cnt < start_frame:
            continue
        if cnt > last_frame:
            break

        # Croping the frame
        crop_frame = frame[y:y+h, x:x+w]

        # Percentage
        xx = cnt *100/frames
        print(int(xx),'%')

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