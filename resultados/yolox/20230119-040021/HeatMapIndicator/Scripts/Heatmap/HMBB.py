import cv2
import numpy as np

def detect_bbox(percent,image,heatmap, path_resultados, case):
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
    result_overlay = cv2.addWeighted(background, 0.7, heatmap, 0.7, 0)
    #Guardo el mapa de calor
    cv2.imwrite(path_resultados + "/Heatmap{0}{1}.jpg".format(percent,case), result_overlay)
    with open(path_resultados + "/result{0}.txt".format(case), "a") as file:
        file.write("Box {0}: ({1},{2}), ({3},{4}), ({5},{6}), ({7},{8}) \n".format(percent,x,y,x+w,y,x+w,y+h,x,y+h))
    return heatmap



def heatmap_creator(background, bboxs_stack, cant_frames, alpha, path_resultados, case):
    n_frames = len(bboxs_stack)
    factor = 1 / cant_frames
    stack = None
    h, w = background.shape[:2]
    for i in range(n_frames):
        temp_canvas = create_canvas(w, h, bboxs_stack[i])
        if stack is None:
            stack = factor*temp_canvas
        else:
            stack = stack + factor * temp_canvas
    norm_stack = min_max_normalization(stack)

    #cv2.imshow("first",norm_stack)
    map_norm_stack = cv2.applyColorMap(norm_stack, cv2.COLORMAP_JET)
    cv2.imwrite(path_resultados + '/Heatmap{0}.jpg'.format(case), map_norm_stack)
    
    result = cv2.addWeighted(background, 0.7, map_norm_stack, 0.7, 0)
    #Guardo imagen final
    cv2.imwrite(path_resultados + '/HMs{0}.jpg'.format(case), result)
    #cv2.imshow("preview",map_norm_stack)
    b, g, r = cv2.split(map_norm_stack)
    t, b = cv2.threshold(b, 128, 255, cv2.THRESH_BINARY)
    map_norm_stack = cv2.merge((b, g, r))
    #cv2.imshow("preview2",map_norm_stack)
    #bbox_concurrido(norm_stack, background)
    #Convierto la imagen a HSV
    hsv_img = cv2.cvtColor(norm_stack, cv2.COLOR_BGR2HSV)
    salida = detect_bbox(0.9,hsv_img,map_norm_stack, path_resultados, case)
    salida = detect_bbox(0.8,hsv_img,map_norm_stack, path_resultados, case)
    salida = detect_bbox(0.7,hsv_img,map_norm_stack, path_resultados, case)
    salida = detect_bbox(0.6,hsv_img,map_norm_stack, path_resultados, case)
    salida = detect_bbox(0.5,hsv_img,map_norm_stack, path_resultados, case)
    salida = detect_bbox(0.4,hsv_img,map_norm_stack, path_resultados, case)
    salida = detect_bbox(0.3,hsv_img,map_norm_stack, path_resultados, case)
    salida = detect_bbox(0.2,hsv_img,map_norm_stack, path_resultados, case)
    salida = detect_bbox(0.1,hsv_img,map_norm_stack, path_resultados, case)



    return cv2.addWeighted(background, alpha, map_norm_stack, 1-alpha, 0)

def create_canvas(w_img, h_img, bboxs,  channels=3):
    canvas = np.zeros((h_img, w_img, channels), dtype=np.uint8)
    for bbox in bboxs:
        x, y, w, h = bbox
        cv2.rectangle(canvas, (x, y), (x+w, y+h), (255, 255, 255), -1)
    return canvas.astype(np.uint16)

def min_max_normalization(input_array):
    if input_array.max() > 0:
        temp = input_array / input_array.max()
        temp = np.floor(temp * 255)
        return temp.astype(np.uint8)
    else:
        return input_array.astype(np.uint8)

def bbox_generator(file):
    bboxs = []

    fl = open(file, 'r')
    data = fl.readlines()
    fl.close()
    cant_frames = 0
    for dt in data:
        # Split string to floats
        frame,_, x, y, w, h, z1, z2, z3 = map(float, dt.split(','))
        x = int(x)
        y = int(y)
        w = int(w)
        h = int(h)

        bboxs.append([x, y, w, h])
    return bboxs, frame

def create_heatmap(background, file, path_out, case):
    h, w = background.shape[:2]
    bboxs_stack = []
    frames = []
    fl = open(file, 'r')
    data = fl.readlines()
    fl.close()
    for dt in data:
        # Split string to floats
        frame,_, x, y, w, h, accuracy, z1, z2, z3 = map(float, dt.split(','))
        x = int(x)
        y = int(y)
        w = int(w)
        h = int(h)
        frame = int(frame)

        #frames.append([frame])
        bboxs_stack.append([frame,x, y, w, h])


    frame_anterior=1
    bbox_heatmap = []
    bboxs = []
    for boundingbox in bboxs_stack:
        bbarray = np.array(boundingbox)
        frame = bbarray[0]
        if frame_anterior == frame: 
            bboxs.append([bbarray[1], bbarray[2], bbarray[3], bbarray[4]])
        else:
            frame_anterior = frame
            bbox_heatmap.append(bboxs)
            bboxs = []
            bboxs.append([bbarray[1], bbarray[2], bbarray[3], bbarray[4]])

    heatmap = heatmap_creator(background, bbox_heatmap, frame, 0.55, path_out, case)
    cv2.imwrite(path_out + "/HeatMap{0}.jpg".format(case), heatmap)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", required=True, help="Path de resultados")
    ap.add_argument("-i", "--input", required=True, help="Path to input")
    args = vars(ap.parse_args())

    input = args["input"]
    background = cv2.imread(input + "background.jpg")
    path = args["path"]

    file = input + 'gt.txt'
    create_heatmap(background, file, path,'gt')
    file2 = input + 'detection.txt'
    create_heatmap(background, file2, path,'detection')

