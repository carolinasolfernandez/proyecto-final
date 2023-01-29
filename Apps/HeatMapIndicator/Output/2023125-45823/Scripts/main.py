from datetime import datetime
import os
import shutil

def bbox_generator(file):
    fl = open(file, 'r')
    data = fl.readlines()
    fl.close()
    for dt in data:
        # Split string to floats
        x_min, y_min, x_max, y_max = map(float, dt.split(','))
        x_min = int(x_min)
        y_min = int(y_min)
        x_max = int(x_max)
        y_max = int(y_max)
        bbox = [x_min, y_min, x_max, y_max]
    return bbox
    
def IOU(box1, box2):
    x1, y1, x2, y2 = box1
    x3, y3, x4, y4 = box2
    x_inter1 = max(x1, x3)
    y_inter1 = max(y1, y3)
    x_inter2 = min(x2, x4)
    y_inter2 = min(y2, y4)
    width_inter = abs(x_inter2 - x_inter1)
    height_inter = abs(y_inter2 - y_inter1)
    area_inter = width_inter * height_inter
    width_box1 = abs(x2 - x1)
    height_box1 = abs(y2 - y1)
    width_box2 = abs(x4 - x3)
    height_box2 = abs(y4 - y3)
    area_box1 = width_box1 * height_box1
    area_box2 = width_box2 * height_box2
    area_union = area_box1 + area_box2 - area_inter
    iou = area_inter / area_union
    return iou

def create_folder():
    a = datetime.now()
    # Directory
    directory = str(a.year) + str(a.month) + str(a.day) + "-" + str(a.hour) + str(a.minute) + str(a.second)
    # Parent Directory path
    parent_dir = os.getcwd() + '\Output'
    # Path
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)
    
    return path

if __name__ == "__main__":
    path = create_folder()
    input = "Input/"
    os.system('python Heatmap/HM.py -p {} -v {}'.format(path, input))
    os.system('python Heatmap/HMBB.py -p {} -i {}'.format(path, input))
    
    box_1 = bbox_generator(path + '/resultdetection.txt')
    box_2 = bbox_generator(path + '/resultgt.txt')

    value = IOU(box_1, box_2)

    print('IoUH = {}'.format(value))

    with open(path + "/IoUBB.txt", 'w') as file:
        file.write("{0}".format(value))

    directory = 'Scripts'
    parent_dir = path
    scripts =  os.path.join(parent_dir, directory)
    os.mkdir(scripts)
    
    shutil.copyfile("main.py", scripts + "/main.py")
    shutil.copytree("Heatmap", scripts + "/Heatmap")
    shutil.copytree("Input", scripts + "/Input")

