from flask import Flask, jsonify, request
from routes.web import web_bp
from routes.api import api_bp
from database import inicializar_base_datos

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_SORT_KEYS"] = False

app.register_blueprint(web_bp)
app.register_blueprint(api_bp)


@app.errorhandler(404)
def error_404(error):
    if request.path.startswith("/api/"):
        return jsonify({"success": False, "error": "Recurso no encontrado."}), 404
    return "Página no encontrada.", 404


@app.errorhandler(400)
def error_400(error):
    if request.path.startswith("/api/"):
        return jsonify({"success": False, "error": "Solicitud incorrecta."}), 400
    return "Solicitud incorrecta.", 400


inicializar_base_datos()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
