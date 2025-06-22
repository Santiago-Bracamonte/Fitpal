
import sqlite3
from .fitpalDB import get_connection

class Ejercicio:
    def __init__(self, id_ejercicio, nombre, tipo, repeticiones, series, descripcion):
        self.id_ejercicio = id_ejercicio
        self.nombre = nombre
        self.tipo = tipo
        self.repeticiones = repeticiones
        self.series = series
        self.descripcion = descripcion

    def __str__(self):
        return f"ID: {self.id_ejercicio}, Nombre: {self.nombre}, Tipo: {self.tipo}"
    
    def __eq__(self, other):
        if not isinstance(other, Ejercicio):
            return NotImplemented
        return (self.id_ejercicio == other.id_ejercicio and
                self.nombre == other.nombre and
                self.tipo == other.tipo and
                self.repeticiones == other.repeticiones and
                self.series == other.series and
                self.descripcion == other.descripcion)

    def __hash__(self): # Necesario si vas a usar Ejercicio en sets o como claves de diccionario
        return hash((self.id_ejercicio, self.nombre, self.tipo, self.repeticiones, self.series, self.descripcion))

class EjercicioDAO:
    def crear_ejercicio(self, nombre, tipo, repeticiones, series, descripcion): # <-- CAMBIADA LA FIRMA
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Ejercicio (nombre, tipo, repeticiones, series, descripcion) VALUES (?, ?, ?, ?, ?)",
                           (nombre, tipo, repeticiones, series, descripcion)) # <-- Los parámetros individuales se usan directamente
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error al crear ejercicio: {e}")
            return None
        finally:
            conn.close()

    def obtener_ejercicio_por_id(self, id_ejercicio):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_ejercicio, nombre, tipo, repeticiones, series, descripcion FROM Ejercicio WHERE id_ejercicio=?", (id_ejercicio,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Ejercicio(*row)
        return None
    
    def obtener_por_nombre_tipo(self, nombre, tipo):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_ejercicio, nombre, tipo, repeticiones, series, descripcion FROM Ejercicio WHERE nombre = ? AND tipo = ?", (nombre, tipo))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Ejercicio(*row)
        return None

    def obtener_todos_los_ejercicios(self): # O get_all, según como lo tengas nombrado
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_ejercicio, nombre, tipo, repeticiones, series, descripcion FROM Ejercicio")
        rows = cursor.fetchall()
        conn.close()
        lista_ejercicios_objetos = [Ejercicio(*row) for row in rows]
        return lista_ejercicios_objetos

    def actualizar_ejercicio(self, ejercicio):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE Ejercicio SET nombre=?, tipo=?, repeticiones=?, series=?, descripcion=? WHERE id_ejercicio=?",
                           (ejercicio.nombre, ejercicio.tipo, ejercicio.repeticiones, ejercicio.series, ejercicio.descripcion, ejercicio.id_ejercicio))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al actualizar ejercicio: {e}")
            return False
        finally:
            conn.close()

    def eliminar_ejercicio(self, id_ejercicio):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Ejercicio WHERE id_ejercicio=?", (id_ejercicio,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar ejercicio: {e}")
            return False
        finally:
            conn.close()

class RutinaEjercicioDAO:
    def agregar_ejercicio_a_rutina(self, fk_rutina, fk_ejercicio):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Rutina_Ejercicio (fk_rutina, fk_ejercicio) VALUES (?, ?)",
                           (fk_rutina, fk_ejercicio))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"Error: El ejercicio {fk_ejercicio} ya está en la rutina {fk_rutina}.")
            return None
        except Exception as e:
            print(f"Error al agregar ejercicio a rutina: {e}")
            return None
        finally:
            conn.close()

    def obtener_ejercicios_de_rutina(self, fk_rutina):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT E.id_ejercicio, E.nombre, E.tipo, E.repeticiones, E.series, E.descripcion
            FROM Ejercicio E
            JOIN Rutina_Ejercicio RE ON E.id_ejercicio = RE.fk_ejercicio
            WHERE RE.fk_rutina = ?
        """, (fk_rutina,))
        rows = cursor.fetchall()
        conn.close()
        return [Ejercicio(*row) for row in rows]

    def eliminar_ejercicio_de_rutina(self, fk_rutina, fk_ejercicio):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Rutina_Ejercicio WHERE fk_rutina=? AND fk_ejercicio=?",
                           (fk_rutina, fk_ejercicio))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar ejercicio de rutina: {e}")
            return False
        finally:
            conn.close()

    def _insertar_ejercicios_iniciales(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM Ejercicio")
            count = cursor.fetchone()[0]

            if count == 0: # Solo insertar si la tabla está vacía
                ejercicios_para_insertar = [
                    ("Press de Banca", "Pecho", 10, 4, "Ejercicio fundamental para el desarrollo del pecho, tríceps y hombros."),
                    ("Sentadilla", "Piernas", 8, 3, "Ejercicio compuesto para el tren inferior, fortalece cuádriceps, glúteos e isquiotibiales."),
                    ("Peso Muerto", "Espalda", 5, 3, "Ejercicio de fuerza completo que trabaja la espalda baja, glúteos, isquiotibiales y antebrazos."),
                    ("Dominadas", "Espalda", 5, 3, "Ejercicio de peso corporal que fortalece la espalda alta y bíceps."),
                    ("Press Militar con Barra", "Hombros", 8, 4, "Ejercicio para el desarrollo de los deltoides y tríceps."),
                    ("Remo con Barra", "Espalda", 10, 4, "Ejercicio que trabaja los músculos de la espalda media y alta."),
                    ("Curl de Bíceps con Barra", "Brazos", 12, 3, "Ejercicio de aislamiento para los bíceps."),
                    ("Press Francés", "Brazos", 10, 3, "Ejercicio de aislamiento para los tríceps."),
                    ("Elevaciones Laterales", "Hombros", 15, 3, "Ejercicio para aislar los deltoides laterales y dar amplitud a los hombros."),
                    ("Extensiones de Cuádriceps", "Piernas", 15, 3, "Ejercicio de aislamiento para los cuádriceps."),
                    ("Curl de Isquiotibiales", "Piernas", 15, 3, "Ejercicio de aislamiento para los isquiotibiales."),
                    ("Plancha Abdominal", "Core", None, 3, "Ejercicio isométrico para fortalecer el core. Mantener 30-60 segundos por serie."),
                    ("Crunch Abdominal", "Core", 20, 3, "Ejercicio clásico para trabajar los abdominales superiores."),
                    ("Flexiones de Brazos", "Pecho", 15, 3, "Ejercicio de peso corporal que trabaja pecho, hombros y tríceps."),
                    ("Zancadas", "Piernas", 10, 3, "Ejercicio unilateral para el tren inferior, mejora el equilibrio y la fuerza."),
                    ("Remo en Punta", "Espalda", 12, 3, "Variación de remo que enfatiza la parte superior de la espalda y los trapecios."),
                    ("Press de Hombros con Mancuernas", "Hombros", 10, 3, "Ejercicio para hombros, permite un mayor rango de movimiento que con barra."),
                    ("Fondos en Paralelas", "Pecho", 8, 3, "Ejercicio compuesto para pecho inferior y tríceps."),
                    ("Hip Thrust", "Glúteos", 12, 4, "Ejercicio potente para el desarrollo de glúteos y cadena posterior."),
                    ("Sentadilla Búlgara", "Piernas", 8, 3, "Ejercicio unilateral avanzado para piernas y glúteos, mejora el equilibrio.")
                ]

                for ej in ejercicios_para_insertar:
                    nombre, tipo, repeticiones, series, descripcion = ej
                    cursor.execute("INSERT INTO Ejercicio (nombre, tipo, repeticiones, series, descripcion) VALUES (?, ?, ?, ?, ?)",
                                   (nombre, tipo, repeticiones, series, descripcion))
                conn.commit()
                print("Ejercicios iniciales insertados con éxito.")
            else:
                print("La tabla de ejercicios ya contiene datos, no se insertaron ejercicios iniciales.")
        except Exception as e:
            print(f"Error al insertar ejercicios iniciales: {e}")
        finally:
            conn.close()