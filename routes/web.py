from flask import Blueprint, render_template, request, redirect, url_for, abort
from models.libro import (
    listar_libros, buscar_libros, obtener_libro_por_id,
    crear_libro, actualizar_libro, eliminar_libro,
)
from models.prestamo import listar_prestamos
from models.descarga import listar_descargas

web_bp = Blueprint("web", __name__)


@web_bp.route("/")
def index():
    libros = listar_libros()
    return render_template("index.html", libros=libros, total_libros=len(libros))


@web_bp.route("/buscar")
def buscar():
    termino = request.args.get("q", "").strip()
    libros = buscar_libros(termino) if termino else listar_libros()
    return render_template("buscar.html", libros=libros, termino=termino)


@web_bp.route("/agregar", methods=["GET"])
def agregar_formulario():
    return render_template("agregar.html")


@web_bp.route("/agregar", methods=["POST"])
def agregar():
    datos = [request.form.get(campo, "") for campo in ("titulo", "autor", "genero", "anio_publicacion")]
    try:
        crear_libro(*datos)
    except ValueError as error:
        return render_template("agregar.html", error=str(error)), 400
    return redirect(url_for("web.index"))


@web_bp.route("/editar/<int:id_libro>", methods=["GET"])
def editar_formulario(id_libro):
    libro = obtener_libro_por_id(id_libro)
    if libro is None:
        abort(404)
    return render_template("editar.html", libro=libro)


@web_bp.route("/editar/<int:id_libro>", methods=["POST"])
def editar(id_libro):
    datos = [request.form.get(campo, "") for campo in ("titulo", "autor", "genero", "anio_publicacion")]
    try:
        actualizado = actualizar_libro(id_libro, *datos)
        if actualizado == 0:
            abort(404)
    except ValueError as error:
        libro = obtener_libro_por_id(id_libro)
        return render_template("editar.html", libro=libro, error=str(error)), 400
    return redirect(url_for("web.index"))


@web_bp.route("/eliminar/<int:id_libro>", methods=["POST"])
def eliminar(id_libro):
    if eliminar_libro(id_libro) == 0:
        abort(404)
    return redirect(url_for("web.index"))


@web_bp.route("/prestados")
def prestados():
    return render_template("prestados.html", prestamos=listar_prestamos())


@web_bp.route("/descargados")
def descargados():
    return render_template("descargados.html", descargas=listar_descargas())
