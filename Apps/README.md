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

## Metricas disponibles
- Error de cantidad de personas detectadas por frame: 
$\displaystyle\frac{Detectadas-Reales}{Detecatadas} *100%$

- Error de cantidad de personas detectadas promedio en dataset: 
$\displaystyle\frac{\sum_{f=1}^{frames} Error_f}{frames}$

## Salida
- Grafico con evolucion por frame: [`error_obj.png`](../resultados/yolox/20221104-162639/error_obj.png)
- Archivo con todas las metricas: [`metrics.txt`](../resultados/yolox/20221104-162639/metrics.txt)
