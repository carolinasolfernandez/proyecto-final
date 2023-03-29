# Análisis del comportamiento de clientes mediante técnicas de inteligencia artificial y visión por computadora

El siguiente repositorio contiene el código desarrollado bajo el marco del Proyecto Final de la carrera de Ingeniería Electrónica de la UTN FRBA durante el año 2022.
El mismo fue llevado a cabo por: 

_Salvador Apablaza, Carolina Sol Fernández y Nicolás Gabriel Locatti_.

# Resumen
En el presente trabajo se desarrolla un framework de detección de personas para analizar el comportamiento de los clientes en una tienda minorista mediante el procesamiento de videos de vigilancia. Para ello, se propone un pipeline compuesto por un preprocesamiento del video, un procesamiento con un modelo basado en redes neuronales, y un postprocesamiento orientado a correcciones. Se proveen indicadores útiles para los negocios, entre ellos, un mapa de calor que muestra los espacios ocupados. El resultado es constatado con un etiquetado manual para evaluar el rendimiento del algoritmo. Se demuestra la viabilidad de este método para comprender el comportamiento de los clientes. 


# Ejecutar circuito
- Instalar las herramientas segun lo indicado [aqui](#instalar)
- Tener un video y su ground truth en Mot1.1
    - El formato Mot1.1 exportado del cvat tiene faltante la columna score/conf. Se debe setear a 1 (se sabe al 100% que es una persona)
    - El formato de los datasets generados con ailia responden al formato: {frame, id, x, y, width, height, score/conf, x, y, z}. x, y, z son seteados a -1
- Ejecutar el comando con los valores correspondiente. Referir a [scripts](./scripts/) para docs:
```
cd scripts
sh pipeline.sh -i ../data/videos/59.mp4 -g ../data/gt/59.txt -m object_tracking/siam-mot
```
- Visualizar los resultados en la carpeta [resultados](./resultados/)


# ailia-models
Contiene la solucion de [ailia-models](https://github.com/axinc-ai/ailia-models/blob/master/TUTORIAL.md) modificado para guardar el csv etiquetado. Seguir las instrucciones del tutorial con una licencia de prueba.
- Se utilizo el `launcher.py`.
- El dataset de cada modelo se guarda en la carpeta principal bajo el nombre `output.txt`
- No se agrego soporte para todos los datasets. Hay datasets programados diferentes. 
- Para agregar soporte, se puede basar en la modificacion del [siam-mot.py](./ailia-models/object_tracking/siam-mot/siam-mot.py) - creacion y llamado de `write_prediction()` - o del [detector_utils.py](./ailia-models/util/detector_utils.py) - creacion y llamado de `write_prediction2()` -
- TODO @any agregar benchmark a los datasets

# Instalar
## ailia-models
- [Download a free evaluation version of ailia SDK](https://ailia.jp/en/trial)
- Unzip ailia SDK
- Run the following command

```
cd ailia_sdk/python
python3 bootstrap.py
pip3 install .
```

- Place the license file in the same folder as libailia.dll ([python_path]/site_packages/ailia) on Windows and in ~/Library/SHALO/ on Mac.
- You can find the location of Python site-packages directory using the following command:
```
pip3 show ailia
```

- Instalar ailia models. Parado en este repo:
```
cd ailia-models
pip install -r requirements.txt
```

- Ejecutar programa:
```
 python launcher.py
```

## TrackEval
- En este repositorio:
```
cd TrackEval
```
- En el caso de windows tuve que modificar el requirements.txt para instalar numpy y scipy manualmente:
    - Modificar el archivo requirements.txt y comentar las 2 primeras lineas.
    - Instalar manualmente numpy y scipsy: `python install numpy scipsy`
- Instalar el resto de los requerimientos
```
pip install -r requirements.txt
```
- Ejecutar el script:
```
cd scripts
python run_mot_challenge.py --BENCHMARK PF --DO_PREPROC False
```
- La salida se guarda en `Trackeval/data/trackers/mot_challenge/PF-train/data/pedestrian_plot.pdf`
- Para entrenar un modelo, se debe modificar el ground truth y el dataset con nuestros datos:
    - GT: `TrackEval/data/gt/mot_challenge/PF-train/PF-01/gt/gt.txt`
    - Dataset: `TrackEval/data/trackers/mot_challenge/PF-train/data/data/PF-01.txt`


## HeatMapIndicator
- En este repositorio:
```
cd Apps/HeatMapIndicator
pip install -r requirements.txt
```
