from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)


df = pd.read_csv("Copia de spotify_songs.csv")

@app.route("/health")
def health():
    return jsonify({"status": "ok", "entorno": "listo"})


#Endpoint songs
@app.route("/songs")
def getSongs():
    df_proc = df.copy() #Se hace la copia del DF para no alterarl os datos og y poder hacer los filtros
    #por artista
    artist = request.args.get("track_artist") #lee el parametro que se escribe en la URL después del "?" Busca la clave que coincide con lo que está 
    #en el parámetro. En este caso es el nombre de mi columna en el csv.
    #Va a extraer el valor a la derecha del "=" y lo guardará en mi variable artis como un String.
    if artist:
        df_proc = df_proc[df_proc["track_artist"].str.contains(artist)]

    #nombre de canción
    song_name = request.args.get("track_name")
    if song_name:
        df_proc = df_proc[df_proc["track_name"].str.contains(song_name)]

    #popularidad
    popularity = request.args.get("track_popularity")
    if popularity:
        df_proc = df_proc[df_proc["track_popularity"] == int(popularity)] #parse a int pq la columna es int pero viene como string

    top_songs = int(request.args.get("limit") or 10) #Si se hace una consulta y ponen un limit, lo toma y se guarda en la variable. sino por defecto toma 10
    df_proc = df_proc.head(top_songs)

    return jsonify(df_proc.to_dict(orient="records")) #orient="records" devuelve cada fila como diccionario individual donde las claves son los nombres de las columnas y los valores son los datos de la canción

if __name__ == "__main__":
    app.run(debug=True)


#& separador