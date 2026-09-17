from flask import Blueprint, jsonify, request, abort
import canciones.servicio as servicio

canciones_bp = Blueprint("canciones", __name__, url_prefix="/canciones")

@canciones_bp.get("")
def listar_canciones():
    artista = request.args.get("artista")
    canciones = servicio.listar_canciones(artista)
    return jsonify({"canciones": canciones})

@canciones_bp.get("/<int:id>")
def obtener_cancion(id):
    cancion = servicio.buscar_cancion_por_id(id)
    if cancion:
        return jsonify(cancion)
    return jsonify({"error": "Canción no encontrada"}), 404

@canciones_bp.post("")
def crear_cancion():
    datos = request.get_json()
    if not datos or "titulo" not in datos:
        abort(400, description="Datos inválidos. Se requiere el título de la canción.")
    nueva_cancion = servicio.crear_cancion(datos)
    return jsonify({"mensaje": "Canción creada correctamente", "cancion": nueva_cancion}), 201

@canciones_bp.delete("/<int:id>")
def eliminar_cancion(id):
    canciones = servicio.cargar_canciones()
    for cancion in canciones:
        if cancion["id"] == id:
            canciones.remove(cancion)
            servicio.guardar_canciones(canciones)
            return jsonify({"mensaje": "Canción eliminada correctamente"}), 200
    return jsonify({"error": "Canción no encontrada"}), 404

@canciones_bp.patch("/<int:id>")
def actualizar_cancion(id):
    datos = request.get_json()
    canciones = servicio.cargar_canciones()
    for cancion in canciones:
        if cancion["id"] == id:
            campos_permitidos = ["titulo", "artista", "album", "anio", "genero", "duracion"]
            for campo in campos_permitidos:
                if campo in datos:
                    cancion[campo] = datos[campo]
            servicio.guardar_canciones(canciones)
            return jsonify({"mensaje": "Canción actualizada correctamente"}), 200
    return jsonify({"error": "Canción no encontrada"}), 404
