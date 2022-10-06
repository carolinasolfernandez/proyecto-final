import tensorflow
from keras import models
from keras import layers
try:
    import tkinter as tk  # using Python 3
    from tkinter import filedialog as fd
except ImportError:
    import Tkinter as tk  # falls back to import from Python 2
    from Tkinter import filedialog as fd
import cv2
from PIL import ImageTk as itk
from PIL import Image

#https://stackoverflow.com/questions/68189294/how-to-display-the-video-in-tkinter-canvas-frame-by-frame

window = tk.Tk()
print("Hello sunshine")

class window_tk():
    def __init__(self, main):
        self.canvas = tk.Canvas(main, bg='white')
        self.init_img_route = '/home/diegoas/Documents/ProyectoFinal/Documentos/poligonales_lib.png'
        self.image = itk.PhotoImage(file=self.init_img_route)
        self.bg= self.canvas.create_image(0,0,anchor = tk.NW,image=self.image)
        self.vid = None
    def load_video(self):
        self.foldername = fd.askopenfilename(parent=window,initialdir="C:/",title='Select a video file to load.',filetypes=[('video files','*.wmv *.mp4 *.mov *.avi')])
        self.current_pic_num=0
        try:
            self.vid = cv2.VideoCapture(self.foldername)
            frame_number =0
            print(self.vid,self.vid.isOpened())
            self.frame_count = 0
            if self.vid.isOpened():
                vid_w = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
                vid_h = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
                vid_f = self.vid.get(cv2.CAP_PROP_FPS)
                ret,frame = self.vid.read()
                #cv2.imshow('frame',frame)
                frame_convert = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                #print(self.frame_count, vid_w,vid_h,vid_f,frame.shape)
                self.image = itk.PhotoImage(Image.fromarray(frame_convert))
                self.canvas.itemconfig(self.bg, image = self.image)
                self.canvas.pack(fill='both',expand=1)

    #            frame_number+=1
        except IndexError:
            pass

new_window = window_tk(window)
new_window.load_video()
train_labels = []
train_samples = []

for i in range(50):
    frame_1 = ''
    train_samples.append(frame_1)   #contain frames
    train_labels.append(1)  # contain amount of people detected
    frame_2 = ''
    train_samples.append(frame_2)
    train_labels.append(2)

    #We need to normalize or standarize the data so that when we train the neural network, said process is quicker or more efficient

print("Bye sunshine")

# https://deeplizard.com/learn/video/gZmobeGL0Yg

# #https://medium.com/@zahraelhamraoui1997/fundamentals-of-deep-learning-93ea5604fce0
# network = models.Sequential()
# network.add(layers.Dense(512, activation='relu', input_shape=(28 * 28,)))   #Dense layer(desnley/fully connected neural layer)
# network.add(layers.Dense(10, activation='softmax')) #10-way softmax layer that returns an array of 10 probability scores(that sum to 1)
# network.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
