# Resultados
Se utilizo el ailia-models y TrackEval para obtener los resultados. Esta organizado en:
- Carpeta con nombre de modelo:
    - Fecha de ejecucion
        - Video original
        - Export del dataset etiquetado cvat (gt)
        - Video etiquetado por el modelo
        - Export del dataset del modelo
        - Resultados de TrackEval
        - Metricas propias:
            - Archivo `metrics.txt`
            - Graficos de cada metrica (`person_count.png`, `mas_concurrido.png`)

- El formato de los datasets generados con ailia responden al formato: {frame, id, x, y, width, height, score/conf, x, y, z}. x, y, z son seteados a -1
- El formato Mot1.1 exportado del cvat tiene faltante la columna score/conf. Se debe setear a 1 (se sabe al 100% que es una persona)
