from database import conectar_db


def _validar_datos(titulo, autor, genero, anio_publicacion):
    titulo = (titulo or "").strip()
    autor = (autor or "").strip()
    genero = (genero or "").strip()
    if not titulo or not autor or not genero:
        raise ValueError("Título, autor y género son obligatorios.")
    try:
        anio_publicacion = int(anio_publicacion)
    except (TypeError, ValueError):
        raise ValueError("El año de publicación debe ser un número válido.")
    return titulo, autor, genero, anio_publicacion


def crear_libro(titulo, autor, genero, anio_publicacion):
    datos = _validar_datos(titulo, autor, genero, anio_publicacion)
    conexion = conectar_db()
    try:
        cursor = conexion.execute(
            "INSERT INTO libros (titulo, autor, genero, anio_publicacion) VALUES (?, ?, ?, ?)",
            datos,
        )
        conexion.commit()
        return cursor.lastrowid
    finally:
        conexion.close()


def listar_libros():
    conexion = conectar_db()
    try:
        filas = conexion.execute(
            "SELECT id, titulo, autor, genero, anio_publicacion FROM libros ORDER BY titulo"
        ).fetchall()
        return [dict(fila) for fila in filas]
    finally:
        conexion.close()


def buscar_libros(termino):
    criterio = f"%{termino.strip()}%"
    conexion = conectar_db()
    try:
        filas = conexion.execute(
            """SELECT id, titulo, autor, genero, anio_publicacion FROM libros
               WHERE titulo LIKE ? OR autor LIKE ? OR genero LIKE ? ORDER BY titulo""",
            (criterio, criterio, criterio),
        ).fetchall()
        return [dict(fila) for fila in filas]
    finally:
        conexion.close()


def obtener_libro_por_id(id_libro):
    conexion = conectar_db()
    try:
        fila = conexion.execute("SELECT * FROM libros WHERE id = ?", (id_libro,)).fetchone()
        return dict(fila) if fila else None
    finally:
        conexion.close()


def actualizar_libro(id_libro, titulo, autor, genero, anio_publicacion):
    datos = _validar_datos(titulo, autor, genero, anio_publicacion)
    conexion = conectar_db()
    try:
        cursor = conexion.execute(
            """UPDATE libros SET titulo = ?, autor = ?, genero = ?, anio_publicacion = ?
               WHERE id = ?""",
            (*datos, id_libro),
        )
        conexion.commit()
        return cursor.rowcount
    finally:
        conexion.close()


def eliminar_libro(id_libro):
    conexion = conectar_db()
    try:
        conexion.execute("DELETE FROM prestamos WHERE id_libro = ?", (id_libro,))
        conexion.execute("DELETE FROM descargas WHERE id_libro = ?", (id_libro,))
        cursor = conexion.execute("DELETE FROM libros WHERE id = ?", (id_libro,))
        conexion.commit()
        return cursor.rowcount
    finally:
        conexion.close()
