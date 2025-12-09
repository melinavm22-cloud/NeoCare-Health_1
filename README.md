# NeoCare Backend - Semana 1 - Preparación del entorno

# Iniciamos el entorno virtual para el proyecto
python -m venv venv

# Instalamos todas las librerías necesarias para el backend
pip install fastapi uvicorn[standard] sqlalchemy psycopg2-binary alembic passlib[bcrypt] python-jose[cryptography] pydantic

# Activamos el entorno virtual para que los paquetes se instalen localmente
venv\Scripts\activate
# En caso de error porque PowerShell tiene bloqueada la ejecución de scripts, hacer 
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
# Y volver a ejecutar 
venv\Scripts\activate


# Verficamos la correcta instalación de Python y pip 
python --version
pip --version

# Instalamos librerías y todo lo necesario para el backend (servidor, base de datos, autenticación, migraciones, etc)
pip install fastapi uvicorn[standard] sqlalchemy psycopg2-binary alembic passlib[bcrypt] python-jose[cryptography] pydantic

# Creamos la carpeta principal
mkdir app
cd app

# Creamos subcarpetas para organizar el código en módulos: configuración, modelos, validaciones y rutas.
mkdir core
mkdir models
mkdir schemas
mkdir routers


# Creamos el archivo principal
New-Item main.py


# Rellenamos el archivo main.py con lo siguiente
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "NeoCare Backend funcionando 🚀"}

# Tras esto, levantamos el servidor
python -m uvicorn app.main:app --reload


# Error (UnknownHashError: bcrypt) con el esquema de contraseñas. Causa: Los usuarios estaban registrados con sha256_crypt, pero el código estaba configurado con bcrypt. Solución: En auth.py cambiamos:
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

# Error 500 al crear un tablero. El modelo Board tenía la columna name, pero el endpoint intentaba crear con title. Solución: Unificamos el modelo y la base de datos para que usaran title.
PostgreSQL (ALTER TABLE boards RENAME COLUMN name TO title;)
En board.py cambiamos name → title
En boards.py usamos Board(title=board.title, ...).

# Internal Server Error 500 persistente al crear tablero. Causa: El modelo y la tabla no estaban sincronizados. Solución: Confirmamos que la tabla en SQL ya tenía title. Ajustamos el modelo Board y el esquema Pydantic BoardCreate para usar title. Después de esto, el endpoint funcionó. 


# Prueba exitosa de creación de tablero y confirmación de que el endpoint POST /boards/ funcionaba correctamente.
{
  "id": 1,
  "user_id": 1,
  "title": "Proyecto NeoCare"
}

# Implementación de la tarea opcional. Añadimos en auth.py la lógica para crear un tablero por defecto al registrar usuario:
default_board = Board(title="Mi primer tablero", user_id=new_user.id)
db.add(default_board)
db.commit()
db.refresh(default_board)

# Prueba. Registramos un nuevo usuario y la respuesta devolvió lo siguiente, por lo que confirmamos que el tablero por defecto se crea automáticamente.
{
  "msg": "Usuario registrado",
  "id": 5,
  "default_board_id": 2
}

# Prueba de listado de tableros. Confirmamos que el tablero por defecto aparece vinculado al nuevo usuario.
[
  {
    "id": 2,
    "user_id": 5,
    "title": "Mi primer tablero"
  }
]



# Links plataforma:
http://127.0.0.1:8000/

http://127.0.0.1:8000/docs
