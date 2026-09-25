from database import conectar_db


def registrar_descarga(id_libro, fecha_descarga, formato):
    formato = (formato or "").strip()
    if not formato:
        raise ValueError("El formato es obligatorio.")
    conexion = conectar_db()
    try:
        cursor = conexion.execute(
            "INSERT INTO descargas (id_libro, fecha_descarga, formato) VALUES (?, ?, ?)",
            (id_libro, fecha_descarga, formato),
        )
        conexion.commit()
        return cursor.lastrowid
    finally:
        conexion.close()


def listar_descargas():
    conexion = conectar_db()
    try:
        filas = conexion.execute(
            """SELECT d.id, l.titulo AS libro, d.fecha_descarga, d.formato
               FROM descargas d JOIN libros l ON l.id = d.id_libro
               ORDER BY d.fecha_descarga DESC"""
        ).fetchall()
        return [dict(fila) for fila in filas]
    finally:
        conexion.close()
