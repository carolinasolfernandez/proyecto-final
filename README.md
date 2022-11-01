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

No todos los datasets tienen el mismo formato. En algunos se utilizo width y en otro x1,x2->(top left, rigth bottom). Tener en cuenta que el extremo superior izquierdo es (0,0) y es positivo hacia abajo y a la derecha.



# ailia-models
Contiene la solucion de [ailia-models](https://github.com/axinc-ai/ailia-models/blob/master/TUTORIAL.md) modificado para guardar el csv etiquetado. Seguir las instrucciones del tutorial con una licencia de prueba.
- Se utilizo el `launcher.py`.
- El dataset de cada modelo se guarda en la carpeta del modelo bajo el nombre `output.csv`
- Una vez ejecutado el modelo, se debe agregar una linea de encabezado al `output.csv`, y cortarlo, ya que se apendea el contenido.
- No se agrego soporte para todos los datasets. Hay datasets programados diferentes. 
- Para agregar soporte, se puede basar en la modificacion del [siam-mot.py](./ailia-models/object_tracking/siam-mot/siam-mot.py) o del [detector_utils.py](./ailia-models/util/detector_utils.py)
- TODO @any agregar benchmark a los datasets