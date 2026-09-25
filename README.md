# Los Libros del Día

Aplicación web para gestionar una biblioteca con Flask, SQLite y Flask-RESTful.

## Funcionalidades

- Listado de libros.
- Búsqueda por título, autor o género.
- Alta, edición y eliminación de libros.
- Historial de préstamos.
- Registro de descargas.
- API RESTful para gestionar libros.

## Instalación

```bash
python -m venv .venv
# Windows PowerShell
.venv\\Scripts\\Activate.ps1
# Linux/macOS
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

```bash
python app.py
```

La base de datos `biblioteca.db` se crea automáticamente con tres tablas y datos de prueba.

URLs:

- Aplicación web: http://localhost:5000
- API: http://localhost:5000/api/books

## API

```bash
curl http://localhost:5000/api/books
curl http://localhost:5000/api/books/1

curl -X POST http://localhost:5000/api/books \\
  -H "Content-Type: application/json" \\
  -d '{"titulo":"Prueba API","autor":"Autor Demo","genero":"Novela","anio_publicacion":2025}'

curl -X PUT http://localhost:5000/api/books/1 \\
  -H "Content-Type: application/json" \\
  -d '{"titulo":"Nuevo título","autor":"Nuevo autor","genero":"Drama","anio_publicacion":2024}'

curl -X DELETE http://localhost:5000/api/books/1
```

## Verificación

- La base de datos se inicializa automáticamente.
- Se crean `libros`, `prestamos` y `descargas`.
- Se cargan cinco libros, tres préstamos y tres descargas.
- La interfaz web permite consultar y administrar los libros.
- La API responde con JSON estructurado y errores HTTP básicos.
