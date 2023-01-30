# Apps nuestras

# Metrics
Script para calcular metricas de negocio. Ejecutarlo con el comando:
```
 python metrics.py 
    -d <dataset_file> 
    -g <ground_truth_file> 
    -o <folder_output>
 ```
Folder output es opcional. Si falta, se guarda los resultados en la carpeta actual.
 
### Ejemplo:
```
 python metrics.py -d ../resultados/yolox/20221104-155223/20221104-155223-out.txt -g ../resultados/yolox/20221104-155223/gt.txt
```

# HeatMap
- Instalacion:
```
cd Apps/HeatMapIndicator
pip install -r requirements.txt
```
- Script para generar mapas de calor:
```
python HeatMapIndicator/main.py 
```
En el caso de error `in create_folder`:
```
cd HeatMapIndicator
python main.py [output-folder-name : optional]
```
- Uso:
   - La carpeta HeatMapIndicator/Input debe contener los archivos:
      - `background.jpg`: imagen del video sin personas
      - `gt`: ground truth file
      - `input.mp4`: video a analizar
      - `detection.txt`: dataset generado por el algoritmo bajo analisis
   - La información de entrada, de salida y el código utilizado quedan almacenado en HeatMapIndicator/Output/Timestamp con el horario de la ejecución del script.


## Metricas disponibles
- Error relativo de cantidad de personas detectadas por frame: 
$\displaystyle\frac{Detectadas-Reales}{Max(Detecatadas, Reales)} *100%$

- Error relativo de cantidad de personas detectadas promedio en dataset: 
$\displaystyle\frac{\sum_{f=1}^{frames} Error_f}{frames}$

- Precision Personas Detectadas: 
$\displaystyle\frac{T_P}{T_P+F_P}$

- Recall Personas Detectadas: 
$\displaystyle\frac{T_P}{T_P+F_N}$

- F1 Score Personas Detectadas: 
$\displaystyle\frac{2*Precision*Recall}{Precision + Recall}$

- Momento mas concurrido: Frames con mayor cantidad de detecciones

- Zona más concurrida con distintos niveles de threshold por dos medios:
1. Sustracción de fondo del video.
2. A traves de los bounding box detectados y ground truth en caso de haber.

## Salida
- Grafico con evolucion por frame: [`error_obj.png`](../resultados/yolox/20221104-162639/error_obj.png)
- Archivo con todas las metricas: [`metrics.txt`](../resultados/yolox/20221104-162639/metrics.txt)
- HeatMap por sustracción de fondo[`Heatmap.jpg`](https://github.com/carolinasolfernandez/proyecto-final/blob/main/Apps/HeatMapIndicator/Output/202311815129/Heatmap.jpg) 
- HeatMap por bounding box detectado[`Heatmapdetection.jpg`](https://github.com/carolinasolfernandez/proyecto-final/blob/main/Apps/HeatMapIndicator/Output/202311815129/Heatmapdetection.jpg)
- HeatMap por bounding box ground truth[`Heatmapgt.jpg`](https://github.com/carolinasolfernandez/proyecto-final/blob/main/Apps/HeatMapIndicator/Output/202311815129/Heatmapgt.jpg)
- Archivo con bounding box para cada threshold: [`result.txt`](https://github.com/carolinasolfernandez/proyecto-final/blob/main/Apps/HeatMapIndicator/Output/202311815129/result.txt)
