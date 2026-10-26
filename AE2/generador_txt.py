from copy import deepcopy
from pathlib import Path


class GeneradorResumenTXT:
    """Genera un resumen con los resultados reales de CSV y JSON."""

    def __init__(
        self,
        resultado_csv: dict,
        resultado_json: dict,
        url_csv: str,
        url_json: str
    ):
        self.resultados = [
            ("CSV", deepcopy(resultado_csv), url_csv),
            ("JSON", deepcopy(resultado_json), url_json)
        ]

    def generar(self, ruta_salida: str = "resumen.txt"):
        ruta = Path(ruta_salida)

        # Evitar que el resumen sobrescriba un archivo de datos.
        for _, resultado, _ in self.resultados:
            for clave in ("archivo_importado", "archivo_guardado"):
                if ruta.resolve() == Path(resultado[clave]).resolve():
                    raise ValueError(
                        "El resumen debe tener una ruta distinta "
                        "a los archivos de datos."
                    )

        lineas = [
            "RESUMEN DE LA ACTIVIDAD AE2",
            "=" * 60,
            f"Generador: {type(self).__name__}.generar()"
        ]

        for formato, resultado, url in self.resultados:
            # Mostrar cada nombre de método una sola vez.
            metodos = dict.fromkeys(resultado["metodos_utilizados"])

            lineas.extend([
                "",
                f"FORMATO: {formato}",
                "-" * 60,
                f"URL de origen: {url}",
                f"Archivo importado: {resultado['archivo_importado']}",
                f"Archivo guardado: {resultado['archivo_guardado']}",
                f"Clase utilizada: {resultado['clase']}",
                "Metodos utilizados: " + ", ".join(
                    f"{resultado['clase']}.{metodo}()"
                    for metodo in metodos
                ),
                f"Registros importados: {resultado['registros_importados']}",
                f"Registros guardados: {resultado['registros_guardados']}",
                f"Modificaciones realizadas: {len(resultado['modificaciones'])}"
            ])

            for cambio in resultado["modificaciones"]:
                lineas.extend([
                    f"  Registro (indice desde 0): {cambio['registro']}",
                    f"  Campo: {cambio['campo']}",
                    f"  Antes: {cambio['valor_anterior']!r}",
                    f"  Despues: {cambio['valor_nuevo']!r}"
                ])

        ruta.parent.mkdir(parents=True, exist_ok=True)

        with open(ruta, mode="w", encoding="utf-8") as archivo:
            archivo.write("\n".join(lineas) + "\n")

        return ruta