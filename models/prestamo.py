from database import conectar_db


def registrar_prestamo(id_libro, usuario, fecha_prestamo, fecha_devolucion=None, estado="activo"):
    usuario = (usuario or "").strip()
    if not usuario:
        raise ValueError("El usuario es obligatorio.")
    conexion = conectar_db()
    try:
        cursor = conexion.execute(
            """INSERT INTO prestamos
               (id_libro, usuario, fecha_prestamo, fecha_devolucion, estado)
               VALUES (?, ?, ?, ?, ?)""",
            (id_libro, usuario, fecha_prestamo, fecha_devolucion, estado),
        )
        conexion.commit()
        return cursor.lastrowid
    finally:
        conexion.close()


def listar_prestamos():
    conexion = conectar_db()
    try:
        filas = conexion.execute(
            """SELECT p.id, l.titulo AS libro, p.usuario, p.fecha_prestamo,
                      p.fecha_devolucion, p.estado
               FROM prestamos p JOIN libros l ON l.id = p.id_libro
               ORDER BY p.fecha_prestamo DESC"""
        ).fetchall()
        return [dict(fila) for fila in filas]
    finally:
        conexion.close()
