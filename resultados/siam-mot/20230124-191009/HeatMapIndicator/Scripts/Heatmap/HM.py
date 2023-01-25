import numpy as np
import cv2
import copy
from PIL import Image
from progress.bar import Bar
from datetime import datetime
import os


def detect_bbox(percent,image,heatmap, path_resultados):
    #Seteo rango de valores para tomar la parte mas concurrida.
    lower_hsv = np.array([0,0,int(percent*255)]) 
    higher_hsv = np.array([0,0,255])
    #Filtro pixeles que esten fuera del rango
    mask = cv2.inRange(image, lower_hsv, higher_hsv)
    #Detecto contorno de imagen binaria con cv2.CHAIN_APPROX_NONE
    contours, hierarchy = cv2.findContours(image=mask, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    #Dibujo los contornos en la imagen original
    image_copy1 = mask.copy()
    cv2.drawContours(image=image_copy1, contours=contours, contourIdx=-1, color=(0, 0, 255), thickness=3, lineType=cv2.LINE_AA)
    #Me quedo con el contorno mas grande que detecto
    c = max(contours, key = cv2.contourArea)
    #Tomo tamaño del bounding box sobre ese contorno
    x,y,w,h = cv2.boundingRect(c)
    #Dibujo el contorno mas grande con su bounding box calculado
    cv2.rectangle(heatmap,(x,y),(x+w,y+h),(255, 255, 255),2)
    #Guardo el mapa de calor
    cv2.imwrite(path_resultados + "/Heatmap{0}.jpg".format(percent), heatmap)
    with open(path_resultados + '/result.txt', "a") as file:
        file.write("Box {0}: ({1},{2}), ({3},{4}), ({5},{6}), ({7},{8}) \n".format(percent,x,y,x+w,y,x+w,y+h,x,y+h))
    return heatmap


def main(video_in, path_resultados):
    input_video = cv2.VideoCapture(video_in)
    #Preparo función que remueve el fondo
    background_subtractor = cv2.bgsegm.createBackgroundSubtractorMOG()
    #Calculo la longitud de frames
    length = int(input_video.get(cv2.CAP_PROP_FRAME_COUNT))
    #Barra de progreso visual
    bar = Bar('Procesando frames del video', max=length)
    #Flag de primer frame
    first_iteration_indicator = 1
    #Recorro cada frame
    for i in range(0, length):
        #Leo el frame
        ret, frame = input_video.read()
        #Si es el primer frame
        if first_iteration_indicator == 1:
            #Me guardo el primer frame
            first_frame = copy.deepcopy(frame)
            #Conservo la resolución. Por ej: 1070x720
            height, width = frame.shape[:2]
            #Inicializo la imagen acumulada como una imagen toda negra
            accum_image = np.zeros((height, width), float)
            #Bajo el flag
            first_iteration_indicator = 0
        #Resto de frames
        else:
            #Aplico la remoción de fondo
            filter = background_subtractor.apply(frame) 
            #Convierto en Array
            pil_image = Image.fromarray(filter)
            frame = np.array(pil_image.convert('L'))
            #Seteo threshhold de bit blanco o negro, para limpiar los pixeles que no son completamente blancos o negros.
            thresh = 128
            #Comparo la imagen por el threshold para dar 1 o 0.
            frame_bool = frame > thresh
            #La paso a flotante
            frame_bool_float = frame_bool.astype(float) 
            #Filtro Threshold
            threshold = 2
            maxValue = 2
            ret, th1 = cv2.threshold(filter, threshold, maxValue, cv2.THRESH_BINARY)
            #Sumo la mask a la suma de masks
            accum_image = accum_image + frame_bool_float
            #Espero q para salir del proceso
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        bar.next()

    bar.finish()
    #Convierto imagen a float
    accum_image = accum_image.astype(float) 
    #Divido por el mayor pixel y dejo el array en valores grayscale 0.00-1.00
    accum_image = np.divide(accum_image, np.amax(accum_image))
    #Convierto el array en valores 0-255 para utilizarlo con cv2
    uint_img = np.array(accum_image*255).astype('uint8')
    #Paso la imagen de valores grayscale a bgr, sigue siendo grayscale pero en formato BGR (Blue-Green-Red)
    grayImage = cv2.cvtColor(uint_img, cv2.COLOR_GRAY2BGR)
    #Aplico mapa de calor estilo JET (Azul-Celeste-Verde-Amarillo-Naranja-Rojo)
    color_image = cv2.applyColorMap(grayImage, cv2.COLORMAP_JET)
    #Sumo la mask al primer frame para la imagen final
    result_overlay = cv2.addWeighted(first_frame, 0.7, color_image, 0.7, 0)
    #Guardo el mapa de calor
    cv2.imwrite(path_resultados + '/HMs.jpg', result_overlay)
    #Defino el color del bounding box
    color=(255,255,255)
    #Convierto la imagen a HSV
    hsv_img = cv2.cvtColor(grayImage, cv2.COLOR_BGR2HSV)

    salida = detect_bbox(0.9,hsv_img,result_overlay, path_resultados)

    #Guardo imagen final
    cv2.imwrite(path_resultados + '/Heatmap.jpg', salida)
    result_overlay = cv2.addWeighted(first_frame, 0.7, color_image, 0.7, 0)
    
    #Cleanup
    input_video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", required=True, help="Path de resultados")
    ap.add_argument("-v", "--video", required=True, help="Path de videos")
    #ap.add_argument("-n", "--number", required=True, type=int, help="Number of frames with 'generated detections'")
    args = vars(ap.parse_args())

    path = args["path"]
    input_video = args["video"] + "input.mp4"
    main(input_video, path)

