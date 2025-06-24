# asignacion_rutina.py (en la carpeta DAL)
import sqlite3
from .fitpalDB import get_connection
from .RutinaDAO import Rutina
from .UsuarioDAO import Usuario
import datetime

class AsignacionRutina:
    def __init__(self, id_asignacion_rutina, fk_usuario, fk_rutina, fecha_asignado, fk_entrenador):
        self.id_asignacion_rutina = id_asignacion_rutina
        self.fk_usuario = fk_usuario
        self.fk_rutina = fk_rutina
        self.fecha_asignado = fecha_asignado 
        self.fk_entrenador = fk_entrenador

    def __str__(self):
        return f"ID Asignación: {self.id_asignacion_rutina}, Usuario: {self.fk_usuario}, Rutina: {self.fk_rutina}, Fecha: {self.fecha_asignado}"

class AsignacionRutinaDAO:
    def asignar_rutina(self, fk_usuario, fk_rutina, fk_entrenador, fecha_asignado=None): 
        if fecha_asignado is None:
            fecha_asignado = datetime.date.today().strftime('%Y-%m-%d') # Formato 'YYYY-MM-DD'

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Asignacion_Rutina (fk_usuario, fk_rutina, fk_entrenador, fecha_asignado) VALUES (?, ?, ?, ?)",
                           (fk_usuario, fk_rutina, fk_entrenador, fecha_asignado)) 
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            print("Error: Esta rutina ya está asignada a este usuario en esta fecha.")
            return None
        except Exception as e:
            print(f"Error al asignar rutina: {e}")
            return None
        finally:
            conn.close()

    def obtener_rutinas_asignadas_a_usuario(self, fk_usuario, fk_rutina=None, fecha=None): 
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                AR.id_asignacion_rutina, 
                AR.fk_usuario, 
                AR.fk_rutina, 
                AR.fecha_asignado,
                AR.fk_entrenador,  -- ¡AGREGADO ESTO!
                R.nombre, R.descripcion, R.duracion
            FROM Asignacion_Rutina AR
            JOIN Rutina R ON AR.fk_rutina = R.id_rutina
            WHERE AR.fk_usuario = ?
            ORDER BY AR.fecha_asignado DESC
        """, (fk_usuario,)) 

        rows = cursor.fetchall()
        conn.close()
        
        resultados = []
        for row in rows:
            
            
            asignacion = AsignacionRutina(row[0], row[1], row[2], row[3], row[4]) 
            rutina = Rutina(row[2], row[5], row[6], row[7]) 
            resultados.append({'asignacion': asignacion, 'rutina': rutina})
        return resultados


    def obtener_clientes_con_rutina_asignada(self, fk_rutina):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT U.id_usuario, U.nombre, U.apellido, U.email, U.contrasena, U.rol, AR.fecha_asignado
            FROM Usuario U
            JOIN Asignacion_Rutina AR ON U.id_usuario = AR.fk_usuario
            WHERE AR.fk_rutina = ?
            ORDER BY AR.fecha_asignado DESC
        """, (fk_rutina,))
        rows = cursor.fetchall()
        conn.close()
        
        resultados = []
        for row in rows:
            usuario = Usuario(row[0], row[1], row[2], row[3], row[4], row[5])
            fecha_asignado = row[6]
            resultados.append({'usuario': usuario, 'fecha_asignado': fecha_asignado})
        return resultados

    def eliminar_asignacion_rutina(self, id_asignacion_rutina):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Asignacion_Rutina WHERE id_asignacion_rutina=?", (id_asignacion_rutina,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar asignación: {e}")
            return False
        finally:
            conn.close()

    def obtener_asignaciones_por_entrenador(self, id_entrenador):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT
                    AR.id_asignacion_rutina,
                    AR.fk_usuario,
                    U.nombre AS nombre_cliente,
                    U.apellido AS apellido_cliente,
                    AR.fk_rutina,
                    R.nombre AS nombre_rutina,
                    R.descripcion AS descripcion_rutina,
                    AR.fecha_asignado,
                    AR.fk_entrenador -- Asegúrate de que esta columna esté seleccionada si la necesitas
                FROM Asignacion_Rutina AS AR
                JOIN Usuario AS U ON AR.fk_usuario = U.id_usuario
                JOIN Rutina AS R ON AR.fk_rutina = R.id_rutina
                WHERE AR.fk_entrenador = ?
                ORDER BY AR.fecha_asignado DESC
            """, (id_entrenador,))
            
            assignments = []
            for row in cursor.fetchall():
                assignments.append({
                    "id_asignacion_rutina": row[0],
                    "fk_usuario": row[1],
                    "nombre_cliente": row[2],
                    "apellido_cliente": row[3],
                    "fk_rutina": row[4],
                    "nombre_rutina": row[5],
                    "descripcion_rutina": row[6],
                    "fecha_asignado": row[7],
                    "fk_entrenador": row[8] 
                })
            return assignments
        except sqlite3.Error as e:
            print(f"Error en obtener_asignaciones_por_entrenador (DAO): {e}")
            return [] 
        finally:
            conn.close()

    def obtener_asignaciones_y_rutinas_por_cliente(self, id_cliente):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT
                    AR.id_asignacion_rutina,
                    AR.fk_usuario,
                    U.nombre AS nombre_cliente,
                    U.apellido AS apellido_cliente,
                    AR.fk_rutina,
                    R.nombre AS nombre_rutina,
                    R.descripcion AS descripcion_rutina,
                    AR.fecha_asignado,
                    AR.fk_entrenador -- Selecciona también este campo si lo necesitas
                FROM Asignacion_Rutina AS AR
                JOIN Usuario AS U ON AR.fk_usuario = U.id_usuario
                JOIN Rutina AS R ON AR.fk_rutina = R.id_rutina
                WHERE AR.fk_usuario = ?
                ORDER BY AR.fecha_asignado DESC
            """, (id_cliente,))
            
            data = []
            for row in cursor.fetchall():
                data.append({
                    "id_asignacion_rutina": row[0],
                    "fk_usuario": row[1],
                    "nombre_cliente": row[2],
                    "apellido_cliente": row[3],
                    "id_rutina": row[4],
                    "nombre_rutina": row[5],
                    "descripcion_rutina": row[6],
                    "fecha_asignado": row[7],
                    "fk_entrenador": row[8] 
                })
            return data
        except sqlite3.Error as e:
            print(f"Error en obtener_asignaciones_y_rutinas_por_cliente (DAO): {e}")
            return [] 
        finally:
            conn.close()






