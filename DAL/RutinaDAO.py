from .fitpalDB import get_connection

class Rutina:
    def __init__(self, id_rutina, nombre, descripcion, duracion):
        self.id_rutina = id_rutina
        self.nombre = nombre
        self.descripcion = descripcion
        self.duracion = duracion

    def __str__(self):
        return f"ID: {self.id_rutina}, Nombre: {self.nombre}, Duración: {self.duracion}"

    def __eq__(self, other):
        if not isinstance(other, Rutina):
            return NotImplemented
        return (self.id_rutina == other.id_rutina and
                self.nombre == other.nombre and
                self.descripcion == other.descripcion and
                self.duracion == other.duracion)

    def __hash__(self):
        return hash((self.id_rutina, self.nombre, self.descripcion, self.duracion))

    def __str__(self):
        return f"ID: {self.id_rutina}, Nombre: {self.nombre}, Duración: {self.duracion}"
    
class RutinaDAO:
    def crear_rutina(self, rutina):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Rutina (nombre, descripcion, duracion) VALUES (?, ?, ?)",
                           (rutina.nombre, rutina.descripcion, rutina.duracion))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error al crear rutina: {e}")
            return None
        finally:
            conn.close()

    def obtener_rutina_por_id(self, id_rutina):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_rutina, nombre, descripcion, duracion FROM Rutina WHERE id_rutina=?", (id_rutina,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Rutina(*row)
        return None

    def obtener_todas_las_rutinas(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_rutina, nombre, descripcion, duracion FROM Rutina")
        rows = cursor.fetchall()
        conn.close()
        return [Rutina(*row) for row in rows]

    def actualizar_rutina(self, rutina):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE Rutina SET nombre=?, descripcion=?, duracion=? WHERE id_rutina=?",
                           (rutina.nombre, rutina.descripcion, rutina.duracion, rutina.id_rutina))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al actualizar rutina: {e}")
            return False
        finally:
            conn.close()

    def eliminar_rutina(self, id_rutina):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Rutina WHERE id_rutina=?", (id_rutina,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar rutina: {e}")
            return False
        finally:
            conn.close()

    def obtener_rutina_por_nombre(self, nombre):
        """
        Obtiene una rutina de la base de datos por su nombre.
        Retorna un objeto Rutina si la encuentra, None en caso contrario.
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id_rutina, nombre, descripcion, duracion FROM Rutina WHERE nombre = ?", (nombre,))
            row = cursor.fetchone()
            conn.close() 

            if row:
                return Rutina(row[0], row[1], row[2], row[3])
            return None 
        except Exception as e:
            print(f"Error al obtener rutina por nombre: {e}")
            if conn:
                conn.close()
            return None