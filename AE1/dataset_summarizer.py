from pathlib import Path

import pandas as pd


class DatasetSummarizer:

    def __init__(self, dataframe: pd.DataFrame):
        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError("Se debe proporcionar un DataFrame de pandas.")

        self.dataframe = dataframe

    def generar_resumen(
        self,
        ruta_salida: str = "resumen_dataset.txt"
    ) -> Path:
        filas, columnas = self.dataframe.shape

        # Mostrar el tipo de dato y los nulos de cada columna.
        detalle_columnas = pd.DataFrame({
            "Tipo de dato": self.dataframe.dtypes.astype(str),
            "Valores nulos": self.dataframe.isna().sum()
        })
        detalle_columnas.index.name = "Columna"

        total_nulos = int(self.dataframe.isna().sum().sum())

        secciones = [
            "RESUMEN DEL DATAFRAME",
            "=" * 60,
            f"Cantidad de filas: {filas}",
            f"Cantidad de columnas: {columnas}",
            f"Total de valores nulos: {total_nulos}",
            "",
            "COLUMNAS, TIPOS DE DATOS Y VALORES NULOS",
            "-" * 60,
            detalle_columnas.to_string()
        ]

        # Calcular estadísticas de las columnas numéricas.
        datos_numericos = self.dataframe.select_dtypes(
            include="number"
        )

        if not datos_numericos.empty:
            secciones.extend([
                "",
                "ESTADÍSTICAS DESCRIPTIVAS",
                "-" * 60,
                datos_numericos.describe().round(2).to_string()
            ])

        # Guardar el resumen con codificación UTF-8.
        ruta = Path(ruta_salida)
        ruta.write_text(
            "\n".join(secciones),
            encoding="utf-8"
        )

        return ruta