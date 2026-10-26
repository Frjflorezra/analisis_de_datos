import csv
from pathlib import Path


class ManejadorCSV:
    """Importa, modifica y guarda archivos CSV locales."""

    def __init__(self, ruta_original: str):
        self.ruta_original = Path(ruta_original)
        self.encabezados = []
        self.datos = None
        self.registros_importados = 0
        self.modificaciones = []
        self.metodos_utilizados = []

    def importar(self):
        """Lee los encabezados y los registros del CSV."""
        with open(
            self.ruta_original,
            mode="r",
            encoding="utf-8-sig",
            newline=""
        ) as archivo:
            lector = csv.reader(archivo)

            encabezados = next(lector, None)

            if not encabezados:
                raise ValueError("El archivo CSV no tiene encabezados.")

            datos = [fila for fila in lector if fila]

        if any(len(fila) != len(encabezados) for fila in datos):
            raise ValueError(
                "Hay filas con una cantidad incorrecta de columnas."
            )

        self.encabezados = encabezados
        self.datos = datos
        self.registros_importados = len(datos)

        # Reiniciar el historial al importar el archivo original.
        self.modificaciones = []
        self.metodos_utilizados = ["importar"]

        # Devolver copias para conservar una vista del antes.
        return (
            self.encabezados.copy(),
            [fila.copy() for fila in self.datos]
        )

    def modificar(self, indice_fila: int, columna: str, nuevo_valor):
        """Actualiza una celda. La primera fila de datos tiene índice 0."""
        if self.datos is None:
            raise RuntimeError("Primero debes importar el archivo CSV.")

        if columna not in self.encabezados:
            raise ValueError(f"No existe la columna: {columna}")

        if not 0 <= indice_fila < len(self.datos):
            raise IndexError("El índice de fila está fuera de rango.")

        indice_columna = self.encabezados.index(columna)
        valor_anterior = self.datos[indice_fila][indice_columna]
        valor_nuevo = str(nuevo_valor)

        self.datos[indice_fila][indice_columna] = valor_nuevo

        cambio = {
            "registro": indice_fila,
            "campo": columna,
            "valor_anterior": valor_anterior,
            "valor_nuevo": valor_nuevo
        }

        self.modificaciones.append(cambio)
        self.metodos_utilizados.append("modificar")

        return cambio.copy()

    def guardar(self, ruta_salida: str):
        """Guarda un nuevo CSV y devuelve los resultados del proceso."""
        if self.datos is None:
            raise RuntimeError("Primero debes importar el archivo CSV.")

        ruta_salida = Path(ruta_salida)

        if ruta_salida.resolve() == self.ruta_original.resolve():
            raise ValueError(
                "Usa una ruta diferente para conservar el original."
            )

        ruta_salida.parent.mkdir(parents=True, exist_ok=True)

        with open(
            ruta_salida,
            mode="w",
            encoding="utf-8",
            newline=""
        ) as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(self.encabezados)
            escritor.writerows(self.datos)

        self.metodos_utilizados.append("guardar")

        return {
            "clase": type(self).__name__,
            "archivo_importado": str(self.ruta_original),
            "archivo_guardado": str(ruta_salida),
            "registros_importados": self.registros_importados,
            "registros_guardados": len(self.datos),
            "modificaciones": [
                cambio.copy() for cambio in self.modificaciones
            ],
            "metodos_utilizados": self.metodos_utilizados.copy()
        }