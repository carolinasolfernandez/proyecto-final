# Análisis de Zonas de Mayor Interés mediante Conteo de Objetos usando Cámara de Vigilancia

El siguiente repositorio contiene el código desarrollado bajo el marco del Proyecto Final de la carrera de Ingeniería Electrónica de la UTN FRBA durante el año 2022.
El mismo fue llevado a cabo por los alumnos _Apablaza, Salvador; Fernández, Carolina; Locatti, Nicolás y Schwartzman, Diego_.

# Hipótesis
La combinación de distintas herramientas de Machine Learning utilizadas para el análisis del comportamiento del peatón en un espacio exterior permite describir el análisis del comportamiento en un espacio interior mediante la obtención de indicadores sobre un video de vigilancia con vista en plano picado.

# Desarrollo
Se plantea realizar un framework que permita analizar el comportamiento que tienen los peatones dentro de un local en espacio interior, a partir de la observación de los mismos sobre la imágen de una cámara fija. Se tomará una muestra de video previamente almacenada en disco para ser procesada y analizada, quedando fuera de los requerimientos procesar las cámaras en vivo.
Se esperan obtener indicadores de comportamiento de las personas que puedan ser de utilidad para los negocios tales como:
- Contador de personas.
- Momento más concurrido.
- Análisis de trayectoria
- Personas por m 2 por tiempo, con el cual se podrá desarrollar un histograma que represente las zonas de mayor interés.

Se realizarán las pruebas sobre un conjunto de datos propios y etiquetados por el equipo, además se utilizarán datasets previamente utilizados por otras investigaciones afines. Para resolver la problemática se evaluarán distintas etapas de pre-procesamiento de la imagen tales como sustracción de fondo, recorte de imagen en zona de interés, entre otros filtros relacionados a la imagen. Para el procesamiento de los videos se analizarán distintos enfoques de machine learning que permitan obtener los indicadores antes mencionados, tales como CNN, GAN, SIFT, SIFT-FAST, entre otros que están bajo estudio.

# Resultados
Se utilizo el ailia-models para obtener los resultados. Esta organizado en:
- Carpeta con numero de video:
    - Video original
    - Export del dataset etiquetado cvat
    - Video etiquetado con el nombre del modelo
    - Export del dataset de cada modelo con su nombre

- El formato de los datasets generados con ailia responden al formato: {frame, id, x, y, width, height, score/conf, x, y, z}. x, y, z son seteados a -1
- El formato Mot1.1 exportado del cvat tiene faltante la columna score/conf. Se debe setear a 1 (se sabe al 100% que es una persona)


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