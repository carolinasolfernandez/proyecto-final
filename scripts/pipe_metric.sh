#! usr/bin/bash

root=$(pwd)/..
cwd=$(pwd)
gt=$root/data/gt/large1.txt
file=$root/Apps/filtered_file.txt

# Copia dataset y GT a TrackEval
evalDirGT=$root/TrackEval/data/gt/mot_challenge/PF-train/PF-01/gt
evalDirData=$root/TrackEval/data/trackers/mot_challenge/PF-train/data
cp $gt $evalDirGT/gt.txt
cp $file $evalDirData/data/PF-01.txt

# Ejecuta TrackEval
cd $root/TrackEval/scripts
python run_mot_challenge.py --BENCHMARK PF --DO_PREPROC False

# Ejecuta Metricas de Negocio
cd $root/Apps
python metrics.py -d $file -g $gt