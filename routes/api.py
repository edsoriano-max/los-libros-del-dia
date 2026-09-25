from flask import Blueprint, request
from flask_restful import Api, Resource
from models.libro import (
    listar_libros, obtener_libro_por_id, crear_libro,
    actualizar_libro, eliminar_libro,
)

api_bp = Blueprint("api_bp", __name__, url_prefix="/api")
api = Api(api_bp)


def datos_libro(datos):
    if not isinstance(datos, dict):
        raise ValueError("El cuerpo debe ser un objeto JSON.")
    campos = ("titulo", "autor", "genero", "anio_publicacion")
    valores = {campo: datos.get(campo) for campo in campos}
    if any(valores[campo] in (None, "") for campo in campos):
        raise ValueError("Faltan campos obligatorios: titulo, autor, genero y anio_publicacion.")
    return valores


class LibroListResource(Resource):
    def get(self):
        return {"success": True, "data": listar_libros()}, 200

    def post(self):
        try:
            datos = datos_libro(request.get_json(silent=True))
            id_creado = crear_libro(**datos)
        except ValueError as error:
            return {"success": False, "error": str(error)}, 400
        return {
            "success": True,
            "message": "Libro creado correctamente.",
            "data": obtener_libro_por_id(id_creado),
        }, 201


class LibroResource(Resource):
    def get(self, id_libro):
        libro = obtener_libro_por_id(id_libro)
        if libro is None:
            return {"success": False, "error": "Libro no encontrado."}, 404
        return {"success": True, "data": libro}, 200

    def put(self, id_libro):
        try:
            datos = datos_libro(request.get_json(silent=True))
            if actualizar_libro(id_libro, **datos) == 0:
                return {"success": False, "error": "Libro no encontrado."}, 404
        except ValueError as error:
            return {"success": False, "error": str(error)}, 400
        return {
            "success": True,
            "message": "Libro actualizado correctamente.",
            "data": obtener_libro_por_id(id_libro),
        }, 200

    def delete(self, id_libro):
        if eliminar_libro(id_libro) == 0:
            return {"success": False, "error": "Libro no encontrado."}, 404
        return {"success": True, "message": "Libro eliminado correctamente."}, 200


api.add_resource(LibroListResource, "/books")
api.add_resource(LibroResource, "/books/<int:id_libro>")
