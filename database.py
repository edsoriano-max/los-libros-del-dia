import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "biblioteca.db"


def conectar_db():
    conexion = sqlite3.connect(DB_PATH)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def crear_tablas():
    conexion = conectar_db()
    try:
        conexion.executescript("""
            CREATE TABLE IF NOT EXISTS libros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo VARCHAR(200) NOT NULL,
                autor VARCHAR(150) NOT NULL,
                genero VARCHAR(100) NOT NULL,
                anio_publicacion INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS prestamos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_libro INTEGER NOT NULL,
                usuario VARCHAR(150) NOT NULL,
                fecha_prestamo DATE NOT NULL,
                fecha_devolucion DATE NULL,
                estado VARCHAR(30) NOT NULL DEFAULT 'activo',
                FOREIGN KEY (id_libro) REFERENCES libros(id)
            );

            CREATE TABLE IF NOT EXISTS descargas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_libro INTEGER NOT NULL,
                fecha_descarga DATE NOT NULL,
                formato VARCHAR(20) NOT NULL,
                FOREIGN KEY (id_libro) REFERENCES libros(id)
            );
        """)

        if conexion.execute("SELECT COUNT(*) FROM libros").fetchone()[0] == 0:
            libros = [
                ("El Quijote", "Miguel de Cervantes", "Clásico", 1605),
                ("1984", "George Orwell", "Distopía", 1949),
                ("La metamorfosis", "Franz Kafka", "Ficción", 1915),
                ("Don Juan Tenorio", "José Zorrilla", "Teatro", 1844),
                ("Cien años de soledad", "Gabriel García Márquez", "Realismo mágico", 1967),
            ]
            conexion.executemany(
                "INSERT INTO libros (titulo, autor, genero, anio_publicacion) VALUES (?, ?, ?, ?)",
                libros,
            )

        if conexion.execute("SELECT COUNT(*) FROM prestamos").fetchone()[0] == 0:
            conexion.executemany(
                """INSERT INTO prestamos
                   (id_libro, usuario, fecha_prestamo, fecha_devolucion, estado)
                   VALUES (?, ?, ?, ?, ?)""",
                [
                    (1, "Ana López", "2025-09-01", "2025-09-12", "devuelto"),
                    (2, "Carlos Ruiz", "2025-09-15", None, "activo"),
                    (3, "María García", "2025-09-20", None, "activo"),
                ],
            )

        if conexion.execute("SELECT COUNT(*) FROM descargas").fetchone()[0] == 0:
            conexion.executemany(
                "INSERT INTO descargas (id_libro, fecha_descarga, formato) VALUES (?, ?, ?)",
                [(1, "2025-09-05", "PDF"), (3, "2025-09-18", "EPUB"), (5, "2025-09-22", "MOBI")],
            )

        conexion.commit()
    finally:
        conexion.close()


def inicializar_base_datos():
    crear_tablas()
