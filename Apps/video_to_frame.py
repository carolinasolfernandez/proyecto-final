import cv2

'''
Convierte un video a frames
'''

video = '../data/videos/large1.mp4'
name = './large1/'
vidcap = cv2.VideoCapture(video)


success,image = vidcap.read()
count = 0
while success:
  cv2.imwrite(name+"%d.jpg" % count, image)     # save frame as JPEG file      
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1