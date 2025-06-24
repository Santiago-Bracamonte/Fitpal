import sqlite3
from .fitpalDB import get_connection
from .RutinaDAO import Rutina  
from .EjercicioDAO import Ejercicio 

class RutinaEjercicio:
    """
    Representa una entrada en la tabla intermedia Rutina_Ejercicio.
    No es un objeto que tenga lógica compleja, solo asocia IDs.
    """
    def __init__(self, id_rutina_ejercicio, fk_rutina, fk_ejercicio):
        self.id_rutina_ejercicio = id_rutina_ejercicio 
        self.fk_rutina = fk_rutina
        self.fk_ejercicio = fk_ejercicio

    def __str__(self):
        return f"Asociación ID: {self.id_rutina_ejercicio}, Rutina ID: {self.fk_rutina}, Ejercicio ID: {self.fk_ejercicio}"

class RutinaEjercicioDAO:

    def __init__(self):
        pass 

    def asociar_ejercicio_a_rutina(self, fk_rutina, fk_ejercicio):
        """
        Asocia un ejercicio existente a una rutina existente.
        Retorna el ID de la nueva asociación si es exitosa, None si falla (ej. duplicado).
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id_rutina_ejercicio FROM Rutina_Ejercicio WHERE fk_rutina = ? AND fk_ejercicio = ?",
                           (fk_rutina, fk_ejercicio))
            if cursor.fetchone():
                return None
            
            cursor.execute("INSERT INTO Rutina_Ejercicio (fk_rutina, fk_ejercicio) VALUES (?, ?)",
                           (fk_rutina, fk_ejercicio))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            print(f"Error de integridad al asociar ejercicio a rutina: {e}")
            return None
        except Exception as e:
            print(f"Error al asociar ejercicio a rutina: {e}")
            return None
        finally:
            conn.close()

    def desasociar_ejercicio_de_rutina(self, fk_rutina, fk_ejercicio):
        """
        Desasocia un ejercicio de una rutina específica.
        Retorna True si la desasociación fue exitosa, False en caso contrario.
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Rutina_Ejercicio WHERE fk_rutina = ? AND fk_ejercicio = ?",
                           (fk_rutina, fk_ejercicio))
            conn.commit()
            if cursor.rowcount > 0:
                return True
            else:
                return False
        except Exception as e:
            print(f"Error al desasociar ejercicio de rutina: {e}")
            return False
        finally:
            conn.close()

    def obtener_ejercicios_de_rutina(self, id_rutina):
        """
        Obtiene todos los ejercicios asociados a una rutina específica.
        Retorna una lista de objetos Ejercicio.
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT 
                    E.id_ejercicio, E.nombre, E.tipo, E.repeticiones, E.series, E.descripcion
                FROM 
                    Rutina_Ejercicio RE
                JOIN 
                    Ejercicio E ON RE.fk_ejercicio = E.id_ejercicio
                WHERE 
                    RE.fk_rutina = ?
                ORDER BY E.nombre
            """, (id_rutina,))
            rows = cursor.fetchall()
            conn.close()

            ejercicios_list = []
            for row in rows:
                ejercicio_obj = Ejercicio(row[0], row[1], row[2], row[3], row[4], row[5])
                ejercicios_list.append(ejercicio_obj)
            
            return ejercicios_list
        except Exception as e:
            print(f"Error en obtener_ejercicios_de_rutina (DAO): {e}")
            conn.close()
            return [] 
    
    def obtener_rutinas_de_ejercicio(self, id_ejercicio):
        """
        Obtiene todas las rutinas a las que un ejercicio específico está asociado.
        Retorna una lista de objetos Rutina.
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT 
                    R.id_rutina, R.nombre, R.descripcion, R.duracion
                FROM 
                    Rutina_Ejercicio RE
                JOIN 
                    Rutina R ON RE.fk_rutina = R.id_rutina
                WHERE 
                    RE.fk_ejercicio = ?
                ORDER BY R.nombre
            """, (id_ejercicio,))
            rows = cursor.fetchall()
            conn.close()

            rutinas_list = []
            for row in rows:
                rutina_obj = Rutina(row[0], row[1], row[2], row[3])
                rutinas_list.append(rutina_obj)
            
            return rutinas_list
        except Exception as e:
            print(f"Error en obtener_rutinas_de_ejercicio (DAO): {e}")
            conn.close()
            return [] 
            
    def eliminar_asociaciones_por_rutina(self, id_rutina):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Rutina_Ejercicio WHERE fk_rutina=?", (id_rutina,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar asociaciones de rutina: {e}")
            return False
        finally:
            conn.close()

    def eliminar_asociaciones_por_ejercicio(self, id_ejercicio):
        """
        Elimina todas las asociaciones de rutinas para un ejercicio específico.
        Útil cuando se elimina un ejercicio.
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Rutina_Ejercicio WHERE fk_ejercicio = ?", (id_ejercicio,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar asociaciones por ejercicio: {e}")
            return False
        finally:
            conn.close()