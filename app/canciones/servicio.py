import json
from pathlib import Path

RUTA_DATOS = Path(__file__).resolve().parent.parent.parent / "data" / "canciones.json"

def cargar_canciones():
    with open(RUTA_DATOS, "r") as f:
        return json.load(f)

def guardar_canciones(canciones):
    with open(RUTA_DATOS, "w") as f:
        json.dump(canciones, f, indent=4)

def listar_canciones(artista=None):
    canciones = cargar_canciones()
    if artista is None:
        return canciones
    return [cancion for cancion in canciones if cancion.get("artista", "").lower() == artista.lower()]

def buscar_cancion_por_id(id):
    canciones = cargar_canciones()
    for cancion in canciones:
        if cancion["id"] == id:
            return cancion
    return None

def crear_cancion(datos):
    canciones = cargar_canciones()
    nuevo_id = (max(cancion["id"] for cancion in canciones) + 1) if canciones else 1
    nueva_cancion = {
        "id": nuevo_id,
        "titulo": datos["titulo"],
        "artista": datos.get("artista", ""),
        "album": datos.get("album", ""),
        "anio": datos.get("anio", ""),
        "genero": datos.get("genero", ""),
        "duracion": datos.get("duracion", "")
    }
    canciones.append(nueva_cancion)
    guardar_canciones(canciones)
    return nueva_cancion
