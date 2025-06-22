# conexion_bd.py
import sqlite3

DATABASE_NAME = "fitpal.db"

def get_connection():
    """Establece y retorna una conexión a la base de datos."""
    return sqlite3.connect(DATABASE_NAME)

def crear_tablas():
    """Crea las tablas de la base de datos si no existen."""
    conn = get_connection()
    cursor = conn.cursor()

    # Tabla Usuario
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Usuario (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL,
            rol TEXT NOT NULL -- 'entrenador' o 'cliente'
        );
    ''')

    # Tabla Rutina
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Rutina (
            id_rutina INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            duracion TEXT -- Puedes ajustar el tipo de dato si es un número de minutos, por ejemplo
        );
    ''')

    # Tabla Ejercicio
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Ejercicio (
            id_ejercicio INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo TEXT,
            repeticiones INTEGER,
            series INTEGER,
            descripcion TEXT
        );
    ''')

    # Tabla Rutina_Ejercicio - UNIQUE para evitar que se dupliquen los ejercicios en la rutina
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Rutina_Ejercicio (
            id_rutina_ejercicio INTEGER PRIMARY KEY AUTOINCREMENT,
            fk_rutina INTEGER NOT NULL,
            fk_ejercicio INTEGER NOT NULL,
            FOREIGN KEY (fk_rutina) REFERENCES Rutina(id_rutina),
            FOREIGN KEY (fk_ejercicio) REFERENCES Ejercicio(id_ejercicio),
            UNIQUE(fk_rutina, fk_ejercicio) 
        );
    ''')

    # Tabla Asignacion_Rutina - UNIQUE para que un usuario no pueda tener la misma rutina asignada en la misma fecha
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Asignacion_Rutina (
        id_asignacion_rutina INTEGER PRIMARY KEY AUTOINCREMENT,
        fk_usuario INTEGER NOT NULL,
        fk_rutina INTEGER NOT NULL,
        fecha_asignado DATE NOT NULL,
        fk_entrenador INTEGER, -- Asegúrate de que esta línea esté presente
        FOREIGN KEY (fk_usuario) REFERENCES Usuario(id_usuario),
        FOREIGN KEY (fk_rutina) REFERENCES Rutina(id_rutina),
        FOREIGN KEY (fk_entrenador) REFERENCES Usuario(id_usuario),
        UNIQUE(fk_usuario, fk_rutina, fecha_asignado)
    );
''')

    conn.commit()
    conn.close()

