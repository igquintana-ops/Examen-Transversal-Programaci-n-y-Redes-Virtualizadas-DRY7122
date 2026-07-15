from flask import Flask, request
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash  # gestion de claves

DB = "usuarios.db"
app = Flask(__name__)


def crear_tabla():
    """Crea la tabla de usuarios si no existe (base de datos SQL)."""
    conexion = sqlite3.connect(DB)
    cursor = conexion.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS usuarios (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT UNIQUE NOT NULL,
               password_hash TEXT NOT NULL
           )"""
    )
    conexion.commit()
    conexion.close()


@app.route("/")
def inicio():
    return "Sitio web Examen Transversal DRY7122 - puerto 5800"


@app.route("/signup", methods=["POST"])
def signup():
    """Registra un usuario almacenando la contrasena en HASH."""
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return "Error: debe indicar username y password\n", 400

    password_hash = generate_password_hash(password)  # la clave se guarda hasheada

    try:
        conexion = sqlite3.connect(DB)
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO usuarios (username, password_hash) VALUES (?, ?)",
            (username, password_hash),
        )
        conexion.commit()
        conexion.close()
        return f"Usuario '{username}' registrado correctamente con clave en hash\n"
    except sqlite3.IntegrityError:
        return f"Error: el usuario '{username}' ya existe\n", 409


@app.route("/login", methods=["POST"])
def login():
    """Valida un usuario comparando el hash almacenado."""
    username = request.form.get("username")
    password = request.form.get("password")

    conexion = sqlite3.connect(DB)
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT password_hash FROM usuarios WHERE username = ?", (username,)
    )
    fila = cursor.fetchone()
    conexion.close()

    if fila and check_password_hash(fila[0], password):
        return f"Login CORRECTO para el usuario '{username}'\n"
    return f"Login INCORRECTO para el usuario '{username}'\n", 401


if __name__ == "__main__":
    crear_tabla()
    # El sitio web utiliza el puerto 5800 segun lo solicitado en el examen
    app.run(host="0.0.0.0", port=5800, debug=True)