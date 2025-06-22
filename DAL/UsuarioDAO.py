import sqlite3
from .fitpalDB import get_connection

class Usuario:
    def __init__(self, id_usuario, nombre, apellido, email, contrasena, rol):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.contrasena = contrasena # Considerar hashear contraseñas en la BLL/GUI antes de pasarlas a DAL
        self.rol = rol

    def __str__(self):
        return f"ID: {self.id_usuario}, Nombre: {self.nombre} {self.apellido}, Email: {self.email}, Rol: {self.rol}"

class UsuarioDAO:
    def crear_usuario(self, usuario):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Usuario (nombre, apellido, email, contrasena, rol) VALUES (?, ?, ?, ?, ?)",
                           (usuario.nombre, usuario.apellido, usuario.email, usuario.contrasena, usuario.rol))
            conn.commit()
            return cursor.lastrowid # Retorna el ID del nuevo usuario
        except sqlite3.IntegrityError:
            print("Error: El email ya está registrado.")
            return None
        finally:
            conn.close()

    def obtener_usuario_por_credenciales(self, email, contrasena):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, nombre, apellido, email, contrasena, rol FROM Usuario WHERE email=? AND contrasena=?", (email, contrasena))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Usuario(*row)
        return None

    def obtener_usuario_por_id(self, id_usuario):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, nombre, apellido, email, contrasena, rol FROM Usuario WHERE id_usuario=?", (id_usuario,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Usuario(*row)
        return None

    def obtener_todos_los_clientes(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, nombre, apellido, email, contrasena, rol FROM Usuario WHERE rol='cliente'")
        rows = cursor.fetchall()
        conn.close()
        return [Usuario(*row) for row in rows]

    def actualizar_usuario(self, usuario):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE Usuario SET nombre=?, apellido=?, email=?, contrasena=?, rol=? WHERE id_usuario=?",
                           (usuario.nombre, usuario.apellido, usuario.email, usuario.contrasena, usuario.rol, usuario.id_usuario))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            return False
        finally:
            conn.close()
            
    def eliminar_usuario(self, id_usuario):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Usuario WHERE id_usuario=?", (id_usuario,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            return False
        finally:
            conn.close()