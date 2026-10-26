import json
from copy import deepcopy
from pathlib import Path


class ManejadorJSON:
    """Importa, modifica y guarda una lista de registros JSON."""

    def __init__(self, ruta_original: str):
        self.ruta_original = Path(ruta_original)
        self.datos = None
        self.registros_importados = 0
        self.modificaciones = []
        self.metodos_utilizados = []

    def importar(self):
        """Lee el JSON local y devuelve una copia de los registros."""
        with open(
            self.ruta_original,
            mode="r",
            encoding="utf-8-sig"
        ) as archivo:
            # Admitir los saltos de línea presentes en el original.
            datos = json.load(archivo, strict=False)

        if not isinstance(datos, list) or not all(
            isinstance(registro, dict) for registro in datos
        ):
            raise ValueError(
                "Se esperaba una lista de registros (diccionarios)."
            )

        self.datos = datos
        self.registros_importados = len(datos)
        self.modificaciones = []
        self.metodos_utilizados = ["importar"]

        return deepcopy(self.datos)

    def modificar(
        self,
        indice_registro: int,
        campo: str,
        nuevo_valor
    ):
        """Actualiza un campo de un registro de la lista principal."""
        if self.datos is None:
            raise RuntimeError("Primero debes importar el archivo JSON.")

        if not 0 <= indice_registro < len(self.datos):
            raise IndexError("El índice de registro está fuera de rango.")

        registro = self.datos[indice_registro]

        if campo not in registro:
            raise ValueError(f"No existe el campo: {campo}")

        valor_anterior = deepcopy(registro[campo])
        registro[campo] = deepcopy(nuevo_valor)

        cambio = {
            "registro": indice_registro,
            "campo": campo,
            "valor_anterior": valor_anterior,
            "valor_nuevo": deepcopy(nuevo_valor)
        }

        self.modificaciones.append(cambio)
        self.metodos_utilizados.append("modificar")

        return deepcopy(cambio)

    def guardar(self, ruta_salida: str):
        """Guarda un nuevo JSON y devuelve los resultados del proceso."""
        if self.datos is None:
            raise RuntimeError("Primero debes importar el archivo JSON.")

        ruta_salida = Path(ruta_salida)

        if ruta_salida.resolve() == self.ruta_original.resolve():
            raise ValueError(
                "Usa una ruta diferente para conservar el original."
            )

        ruta_salida.parent.mkdir(parents=True, exist_ok=True)

        with open(
            ruta_salida,
            mode="w",
            encoding="utf-8"
        ) as archivo:
            json.dump(
                self.datos,
                archivo,
                ensure_ascii=False,
                indent=4,
                allow_nan=False
            )

        self.metodos_utilizados.append("guardar")

        return {
            "clase": type(self).__name__,
            "archivo_importado": str(self.ruta_original),
            "archivo_guardado": str(ruta_salida),
            "registros_importados": self.registros_importados,
            "registros_guardados": len(self.datos),
            "modificaciones": deepcopy(self.modificaciones),
            "metodos_utilizados": self.metodos_utilizados.copy()
        }