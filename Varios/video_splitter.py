from moviepy.editor import VideoFileClip
import os

video_src = "/home/diegoas/Documents/ProyectoFinal/Video/Original"
video_dst = "/home/diegoas/Documents/ProyectoFinal/Video/Fractioned"
list_of_files = os.listdir(video_src)

# La lógica fue que solo existiese el archivo original, de interés, en el directorio 'video_src'
for root, dirs, files in os.walk(video_src):
	for file in files:
		list_of_files.append(os.path.join(root,file))
        # Se robó código por lo que decidimos utilizar un array y no otra variable, además entiendo que 'os.list_dir' devuelve un array
for name in list_of_files:
    print(name)
# Al tener unicamente el video de interes, va a ser el primer elemento del array
full_video = video_src + '/' + list_of_files[0]
current_duration = VideoFileClip(full_video).duration
# Se decidió dividir en 10, sin un criterio en particular
divide_into_count = 10
single_duration = current_duration/divide_into_count
video_frac = 1

while current_duration > single_duration:
    clip = VideoFileClip(full_video).subclip(current_duration-single_duration, current_duration)
    current_duration -= single_duration
    current_video = f"{video_dst}/{list_of_files[0]}-{video_frac}of{divide_into_count}.mp4"
    clip.to_videofile(current_video, codec="libx264")
    print("-----------------###-----------------")
    video_frac+=1
