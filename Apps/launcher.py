import cv2
import tkinter as tk
from tkinter import filedialog
import os.path
from pathlib import Path

class Cropper:
    def __init__(self):
        self.root = tk.Tk()
        #Saco la ventana de dialogo del Tkinter
        self.root.withdraw()

        #Tomo información de la pantalla para poder dimensionar la ventana, no está funcionando muy bien
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        #Abro ventana para seleccionar el archivo a procesar
        self.videofile = filedialog.askopenfilename()

        #Se abre el video para empezar a leer
        self.cap = cv2.VideoCapture(self.videofile)

        #Se chequea si el video se abrió bien
        if (self.cap.isOpened() == False):
          print("No se puede leer el archivo!")
          exit()

        while(self.cap.isOpened()):
            #Tomo primer frame del video
            self.ret, self.frame = self.cap.read()
            break
        # Libero el objeto capturado para asegurar comenzar con el primer frame
        self.cap.release()

        #Parametros para realizar el corte
        self.cropping = False
        self.x_start, self.y_start, self.x_end, self.y_end = 0, 0, 0, 0
        self.oriImage = self.frame.copy()

        #Preparo la ventana y la ubico en el centro de la pantalla
        cv2.namedWindow("Seleccionar ROI-->Presionar Q para finalizar", cv2.WINDOW_NORMAL)
        cv2.setMouseCallback("Seleccionar ROI-->Presionar Q para finalizar", self.mouse_crop)
        cv2.resizeWindow('Seleccionar ROI-->Presionar Q para finalizar', self.frame.shape[1], self.frame.shape[0])
        self.x_pos = round(self.screen_width/2) - round(self.frame.shape[1]/2)
        self.y_pos = round(self.screen_height/2) - round(self.frame.shape[0]/2)
        #Mueve mal la ventana, la deja en cualquier lado 
        #cv2.moveWindow("Seleccionar ROI-->Presionar Q para finalizar", self.x_pos, self.y_pos)

        #Muestro el primer frame y permito la selección rectangular, espero Q para confirmar.
        while True:
            i = self.frame.copy()
            if not self.cropping:
                cv2.imshow("Seleccionar ROI-->Presionar Q para finalizar", self.frame)
                if (self.x_start + self.y_start + self.x_end + self.y_end) > 0:
                    cv2.rectangle(i, (self.x_start, self.y_start), (self.x_end, self.y_end), (255, 0, 0), 2)
                    cv2.imshow("Seleccionar ROI-->Presionar Q para finalizar", i)

            elif self.cropping:
                cv2.rectangle(i, (self.x_start, self.y_start), (self.x_end, self.y_end), (255, 0, 0), 2)
                cv2.imshow("Seleccionar ROI-->Presionar Q para finalizar", i)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

        #Ya tengo los parámetros para hacer el corte.
        #print(x_start, y_start, x_end, y_end)

        #Realizo un corte del video original, image[y:y+h, x:x+w]
        self.cropped = self.oriImage[self.y_start:self.y_end, self.x_start:self.x_end]
        #Realizo un corte del video original, image[y:y+h, x:x+w]
        self.fgmask = self.oriImage[self.y_start:self.y_end, self.x_start:self.x_end]

        # #Ver el resultado 
        # cv2.namedWindow('ROI', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('ROI', self.cropped.shape[1], self.cropped.shape[0])
        # self.x_pos = round(self.screen_width/2) - round(self.cropped.shape[1]/2)
        # self.y_pos = round(self.screen_height/2) - round(self.cropped.shape[0]/2)
        # cv2.moveWindow("ROI", self.x_pos, self.y_pos)
        # cv2.imshow("ROI", self.cropped)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        #Recorto el video con los mismos parametros de recorte
        self.cap = cv2.VideoCapture(self.videofile)

        #Guardo el archivo en el mismo directorio con sufijo _Procesado
        self.newFileName = os.path.join(str(Path(self.videofile).parents[0]), str(Path(self.videofile).stem) +'_Procesado.avi')
        self.newFileName2 = os.path.join(str(Path(self.videofile).parents[0]), str(Path(self.videofile).stem) +'_ProcesadoMOG2.avi')
        self.frame_width = self.x_end - self.x_start
        self.frame_height = self.y_end - self.y_start

        #Se toma info de los fps del archivo si es posible
        self.fps = int(round(self.cap.get(5)))
        #Verifico si obtuvimos un valor, de lo contrario impongo 30 fps; es posible que deba cambiar esto o que sea MUY IMPORTANTE
        # # # MUY IMPORTANTE EL VALOR DE FPS IMPUESTO
        if self.fps == 0:
            self.fps = 30 #A mayor valor menor velocidad

        #Creo el objeto VideoWriter y defino el codec
        self.out = cv2.VideoWriter(self.newFileName, cv2.VideoWriter_fourcc('M','J','P','G'), self.fps, (self.frame_width,self.frame_height))

        #Creo el objeto para MOG2
        self.fgbg = cv2.createBackgroundSubtractorMOG2()
        self.out2 = cv2.VideoWriter(self.newFileName2, cv2.VideoWriter_fourcc('M','J','P','G'), self.fps, (self.frame_width,self.frame_height), isColor=False)

        #Leo frame por frame
        while(True):
            self.ret, self.frame = self.cap.read()
            if self.ret:
                #Recorto el frame
                self.cropped = self.frame[self.y_start:self.y_end, self.x_start:self.x_end]
                #Escribo el frame en el video de salida
                self.out.write(self.cropped)

                #Escribo el frame en el video de salida de MOG2
                self.fgmask = self.fgbg.apply(self.cropped)
                self.out2.write(self.fgmask)

                #Muestro el frame resultante - No puedo mover la ventana, a veces funciona
                cv2.namedWindow('Procesando video', cv2.WINDOW_NORMAL)
                cv2.resizeWindow('Procesando video', self.cropped.shape[1], self.cropped.shape[0])
                x_pos = round(self.screen_width/2) - round(self.cropped.shape[1]/2)
                y_pos = round(self.screen_height/2) - round(self.cropped.shape[0]/2)
                cv2.moveWindow("Procesando video", self.x_pos,self.y_pos)
                cv2.imshow('Procesando video',self.cropped)
                #Muestro el frame resultante - No puedo mover la ventana, a veces funciona
                cv2.namedWindow('Procesando video MOG2', cv2.WINDOW_NORMAL)
                cv2.resizeWindow('Procesando video MOG2', self.fgmask.shape[1], self.fgmask.shape[0])
                x_pos = round(self.screen_width/2) - round(self.fgmask.shape[1]/2)
                y_pos = round(self.screen_height/2) - round(self.fgmask.shape[0]/2)
                cv2.moveWindow("Procesando video MOG2", self.x_pos,self.y_pos)
                cv2.imshow('Procesando video MOG2',self.fgmask)

                # Si presiona Q corta el procesamiento
                if cv2.waitKey(1) & 0xFF == ord('q'):
                  break

        # Termina el loop
            else:
                break

        #Cuando se termina todo, libero el objeto de video capturado y el escrito
        self.cap.release()
        self.out.release()

        #Cierro todas las ventanas
        cv2.destroyAllWindows()

        #Mensaje que finalizó con éxito
        print("Video procesado: ", self.newFileName)

    def mouse_crop(self, event, x, y, flags, param):
        # Si el click izquierdo esta presionado, empieza a grabar coordenadas
        # (x, y) que indican el área de interés para recortar.
        if event == cv2.EVENT_LBUTTONDOWN:
            self.x_start, self.y_start, self.x_end, self.y_end = x, y, x, y
            self.cropping = True

        # Mouse en movimiento
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.cropping:
                self.x_end, self.y_end = x, y

        # Suelta click izquierdo
        elif event == cv2.EVENT_LBUTTONUP:
            # Guardo las coordenadas (x, y) 
            self.x_end, self.y_end = x, y
            self.cropping = False # Finalizó el recorte

if __name__ == "__main__":
    app = Cropper()
