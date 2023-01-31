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


videoName="$(basename "$inVideo" | sed 's/\(.*\)\..*/\1/')"

# Muevo los resultados a la carpeta resultados/modelo/fecha
resDir=$root/resultados/$model/$dateName
mkdir -p $resDir
mv $cwd/$outVideo $resDir/$videoName-out.mp4

#cp $cwd/$inVideo $resDir/
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


# Copio archivos necesario para HeatMapIndicator
cp $cwd/$gt $root/Apps/HeatMapIndicator/Input/gt.txt
cp $resDir/$dateName-out.txt $root/Apps/HeatMapIndicator/Input/detection.txt
cp $cwd/$inVideo $root/Apps/HeatMapIndicator/Input/input.mp4

echo "ejecutando mapa de calor ...."
# Ejecuta Mapa de calor
cd $root/Apps/HeatMapIndicator
python main.py -d $dateName
mv $root/Apps/HeatMapIndicator/Output/$dateName $resDir/HeatMapIndicator


echo "rellenando el csv de resultados ..."
echo "fecha, algoritmo, video, TE: HOTA, TE: DetA, TE: AssA, TE: DetRe, TE: DetPr, TE: AssRe, TE: AssPr, TE: LocA, TE: IDF1, TE: IDR, TE: IDP, TE: IDTP, TE: IDFN, TE: IDFP, TE: SFDA, TE: ATA, MP: F1 Score Detecciones, MP: Precision Detecciones, MP: Recall Detecciones, MP: Max Personas Detectadas/Esperadas, HM: Error[%], Carpeta" >> $resDir/resultados.csv

te=($(sed -n 2p $resDir/pedestrian_summary.txt))
mp1=($(sed -n 1p $resDir/metrics.txt))
mp2=($(sed -n 2p $resDir/metrics.txt))
mp3=($(sed -n 3p $resDir/metrics.txt))
mp4=($(sed -n 11p $resDir/metrics.txt))
hm=($(sed -n 1p $resDir/HeatMapIndicator/IoUBB.txt))
line="$dateName, $modelDir, $inVideo, ${te[0]}, ${te[1]}, ${te[2]}, ${te[3]}, ${te[4]}, ${te[5]}, ${te[6]}, ${te[7]}, ${te[29]}, ${te[30]}, ${te[31]}, ${te[32]}, ${te[33]}, ${te[34]}, ${te[39]}, ${te[40]}, ${mp1[3]}, ${mp2[2]}, ${mp3[2]}, ${mp4[6]}/${mp4[9]}, ${hm[0]}, ../resultados/$model/$dateName"

echo $line >> $resDir/resultados.csv

echo $line >> $root/resultados/resultados.csv

echo "Los resultados se encuentran en la carpeta $resDir"