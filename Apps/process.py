def process_file(filename):
    objects = {}
    with open(filename) as f:
        for line in f:
            frame, obj_id, x, y, width, height, probability, x1,y1,z1 = line.split(',')
            obj_id = int(obj_id)
            x, y, width, height, probability = float(x), float(y), float(width), float(height), float(probability)

            if obj_id not in objects:
                objects[obj_id] = {'x': [x], 'y': [y], 'width': [width], 'height': [height], 'probability': [probability], 'frames': 1}
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
        if obj['frames'] < 50 and sum(obj['probability']) / obj['frames'] < 0.5 and obj['x'][0] > 10 and obj['x'][0] + obj['width'][0] < 1270 \
        and obj['y'][0] > 10 and obj['y'][0] + obj['height'][0] < 710:
            result.append(obj_id)

    return result

def filter_file(filename, output_filename):
    ids_to_filter = set(process_file(filename))
    with open(filename) as f_in, open(output_filename, "w") as f_out:
        for line in f_in:
            frame, obj_id, x, y, width, height, probability, x1,y1,z1 = line.split(',')
            obj_id = int(obj_id)
            if obj_id not in ids_to_filter:
                f_out.write(line)

filter_file("../resultados/siam-mot/large1/20230130-031631/20230130-031631-out.txt", "filtered_file.txt")