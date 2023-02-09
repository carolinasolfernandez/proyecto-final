import argparse
import os
import subprocess

'''
Filtra de los resultados los que cumplen con todo los siguiente:
- tienen un promedio de probabillidad menor a 0.5
- no aparecen en frame 1
- aparecen en una coordenada distinta a las iniciales (dejando un margen de 5px por borde)
- aparecen en menos de 50 frames
'''

def calculate_iou(boxA, boxB):
    # Calculate the intersection area of two boxes
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[0]+boxA[2], boxB[0]+boxB[2])
    yB = min(boxA[1]+boxA[3], boxB[1]+boxB[3])

    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
 
    # Calculate the union area of two boxes
    boxAArea = (boxA[2] + 1) * (boxA[3] + 1)
    boxBArea = (boxB[2] + 1) * (boxB[3] + 1)
    unionArea = boxAArea + boxBArea - interArea
 
    # Compute the IoU
    iou = interArea / unionArea
 
    return iou

def track_objects(frames, threshold=0.5):
    objects = {}
    separations = []
    
    for frame_id, frame in enumerate(frames):
        # Check if the objects in the previous frame are still present
        disappeared_objects = []
        for obj_id, obj_info in objects.items():
            obj_present = False
            for obj in frame:
                if (obj[0] == obj_id):
                    obj_present = True
                    break
            if not obj_present:
                x, y, w, h = obj_info
                if x > 0 and y > 0 and x+w < 1280 and y+h < 720:
                    disappeared_objects.append((obj_id, obj_info))
        
        # Remove the disappeared objects from the dictionary
        for obj_id, obj_info in disappeared_objects:
            del objects[obj_id]
        
        # Assign a new ID to each newly detected object
        new_ids = []
        for obj in frame:
            obj_id = obj[0]
            x, y, w, h = obj[1:]
            new_object = True
            if x > 0 and y > 0 and x+w < 1280 and y+h < 720:
                for disappeared_id, disappeared_info in disappeared_objects:
                    ix, iy, iw, ih = disappeared_info
                    iou = calculate_iou((x, y, w, h), (ix, iy, iw, ih))
                    if iou >= threshold:
                        objects[disappeared_id] = (x, y, w, h)
                        print("-------")
                        #separations.append((disappeared_id, obj_id, frame_id, min(x,ix), min(y,iy),max(w,iw),max(h,ih)))
                        new_object = False
                        break
                if new_object:
                    new_ids.append(obj_id)
                    objects[obj_id] = (x, y, w, h)

    
        '''
        # Keep track of the frames where objects disappear
        for obj_id, obj_info in disappeared_objects:
            separations.append((frame_id, obj_id, obj_info))
        '''
    
    print(separations)
    return separations

def overlap_percentage(rect1, rect2): #rect1 over rect 2
    # Unpack the rectangles
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    
    # Calculate the coordinates of the bottom-right corners of the rectangles
    x1_br = x1 + w1
    y1_br = y1 + h1
    x2_br = x2 + w2
    y2_br = y2 + h2
    
    # Determine the overlapping area
    overlap_x1 = max(x1, x2)
    overlap_y1 = max(y1, y2)
    overlap_x2 = min(x1_br, x2_br)
    overlap_y2 = min(y1_br, y2_br)
    if overlap_x2 > overlap_x1 and overlap_y2 > overlap_y1:
        overlap_area = (overlap_x2 - overlap_x1) * (overlap_y2 - overlap_y1)
    else:
        overlap_area = 0
    
    # Calculate the total area of rectangle 1
    rect1_area = w1 * h1
    
    # Calculate the percentage of rectangle 1's area that overlaps with rectangle 2
    overlap_percentage = overlap_area / rect1_area
    
    return overlap_percentage


'''
other_objects = [obj for obj in objects.values() if obj['frame'] == frame and obj_id != obj['id']]
                for other_obj in other_objects:
                    IoU = calculate_IoU(x, y, width, height, other_obj['x'], other_obj['y'], other_obj['width'], other_obj['height'])
                    if IoU > 0.9:
                        result.append(obj_id)
                        result.append(other_obj['id'])
'''
def process_file(filename):
    objects = {}    
    data = {}
    result = []
    with open(filename) as f:
        for line in f:
            frame, obj_id, x, y, width, height, probability, x1,y1,z1 = line.split(',')
            obj_id = int(obj_id)
            frame, x, y, width, height, probability = int(frame), float(x), float(y), float(width), float(height), float(probability)

            if obj_id not in objects:
                objects[obj_id] = {'initialFrame': frame, 'lastFrame': frame, 'id': obj_id, 'x': [x], 'y': [y], 'width': [width], 'height': [height], 'probability': [probability], 'frames': 1}
            else:
                obj = objects[obj_id]
                obj['x'].append(x)
                obj['y'].append(y)
                obj['width'].append(width)
                obj['height'].append(height)
                obj['probability'].append(probability)
                obj['frames'] += 1
                obj['lastFrame'] = frame

            if frame not in data:
                data[frame] = []
            data[frame].append((obj_id, x, y, width, height))

    data2= [data[f] for f in sorted(data.keys())]
    separations = track_objects(data2)

    for obj_id, obj in objects.items():
        if obj['initialFrame'] != 1 and obj['frames'] < 50 and sum(obj['probability']) / obj['frames'] < 0.5 and obj['x'][0] > 5 and obj['x'][0] + obj['width'][0] < 1270 \
        and obj['y'][0] > 10 and obj['y'][0] + obj['height'][0] < 710:
            result.append(obj_id)
            
    return result, separations

def callCrop(video, start_frame, last_frame, x, y, w, h):
    # start your process
    process= subprocess.Popen(["python", 'crop.py'] + video+ start_frame + last_frame + x + y + w + h)
    process.wait()

    script_file =" ../ailia-models/object_detection/yolov7/yolov7.py"
    script_directory = os.path.dirname(script_file)
    os.chdir(script_directory)

    # start your process
    process= subprocess.Popen(["python", os.path.basename(script_file)] +  "--video ./out.mp4 --env_id 2")
    process.wait()


def filter_file(filename, output_filename, ids_to_filter):
    with open(filename) as f_in, open(output_filename, "w") as f_out:
        for line in f_in:
            frame, obj_id, x, y, width, height, probability, x1,y1,z1 = line.split(',')
            obj_id = int(obj_id)
            if obj_id not in ids_to_filter:
                f_out.write(line)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="The path to the input file")
    parser.add_argument("output_file", help="The path to the output file")
    parser.add_argument("video", help="The video to process")
    args = parser.parse_args()

    ids_to_filter, separations = process_file(args.input_file)
    print(separations)
    callCrop(args.video)
    filter_file(args.input_file, args.output_file, set(ids_to_filter))