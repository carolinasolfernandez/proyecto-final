#! usr/bin/bash

# sh pipeline.sh -i ../data/videos/59.mp4 -g ../data/gt/59.txt -m object_detection/yolox

envID=2 #index de GPU. Ver en el luncher, el index de la unidad

#modelDir=object_detection/yolox
#modelDir=object_tracking/siam-mot
#inVideo='../data/videos/59.mp4'
#gt='../data/gt/59.txt'

dateName="$(date +%Y%m%d-%H%M%S)"
outVideo=$dateName.mp4

echo 'El video se puede cancelar con la tecla Q'

cwd=$(pwd)
root=$(pwd)/..

while getopts m:i:e:g: flag
do
    case "${flag}" in
        m) modelDir=${OPTARG};;
        i) inVideo=${OPTARG};;
        e) envID=${OPTARG};;
        g) gt=${OPTARG};;
    esac
done

: ${modelDir:?Falta -m <modelDir>} ${inVideo:?Falta -i <inVideo.mp4>} ${gt:?Falta -g <gt.txt>}


# Corre modelo
ailiaDir=$root/ailia-models
rm -f -- $ailiaDir/output.txt
cd $ailiaDir/$modelDir
model="$(basename -- $modelDir)"
python $model.py --video $cwd/$inVideo --savepath $cwd/$outVideo --env_id $envID --benchmark_count 5

# Muevo los resultados a la carpeta resultados/modelo/fecha
resDir=$root/resultados/$model/$dateName
mkdir -p $resDir
mv $cwd/$outVideo $resDir/$dateName-out.mp4
cp $cwd/$inVideo $resDir/
mv $ailiaDir/output.txt $resDir/$dateName-out.txt

# Copia dataset y GT a TrackEval
evalDirGT=$root/TrackEval/data/gt/mot_challenge/PF-train/PF-01/gt
evalDirData=$root/TrackEval/data/trackers/mot_challenge/PF-train/data
cp $cwd/$gt $evalDirGT/gt.txt
cp $resDir/$dateName-out.txt $evalDirData/data/PF-01.txt

# Ejecuta TrackEval
cd $root/TrackEval/scripts
python run_mot_challenge.py --BENCHMARK PF --DO_PREPROC False

# Copia resultados de TrackEval a Resultados
cp $evalDirData/pedestrian_detailed.csv $resDir/
cp $evalDirData/pedestrian_plot.png $resDir/
cp $evalDirData/pedestrian_summary.txt $resDir/
cp $cwd/$gt  $resDir/gt.txt

# Ejecuta Metricas de Negocio
cd $root/Apps
python metrics.py -d $resDir/$dateName-out.txt -g $resDir/gt.txt -o $resDir

echo "Los resultados se encuentran en la carpeta $resDir"