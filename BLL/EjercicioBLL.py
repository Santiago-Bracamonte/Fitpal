
from DAL.EjercicioDAO import EjercicioDAO
from DAL.EjercicioDAO import Ejercicio

class EjercicioBLL:
    def __init__(self):
        self.ejercicio_dao = EjercicioDAO() 
        

    def crear_nuevo_ejercicio(self, nombre, tipo, repeticiones=None, series=None, descripcion=None):
        """
        Crea un nuevo ejercicio. Realiza validaciones básicas.
        Retorna el objeto Ejercicio si es exitoso, False en caso contrario.
        """
        if not nombre or not tipo:
            print("Error BLL (Ejercicio): El nombre y el tipo del ejercicio son obligatorios.")
            return False

        if repeticiones is not None and not isinstance(repeticiones, int) or (repeticiones is not None and repeticiones < 0):
            print("Error BLL (Ejercicio): Repeticiones debe ser un número entero positivo.")
            return False
        if series is not None and not isinstance(series, int) or (series is not None and series < 0):
            print("Error BLL (Ejercicio): Series debe ser un número entero positivo.")
            return False
            
    

        return self.ejercicio_dao.crear_ejercicio(nombre, tipo, repeticiones, series, descripcion)

    def modificar_ejercicio_existente(self, id_ejercicio, nombre=None, tipo=None, repeticiones=None, series=None, descripcion=None):
        """
        Modifica un ejercicio existente.
        Retorna True si la modificación fue exitosa, False en caso contrario.
        """
        if not id_ejercicio:
            print("Error BLL (Ejercicio): El ID del ejercicio es obligatorio para modificar.")
            return False

        ejercicio_existente = self.ejercicio_dao.obtener_ejercicio_por_id(id_ejercicio)
        if not ejercicio_existente:
            print(f"Error BLL (Ejercicio): Ejercicio con ID {id_ejercicio} no encontrado.")
            return False

        if nombre is not None and not nombre:
            print("Error BLL (Ejercicio): El nombre no puede estar vacío.")
            return False
        if tipo is not None and not tipo:
            print("Error BLL (Ejercicio): El tipo no puede estar vacío.")
            return False

        if repeticiones is not None and not isinstance(repeticiones, int) or (repeticiones is not None and repeticiones < 0):
            print("Error BLL (Ejercicio): Repeticiones debe ser un número entero positivo.")
            return False
        if series is not None and not isinstance(series, int) or (series is not None and series < 0):
            print("Error BLL (Ejercicio): Series debe ser un número entero positivo.")
            return False
            
        if nombre is not None and tipo is not None:
            check_ej = self.ejercicio_dao.obtener_por_nombre_tipo(nombre, tipo)
            if check_ej and check_ej.id_ejercicio != id_ejercicio:
                print(f"Error BLL (Ejercicio): El nombre y tipo '{nombre}'/'{tipo}' ya están en uso por otro ejercicio.")
                return False

        ejercicio_para_actualizar = Ejercicio(id_ejercicio, nombre, tipo, repeticiones, series, descripcion)

        return self.ejercicio_dao.actualizar_ejercicio(ejercicio_para_actualizar)
    
    def eliminar_ejercicio_existente(self, id_ejercicio):
        """
        Elimina un ejercicio por su ID.
        Retorna True si la eliminación fue exitosa, False en caso contrario.
        """
        if not id_ejercicio:
            print("Error BLL (Ejercicio): El ID del ejercicio es obligatorio para eliminar.")
            return False

        ejercicio_existente = self.ejercicio_dao.obtener_ejercicio_por_id(id_ejercicio)
        if not ejercicio_existente:
            print(f"Error BLL (Ejercicio): Ejercicio con ID {id_ejercicio} no encontrado.")
            return False
        

        return self.ejercicio_dao.eliminar_ejercicio(id_ejercicio)

    def obtener_todos_los_ejercicios(self):
        """
        Obtiene todos los ejercicios registrados.
        Retorna una lista de objetos Ejercicio.
        """
        ejercicios = self.ejercicio_dao.obtener_todos_los_ejercicios()
        for i, ej in enumerate(ejercicios[:5]):
            return ejercicios
        

    def obtener_ejercicio_por_id(self, id_ejercicio):
        """
        Obtiene un ejercicio por su ID.
        Retorna un objeto Ejercicio o None si no se encuentra.
        """
        if not id_ejercicio:
            print("Error BLL (Ejercicio): ID de ejercicio es obligatorio.")
            return None
        return self.ejercicio_dao.obtener_ejercicio_por_id(id_ejercicio)
        
ejercicios_bll = EjercicioBLL()

def crear_nuevo_ejercicio(nombre, tipo, repeticiones=None, series=None, descripcion=None):
    return ejercicios_bll.crear_nuevo_ejercicio(nombre, tipo, repeticiones, series, descripcion)

def modificar_ejercicio_existente(id_ejercicio, nombre=None, tipo=None, repeticiones=None, series=None, descripcion=None):
    return ejercicios_bll.modificar_ejercicio_existente(id_ejercicio, nombre, tipo, repeticiones, series, descripcion)

def eliminar_ejercicio_existente(id_ejercicio):
    return ejercicios_bll.eliminar_ejercicio_existente(id_ejercicio)

def obtener_todos_los_ejercicios():
    return ejercicios_bll.obtener_todos_los_ejercicios()

def obtener_ejercicio_por_id(id_ejercicio):
    return ejercicios_bll.obtener_ejercicio_por_id(id_ejercicio)