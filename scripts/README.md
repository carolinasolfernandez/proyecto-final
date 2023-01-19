# Scripts

Esta carpeta contiene los scripts a ejecutar

# Pipeline
El script `pipeline.sh`:
- Ejecuta el modelo indicado
- Evalua el dataset resultante usando trackeval
- Evalua metricas de negocio
- Genera un mapa de calor.

Para usarlo, se necesita tener [instalado ailia-models y TrackEval](../README.md#instalar), referenciados en esta misma solucion.
```
sh pipeline.sh -i ../data/videos/59.mp4 -g ../data/gt/59.txt -m object_tracking/siam-mot
```
Los resultados y datos utilizados estaran disponibles en [resultados/{modelo}/{fecha}](../resultados/) una vez termine el script.

## Parametros:
- -i: input video. Video a ser analizado
- -g: ground truth. Etiquetado del video
- -m: modelo a ejecutar de ailia-models. Se pueden ver los modelos en [ailia-models](../ailia-models/)
    - Ej1: object_tracking/siam-mot
    - Ej2: object_detection/yolox
- -e env_id. Opcional. Placa grafica a utilizar. Ejecutar y ver en el luncher, el index de la GPU ` python launcher.py`