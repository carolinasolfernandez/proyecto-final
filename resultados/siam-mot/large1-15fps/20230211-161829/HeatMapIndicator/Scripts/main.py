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
    
def IOU(box_d, box_gt):
    dx1, dy1, dx2, dy2 = box_d
    gx1, gy1, gx2, gy2 = box_gt

    x1 = max(dx1, gx1)
    y1 = max(dy1, gy1)
    x2 = min(dx2, gx2)
    y2 = min(dy2, gy2)

    # Calculate the area of intersection
    intersection = max(0, x2 - x1) * max(0, y2 - y1)

    # Calculate the area of union
    gt_area = abs((gx2 - gx1) * (gy2 - gy1))
    det_area = abs((dx2 - dx1) * (dy2 - dy1))
    union = gt_area + det_area - intersection

    # Calculate the IoU
    return intersection / union

def create_folder(date):
    #a = datetime.now()

    # Directory
    #directory = str(a.year) + str(a.month) + str(a.day) + "-" + str(a.hour) + str(a.minute) + str(a.second)
    # Parent Directory path
    directory = date
    parent_dir = os.getcwd() + '\Output'
    # Path
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)
    
    return path

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--date", required=True, help="DateTime")
    args = vars(ap.parse_args())

    date = args["date"]
    path = create_folder(date)
    input = "Input/"
    os.system('python Heatmap/HM.py -p {} -v {}'.format(path, input))
    os.system('python Heatmap/HMBB.py -p {} -i {}'.format(path, input))
    
    box_d = bbox_generator(path + '/resultdetection.txt')
    box_gt = bbox_generator(path + '/resultgt.txt')

    value = IOU(box_d, box_gt)

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

