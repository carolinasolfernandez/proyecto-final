#! usr/bin/bash

# sh pipeline.sh -i ../data/videos/59.mp4 -g ../data/gt/59.txt -m object_detection/yolox

envID=2 #index de GPU. Ver en el luncher, el index de la unidad
monitor=1


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


ailiaDir=$root/ailia-models
rm -f -- $ailiaDir/output.txt
model="$(basename -- $modelDir)"
videoName="$(basename "$inVideo" | sed 's/\(.*\)\..*/\1/')"

#Creo carpeta de resultados
resDir=$root/resultados/$model/$videoName/$dateName
mkdir -p $resDir


stats_gpu=-1
stats_cpu=-1
stats_mem=-1
stats_time=-1

if [ $monitor -eq 1 ]
then
    # Corro modelo con stats --- Comentar estas lineas hasta el espacio y descomentar las dos de arriba
    statsFile=$cwd/stats.txt
    python $root/Apps/monitoring.py $statsFile $ailiaDir/$modelDir/$model.py --video $cwd/$inVideo --savepath $cwd/$outVideo --env_id $envID --benchmark_count 5
    mv $statsFile $resDir/stats.txt
    stats_gpu=$(awk 'NR==1 {print $NF}' $resDir/stats.txt)
    stats_cpu=$(awk 'NR==2 {print $NF}' $resDir/stats.txt)
    stats_mem=$(awk 'NR==3 {print $NF}' $resDir/stats.txt)
    stats_time=$(awk 'NR==4 {print $NF}' $resDir/stats.txt)
else
    # Corre modelo
    cd $ailiaDir/$modelDir
    python $model.py --video $cwd/$inVideo --savepath $cwd/$outVideo --env_id $envID --benchmark_count 5
fi


# Muevo los resultados a la carpeta resultados/modelo/fecha
mv $cwd/$outVideo $resDir/$videoName-out.mp4
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
echo "fecha, algoritmo, video, TE: HOTA, TE: DetA, TE: AssA, TE: DetRe, TE: DetPr, TE: AssRe, TE: AssPr, TE: LocA, TE: IDF1, TE: IDR, TE: IDP, TE: IDTP, TE: IDFN, TE: IDFP, TE: SFDA, TE: ATA, MP: F1 Score Detecciones, MP: Precision Detecciones, MP: Recall Detecciones, MP: Max Personas Detectadas/Esperadas, HM: IOUBB[%], Tiempo [s], RAM [MB], CPU [%], GPU [%], Carpeta" >> $resDir/resultados.csv

te=($(sed -n 2p $resDir/pedestrian_summary.txt))
mp1=($(sed -n 1p $resDir/metrics.txt))
mp2=($(sed -n 2p $resDir/metrics.txt))
mp3=($(sed -n 3p $resDir/metrics.txt))
mp4=($(sed -n 11p $resDir/metrics.txt))
hm=($(sed -n 1p $resDir/HeatMapIndicator/IoUBB.txt))

line="$dateName, $modelDir, $inVideo, ${te[0]}, ${te[1]}, ${te[2]}, ${te[3]}, ${te[4]}, ${te[5]}, ${te[6]}, ${te[7]}, ${te[29]}, ${te[30]}, ${te[31]}, ${te[32]}, ${te[33]}, ${te[34]}, ${te[39]}, ${te[40]}, ${mp1[3]}, ${mp2[2]}, ${mp3[2]}, ${mp4[6]}/${mp4[9]}, ${hm[0]}, $stats_time, $stats_mem, $stats_cpu, $stats_gpu, ../resultados/$model/$dateName"

echo $line >> $resDir/resultados.csv

echo $line >> $root/resultados/resultados.csv

echo "Los resultados se encuentran en la carpeta $resDir"