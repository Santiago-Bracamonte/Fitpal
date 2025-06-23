from DAL.RutinaDAO import Rutina, RutinaDAO
from DAL.EjercicioDAO import RutinaEjercicioDAO
from DAL.RutinaEjercicioDAO import RutinaEjercicioDAO

rutina_dao = RutinaDAO()
rutina_ejercicio_dao = RutinaEjercicioDAO()

def crear_rutina_con_ejercicios(nombre, descripcion, duracion, ejercicios_ids):
    if not nombre or not duracion:
        print("Nombre y duración son obligatorios para la rutina.")
        return None
    
    nueva_rutina_obj = Rutina(None, nombre, descripcion, duracion)
    id_rutina = rutina_dao.crear_rutina(nueva_rutina_obj)
    
    if id_rutina:
        for ejercicio_id in ejercicios_ids:
            rutina_ejercicio_dao.asociar_ejercicio_a_rutina(id_rutina, ejercicio_id)
        return rutina_dao.obtener_rutina_por_id(id_rutina) 
    return None

def modificar_rutina_y_ejercicios(rutina_id, new_name, new_desc, new_duration, new_exercise_ids):

    rutina_existente = rutina_dao.obtener_rutina_por_id(rutina_id)
    if not rutina_existente:
        return False 

    rutina_actualizada = Rutina(rutina_id, new_name, new_desc, new_duration)
    if not rutina_dao.actualizar_rutina(rutina_actualizada):
        return False

    ejercicios_actuales = rutina_ejercicio_dao.obtener_ejercicios_de_rutina(rutina_id)

    # Paso 4: Eliminar asociaciones existentes de la rutina
    if not rutina_ejercicio_dao.eliminar_asociaciones_por_rutina(rutina_id):

        return False 

    for ejercicio_id in new_exercise_ids:
        
        if not rutina_ejercicio_dao.asociar_ejercicio_a_rutina(rutina_id, ejercicio_id):
            return False 

    return True 

def eliminar_rutina_completa(id_rutina):
    rutina_ejercicio_dao.eliminar_asociaciones_por_rutina(id_rutina) 
 
    return rutina_dao.eliminar_rutina(id_rutina)

def obtener_detalles_rutina_con_ejercicios(id_rutina):
    rutina = rutina_dao.obtener_rutina_por_id(id_rutina)
    if rutina:
        ejercicios = rutina_ejercicio_dao.obtener_ejercicios_de_rutina(id_rutina)
        for i, ej in enumerate(ejercicios[:5]): 
            return {"rutina": rutina, "ejercicios": ejercicios}
    return None

def obtener_listado_rutinas():
    return rutina_dao.obtener_todas_las_rutinas()

