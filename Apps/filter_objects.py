import argparse
import math
import numpy as np
import cv2

'''
Filtra de los resultados los que cumplen con todo los siguiente:
- tienen un promedio de probabillidad menor a 0.5
- no aparecen en frame 1
- aparecen en una coordenada distinta a las iniciales (dejando un margen de 5px por borde)
- aparecen en menos de 50 frames
O si su altura es mayor a threshold teniendo en cuenta la posicion (la persona no puede medir mas de 2 metros)
'''
# python filter_objects.py ./input.txt ./output.txt

def process_file(filename):
    objects = {}
    with open(filename) as f:
        for line in f:
            frame, obj_id, x, y, width, height, probability, x1,y1,z1 = line.split(',')
            obj_id = int(obj_id)
            frame, x, y, width, height, probability = int(frame), float(x), float(y), float(width), float(height), float(probability)

            if obj_id not in objects:
                objects[obj_id] = {'frame': frame, 'x': [x], 'y': [y], 'width': [width], 'height': [height], 'probability': [probability], 'frames': 1}
            else:
                obj = objects[obj_id]
                obj['x'].append(x)
                obj['y'].append(y)
                obj['width'].append(width)
                obj['height'].append(height)
                obj['probability'].append(probability)
                obj['frames'] += 1

    result = []
    for obj_id, obj in objects.items():
        if obj['frame'] != 1 and obj['frames'] < 50 and sum(obj['probability']) / obj['frames'] < 0.5 and obj['x'][0] > 5 and obj['x'][0] + obj['width'][0] < 1270 \
        and obj['y'][0] > 10 and obj['y'][0] + obj['height'][0] < 710:
            result.append(obj_id)

    return result

def filter_file(filename, output_filename):
    ids_to_filter = set(process_file(filename))
    with open(filename) as f_in, open(output_filename, "w") as f_out:
        for line in f_in:
            frame, obj_id, x, y, width, height, probability, x1,y1,z1 = line.split(',')
            obj_id = int(obj_id)
            if float(x) < 0:
                x = str(0)
            if float(y) < 0:
                y = str(0)
            if obj_id not in ids_to_filter and float(height) < 510:
                f_out.write(line)


def person_height(x1, y1, x2, y2, cam_y_axis_x, cam_y_axis_y):
    camera_height = 2.6
    field_of_view = 60
    width_img = 1280
    height_img = 720
    person_height_pixels = y2 - y1
    y_center_person = (y1 + y2) / 2
    x_center_person = (x1 + x2) / 2
    angle_degrees = math.degrees(math.atan2(cam_y_axis_y - y1, cam_y_axis_x - x_center_person))
    #angle_degrees = (height_img / 2 - y1) * field_of_view / height_img
    distance_to_person = camera_height / math.tan(math.radians(angle_degrees))
    person_height_meters = person_height_pixels * distance_to_person * math.tan(math.radians(field_of_view / height_img)) / height_img
    return person_height_meters

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="The path to the input file")
    parser.add_argument("output_file", help="The path to the output file")
    args = parser.parse_args()

    filter_file(args.input_file, args.output_file)