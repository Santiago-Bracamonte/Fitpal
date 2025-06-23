from DAL.RutinaDAO import RutinaDAO 
from DAL.EjercicioDAO import EjercicioDAO 
from DAL.RutinaEjercicioDAO import RutinaEjercicioDAO 
from DAL.RutinaDAO import Rutina 
from DAL.EjercicioDAO import Ejercicio 

class RutinaBLL:
    """
    BLL para la gestión de Rutinas y sus Ejercicios.
    """
    def __init__(self):
        self.rutina_dao = RutinaDAO()
        self.ejercicio_dao = EjercicioDAO()
        self.rutina_ejercicio_dao = RutinaEjercicioDAO()


    def crear_nueva_rutina(self, nombre, descripcion, duracion):
        """
        Crea una nueva rutina en la base de datos.
        Retorna el objeto Rutina completo con su ID si es exitoso, None si falla.
        """
        if not nombre or not descripcion or not duracion:
            print("Error BLL (Rutina): Nombre, descripción y duración son obligatorios.")
            return None
        
        existing_rutina = self.rutina_dao.obtener_rutina_por_nombre(nombre) 
        if existing_rutina:
            print(f"Error BLL (Rutina): Ya existe una rutina con el nombre '{nombre}'.")
            return None

        nueva_rutina_obj = Rutina(None, nombre, descripcion, duracion)
        id_creado = self.rutina_dao.crear_rutina(nueva_rutina_obj)
        
        if id_creado:
            nueva_rutina_obj.id_rutina = id_creado
            return nueva_rutina_obj
        else:
            print(f"Error BLL (Rutina): No se pudo crear la rutina '{nombre}'.")
            return None

    def actualizar_rutina(self, id_rutina, nombre, descripcion, duracion):
        """
        Actualiza una rutina existente.
        Retorna True si la actualización fue exitosa, False en caso contrario.
        """
        if not all([id_rutina, nombre, descripcion, duracion]):
            print("Error BLL (Rutina): Todos los campos son obligatorios para actualizar.")
            return False

        rutina_existente = self.rutina_dao.obtener_rutina_por_id(id_rutina)
        if not rutina_existente:
            print(f"Error BLL (Rutina): Rutina con ID {id_rutina} no encontrada para actualizar.")
            return False

        check_rutina_nombre = self.rutina_dao.obtener_rutina_por_id(nombre)
        if check_rutina_nombre and check_rutina_nombre.id_rutina != id_rutina:
            print(f"Error BLL (Rutina): El nombre '{nombre}' ya está en uso por otra rutina.")
            return False

        rutina_actualizada_obj = Rutina(id_rutina, nombre, descripcion, duracion)
        success = self.rutina_dao.actualizar_rutina(rutina_actualizada_obj)
        
        if success:
            return True
        else:
            print(f"Error BLL (Rutina): No se pudo actualizar la rutina ID {id_rutina}.")
            return False

    def eliminar_rutina(self, id_rutina):
        """
        Elimina una rutina y todas sus asociaciones con ejercicios.
        Retorna True si la eliminación fue exitosa, False en caso contrario.
        """
        if not id_rutina:
            print("Error BLL (Rutina): ID de rutina es obligatorio para eliminar.")
            return False

        rutina_existente = self.rutina_dao.obtener_rutina_por_id(id_rutina)
        if not rutina_existente:
            print(f"Error BLL (Rutina): Rutina con ID {id_rutina} no encontrada para eliminar.")
            return False
            
       
        self.rutina_ejercicio_dao.eliminar_asociaciones_por_rutina(id_rutina)
        
        success = self.rutina_dao.eliminar_rutina(id_rutina)
        
        if success:
            return True
        else:
            print(f"Error BLL (Rutina): No se pudo eliminar la rutina ID {id_rutina}.")
            return False

    def obtener_todas_las_rutinas(self):
        """
        Obtiene todas las rutinas registradas.
        Retorna una lista de objetos Rutina.
        """
        rutinas = self.rutina_dao.obtener_todas_las_rutinas()
        return rutinas

    def obtener_rutina_por_id(self, id_rutina):
        """
        Obtiene una rutina por su ID.
        Retorna el objeto Rutina si lo encuentra, None en caso contrario.
        """
        if not id_rutina:
            print("Error BLL (Rutina): ID de rutina es obligatorio.")
            return None
        rutina = self.rutina_dao.obtener_rutina_por_id(id_rutina)
        if rutina:
            return rutina


    def obtener_detalles_rutina_con_ejercicios(self, id_rutina):
        """
        Obtiene los detalles de una rutina y la lista de todos sus ejercicios asociados.
        Retorna un diccionario con 'rutina' (objeto Rutina) y 'ejercicios' (lista de objetos Ejercicio).
        Retorna None si la rutina no existe.
        """
        if not id_rutina:
            print("Error BLL (Detalles Rutina): ID de rutina es obligatorio.")
            return None

        rutina = self.rutina_dao.obtener_rutina_por_id(id_rutina)
        if rutina:
            ejercicios = self.rutina_ejercicio_dao.obtener_ejercicios_de_rutina(id_rutina)
            return {"rutina": rutina, "ejercicios": ejercicios}
        else:
            print(f"Error BLL (Detalles Rutina): Rutina con ID {id_rutina} no encontrada.")
            return None

    def asociar_ejercicio_a_rutina_bll(self, id_rutina, id_ejercicio):
        """
        Lógica de negocio para asociar un ejercicio a una rutina.
        Verifica la existencia de ambos.
        Retorna True si la asociación fue exitosa, False en caso contrario.
        """
        if not id_rutina or not id_ejercicio:
            print("Error BLL (Asociación): IDs de rutina y ejercicio son obligatorios.")
            return False

        rutina_existente = self.rutina_dao.obtener_rutina_por_id(id_rutina)
        ejercicio_existente = self.ejercicio_dao.obtener_ejercicio_por_id(id_ejercicio)

        if not rutina_existente:
            print(f"Error BLL (Asociación): Rutina con ID {id_rutina} no encontrada.")
            return False
        if not ejercicio_existente:
            print(f"Error BLL (Asociación): Ejercicio con ID {id_ejercicio} no encontrado.")
            return False

        id_asociacion = self.rutina_ejercicio_dao.asociar_ejercicio_a_rutina(id_rutina, id_ejercicio)
        
        if id_asociacion:
            return True
        else:
            return False

    def desasociar_ejercicio_de_rutina_bll(self, id_rutina, id_ejercicio):
        """
        Lógica de negocio para desasociar un ejercicio de una rutina.
        Retorna True si la desasociación fue exitosa, False en caso contrario.
        """
        if not id_rutina or not id_ejercicio:
            print("Error BLL (Desasociación): IDs de rutina y ejercicio son obligatorios.")
            return False

       

        success = self.rutina_ejercicio_dao.desasociar_ejercicio_de_rutina(id_rutina, id_ejercicio)
        
        if success:
            return True
        else:
            return False


rutina_bll = RutinaBLL()

def crear_nueva_rutina(nombre, descripcion, duracion):
    return rutina_bll.crear_nueva_rutina(nombre, descripcion, duracion)

def actualizar_rutina(id_rutina, nombre, descripcion, duracion):
    return rutina_bll.actualizar_rutina(id_rutina, nombre, descripcion, duracion)

def eliminar_rutina(id_rutina):
    return rutina_bll.eliminar_rutina(id_rutina)

def obtener_todas_las_rutinas():
    return rutina_bll.obtener_todas_las_rutinas()

def obtener_rutina_por_id(id_rutina):
    return rutina_bll.obtener_rutina_por_id(id_rutina)

def obtener_detalles_rutina_con_ejercicios(id_rutina):
    return rutina_bll.obtener_detalles_rutina_con_ejercicios(id_rutina)

def asociar_ejercicio_a_rutina(id_rutina, id_ejercicio):
    return rutina_bll.asociar_ejercicio_a_rutina_bll(id_rutina, id_ejercicio) 

def desasociar_ejercicio_de_rutina(id_rutina, id_ejercicio):
    return rutina_bll.desasociar_ejercicio_de_rutina_bll(id_rutina, id_ejercicio) 