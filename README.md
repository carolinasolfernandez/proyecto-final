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