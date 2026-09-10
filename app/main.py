from flask import Flask, jsonify, request, abort
import pandas as pd
import json
from pathlib import Path

RUTA_DATOS = Path("data/canciones.json")
def cargar_canciones():
    with open(RUTA_DATOS, "r") as f:
        return json.load(f)

def guardar_canciones(canciones):
    with open(RUTA_DATOS, "w") as f:
        json.dump(canciones, f, indent=4)

canciones = cargar_canciones()
print(canciones)

app = Flask(__name__)

# df = pd.read_csv("Copia de spotify_songs.csv")

@app.route("/health")
def health():
    return jsonify({"status": "ok", "entorno": "listo"})


@app.get("/canciones") #ruta estática
def listar_canciones():
    canciones = cargar_canciones()
    artista = request.args.get("artista")
    print(artista)
    return jsonify (canciones)

@app.get("/canciones/<int:id>")#ruta dinámica
def obtener_cancion(id):
    canciones = cargar_canciones()
    for cancion in canciones:
        if cancion["id"] == id:
            return jsonify(cancion)
    return jsonify({"error": "Canción no encontrada"}), 404

@app.errorhandler(404)
def not_found(e): #e = error
    return jsonify({"error": e.description}), 404

@app.post("/canciones")
def crear_cancion():
    datos = request.get_json()
    if not datos or "titulo" not in datos:
        return jsonify({"error": "Faltan datos"}), 400
    canciones = cargar_canciones()
    nuevo_id = max(cancion["id"] for cancion in canciones) + 1
    datos["id"] = nuevo_id
    canciones.append(datos)
    guardar_canciones(canciones)
    return jsonify({"mensaje": "Canción creada correctamente"}), 201


@app.delete("/canciones/<int:id>")
def eliminar_cancion(id):
    canciones = cargar_canciones()
    for cancion in canciones:
        if cancion["id"] == id:
            canciones.remove(cancion)
            guardar_canciones(canciones)
            return jsonify({"mensaje": "Canción eliminada correctamente"}), 200
    return jsonify({"error": "Canción no encontrada"}), 404

if __name__ == "__main__":
    app.run(debug=True)




#Endpoint songs
# @app.route("/songs")
# def getSongs(): #Esto es una ruta estática
#     df_proc = df.copy() #Se hace la copia del DF para no alterarl os datos og y poder hacer los filtros
#     #por artista
#     artist = request.args.get("track_artist") #lee el parametro que se escribe en la URL después del "?" Busca la clave que coincide con lo que está 
#     #en el parámetro. En este caso es el nombre de mi columna en el csv.
#     #Va a extraer el valor a la derecha del "=" y lo guardará en mi variable artis como un String.
#     if artist:
#         df_proc = df_proc[df_proc["track_artist"].str.contains(artist)]

#     #nombre de canción
#     song_name = request.args.get("track_name")
#     if song_name:
#         df_proc = df_proc[df_proc["track_name"].str.contains(song_name)]

#     #popularidad
#     popularity = request.args.get("track_popularity")
#     if popularity:
#         df_proc = df_proc[df_proc["track_popularity"] == int(popularity)] #parse a int pq la columna es int pero viene como string

#     top_songs = int(request.args.get("limit") or 10) #Si se hace una consulta y ponen un limit, lo toma y se guarda en la variable. sino por defecto toma 10
#     df_proc = df_proc.head(top_songs)

#     return jsonify(df_proc.to_dict(orient="records")) #orient="records" devuelve cada fila como diccionario individual donde las claves son los nombres de las columnas y los valores son los datos de la canción

#& separador
#@app.get
#@app.post