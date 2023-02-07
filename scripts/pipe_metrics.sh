#! usr/bin/bash

# Ejecuta las metricas usando un video ya procesado y guardado en alguna carpeta de resultados

####### Datos a modificar ########

nombre=large1
modelDir=object_tracking/siam-mot
date=20230207-031124 # fecha de ejecucion a reejecutar

nombre=59
modelDir=object_tracking/siam-mot
date=20230206-052246 # fecha de ejecucion a reejecutar

#### Modificar solo si cambian directorios - sino se usa el nombre convencion
inVideo=../data/videos/$nombre.mp4
#videoProcesado=$nombre-out.mp4
gt=data/gt/$nombre.txt
#################################


dateName="$(date +%Y%m%d-%H%M%S)"
datasetProcesado=$date-out.txt
model="$(basename -- $modelDir)"
dirProcesadoAnterior=resultados/$model/$nombre/$date

cwd=$(pwd)
root=$(pwd)/..

# Muevo los resultados a la carpeta resultados/modelo/fecha
resDir=$root/resultados/$model/$nombre/$dateName
mkdir -p $resDir
#cp $root/$dirProcesadoAnterior/$videoProcesado $resDir/$videoProcesado
cp $root/$dirProcesadoAnterior/$datasetProcesado $resDir/$dateName-out.txt
salidaDataset=$resDir/$dateName-out.txt


# Ejecuta Filtrado
cd $root/Apps
python filter_objects.py $resDir/$dateName-out.txt $resDir/$dateName-out-filtered.txt
salidaDataset=$resDir/$dateName-out-filtered.txt



# Copia dataset y GT a TrackEval
evalDirGT=$root/TrackEval/data/gt/mot_challenge/PF-train/PF-01/gt
evalDirData=$root/TrackEval/data/trackers/mot_challenge/PF-train/data
cp $root/$gt $evalDirGT/gt.txt
cp $salidaDataset $evalDirData/data/PF-01.txt

# Ejecuta TrackEval
cd $root/TrackEval/scripts
python run_mot_challenge.py --BENCHMARK PF --DO_PREPROC False

# Copia resultados de TrackEval a Resultados
cp $evalDirData/pedestrian_detailed.csv $resDir/
cp $evalDirData/pedestrian_plot.png $resDir/
cp $evalDirData/pedestrian_summary.txt $resDir/
cp $root/$gt  $resDir/gt.txt

# Ejecuta Metricas de Negocio
cd $root/Apps
python metrics.py -d $salidaDataset -g $resDir/gt.txt -o $resDir


# Copio archivos necesario para HeatMapIndicator
cp $root/$gt $root/Apps/HeatMapIndicator/Input/gt.txt
cp $salidaDataset $root/Apps/HeatMapIndicator/Input/detection.txt
cp $cwd/$inVideo $root/Apps/HeatMapIndicator/Input/input.mp4

echo "ejecutando mapa de calor ...."
# Ejecuta Mapa de calor
cd $root/Apps/HeatMapIndicator
python main.py -d $dateName
mv $root/Apps/HeatMapIndicator/Output/$dateName $resDir/HeatMapIndicator


echo "rellenando el csv de resultados ..."
echo "fecha, algoritmo, video, TE: HOTA, TE: DetA, TE: AssA, TE: DetRe, TE: DetPr, TE: AssRe, TE: AssPr, TE: LocA, TE: IDF1, TE: IDR, TE: IDP, TE: IDTP, TE: IDFN, TE: IDFP, TE: SFDA, TE: ATA, MP: F1 Score Detecciones, MP: Precision Detecciones, MP: Recall Detecciones, MP: Max Personas Detectadas/Esperadas, HM: IOU[%], Tiempo [s], RAM [MB], CPU [%], GPU [%], Carpeta" >> $resDir/resultados.csv

te=($(sed -n 2p $resDir/pedestrian_summary.txt))
mp1=($(sed -n 1p $resDir/metrics.txt))
mp2=($(sed -n 2p $resDir/metrics.txt))
mp3=($(sed -n 3p $resDir/metrics.txt))
mp4=($(sed -n 11p $resDir/metrics.txt))
hm=($(sed -n 1p $resDir/HeatMapIndicator/IoUBB.txt))
line="$dateName, $modelDir-filtered, $inVideo, ${te[0]}, ${te[1]}, ${te[2]}, ${te[3]}, ${te[4]}, ${te[5]}, ${te[6]}, ${te[7]}, ${te[29]}, ${te[30]}, ${te[31]}, ${te[32]}, ${te[33]}, ${te[34]}, ${te[39]}, ${te[40]}, ${mp1[3]}, ${mp2[2]}, ${mp3[2]}, ${mp4[6]}/${mp4[9]}, ${hm[0]}, -1, -1, -1, -1, ../resultados/$model/$dateName"

echo $line >> $resDir/resultados.csv

echo $line >> $root/resultados/resultados.csv

echo "Los resultados se encuentran en la carpeta $resDir"