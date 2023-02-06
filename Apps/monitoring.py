# primer arg es el archivo a escribir el monitoreo
# segundo arg es el script the ailia
# python monitoring.py stats.txt ../ailia-models/object_detection/yolox/yolox.py --video ../../../data/videos/59.mp4 --savepath ../as.mp4 --env_id=2
import os
import sys
import psutil
import time
import subprocess
from time import sleep


# get the script to execute and target file
target_file = sys.argv[1]
script_file = sys.argv[2]
script_args = sys.argv[3:]

# change to the directory of the script
script_directory = os.path.dirname(script_file)
os.chdir(script_directory)

#main_process = psutil.Process(os.getpid())
psutil.cpu_percent()
# get the start time
start_time = time.time()
# start your process
process= subprocess.Popen(["python", os.path.basename(script_file)] + script_args)
pid2=process.pid

sub_process = psutil.Process(pid2)
cpu_2=sub_process.cpu_percent()

time.sleep(100)

memory_utilization_sub_process_Mb = sub_process.memory_info().vms /(1024**2)
cpu_1_end=psutil.cpu_percent()
cpu_2_end=sub_process.cpu_percent()

# wait for the process to complete
process.wait()

# get the total time elapsed
time_elapsed = time.time() - start_time

print(  "GPU utilization [%]: " + str(cpu_2_end) + "\n" +
        "CPU utilization [%]: " + str(cpu_1_end) + "\n" +
        "Memory utilization Mb: " + str(memory_utilization_sub_process_Mb) + "\n" + 
        "Time elapsed: " + str(time_elapsed) + " seconds\n")


# write the results to a file
with open(target_file, "w") as file:
    file.write("GPU utilization [%]: " + str(cpu_2_end) + "\n")
    file.write("CPU utilization [%]: " + str(cpu_1_end) + "\n")
    file.write("Memory utilization [Mb]: " + str(memory_utilization_sub_process_Mb) + "\n")
    file.write("Time elapsed [s]: " + str(time_elapsed) + "\n")