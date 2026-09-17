from flask import Flask, jsonify
from canciones.routes import canciones_bp

app = Flask(__name__)
app.register_blueprint(canciones_bp)

@app.route("/health")
def health():
    return jsonify({"status": "ok", "entorno": "listo"})

if __name__ == "__main__":
    app.run(debug=True)