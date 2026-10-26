# AE2: procesamiento de archivos CSV y JSON

Este proyecto importa archivos locales CSV y JSON, modifica sus datos mediante clases separadas y guarda nuevas versiones conservando los originales. También genera un resumen TXT con las fuentes, las modificaciones y los resultados de la ejecución.

## Estructura del proyecto

```text
AE2/
├── manejador_csv.py
├── manejador_json.py
├── generador_resumen_txt.py
├── actividad_ae2.ipynb
├── README.md
├── resumen.txt
├── originales/
│   ├── Iris.csv
│   └── case_study_university.json
└── modificados/
    ├── Iris_modificado.csv
    └── case_study_university_modificado.json
```

Los archivos originales y modificados están incluidos en el repositorio. No es necesario descargar nuevamente los datos para ejecutar el proyecto.

## Requisitos

- Python 3.
- Un entorno compatible con Jupyter Notebook.

Las clases utilizan únicamente módulos de la biblioteca estándar de Python: `csv`, `json`, `pathlib` y `copy`.

## Ejecución

1. Abrir la carpeta `AE2` como directorio de trabajo.
2. Abrir `actividad_ae2.ipynb` en un entorno compatible con Jupyter.
3. Reiniciar el kernel y ejecutar todas las celdas en orden.
4. Revisar las salidas que muestran los datos antes y después de las modificaciones y el contenido del resumen.

Las rutas utilizadas son relativas a `AE2`. La ejecución actualiza los archivos de la carpeta `modificados` y el archivo `resumen.txt`, conservando los originales.

## Clases y responsabilidades

| Archivo | Clase | Responsabilidad |
|---|---|---|
| `manejador_csv.py` | `ManejadorCSV` | Importar con `csv.reader`, modificar una celda y guardar con `csv.writer`, incluyendo encabezados. |
| `manejador_json.py` | `ManejadorJSON` | Importar con `json.load`, modificar un campo y guardar con `json.dump`. |
| `generador_resumen_txt.py` | `GeneradorResumenTXT` | Generar el resumen a partir de los resultados de ambas clases y las URL de origen. |

El notebook coordina las llamadas a las clases y verifica los archivos generados.

## Datos y fuentes

Los originales fueron obtenidos de Hugging Face:

- **CSV:** [Iris.csv — scikit-learn/iris](https://huggingface.co/datasets/scikit-learn/iris/resolve/main/Iris.csv).
- **JSON:** [case_study_university.json — osunlp/HippoRAG_2](https://huggingface.co/datasets/osunlp/HippoRAG_2/resolve/main/case_study_university.json).

Estas URL también están definidas en el notebook y se incorporan al resumen TXT.

El JSON original contiene saltos de línea literales dentro de algunos textos. La clase los admite mediante `json.load(..., strict=False)`. Al guardar, `json.dump` los representa correctamente, de modo que el archivo generado admite la lectura estricta habitual.

## Modificaciones realizadas

- **CSV:** se actualiza `SepalLengthCm` en la primera fila de datos, de `5.1` a `5.2`.
- **JSON:** se sustituye el campo `question` del primer registro por una pregunta en español.

Ambas modificaciones se implementan dentro de sus respectivas clases y se ejecutan desde el notebook.

## Resultados

- `modificados/Iris_modificado.csv`: CSV actualizado con sus encabezados.
- `modificados/case_study_university_modificado.json`: JSON actualizado.
- `resumen.txt`: informe generado con las URL de origen, las rutas de entrada y salida, las clases y métodos utilizados, las cantidades de registros y los valores anteriores y posteriores a los cambios.

Cada elemento de la lista principal del JSON cuenta como un registro. Los párrafos anidados forman parte de ese registro.

## Verificación

El notebook vuelve a leer los archivos modificados y comprueba:

- La conservación de los encabezados del CSV.
- La coincidencia del contenido guardado con los datos de las clases.
- La aplicación de las modificaciones.
- Las cantidades de registros guardados.
- La conservación exacta de los bytes de los originales.
- La presencia de las fuentes y los cambios en el resumen.

Si todas las comprobaciones se cumplen, la última celda muestra:

```text
Flujo completo ejecutado correctamente.
```