from datetime import datetime
import os
import shutil

def create_folder():
    a = datetime.now()
    # Directory
    directory = str(a.year) + str(a.month) + str(a.day)  + str(a.hour) + str(a.minute) + str(a.second)
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
    
    directory = 'Scripts'
    parent_dir = path
    scripts =  os.path.join(parent_dir, directory)
    os.mkdir(scripts)

    shutil.copyfile("main.py", scripts + "/main.py")
    shutil.copytree("Heatmap", scripts + "/Heatmap")
    shutil.copytree("Input", scripts + "/Input")