from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

# carpeta donde se guardarán archivos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE = os.path.join(BASE_DIR, "server_storage")

os.makedirs(STORAGE, exist_ok=True)

# =========================
# SUBIR ARCHIVO (.json)
# =========================
@app.route("/upload", methods=["POST"])
def upload():

    if "file" not in request.files:
        return jsonify({"error": "No se envió archivo"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Archivo vacío"}), 400

    path = os.path.join(STORAGE, file.filename)
    file.save(path)

    return jsonify({
        "ok": True,
        "filename": file.filename
    })


# =========================
# VER ARCHIVOS DEL SERVIDOR
# =========================
@app.route("/")
def index():
    files = os.listdir(STORAGE)
    return jsonify({
        "archivos": files
    })


# =========================
# DESCARGAR ARCHIVO
# =========================
@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(STORAGE, filename, as_attachment=True)


# =========================
# INICIO SERVIDOR
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

