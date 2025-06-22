from datetime import date
from DAL.AsignacionRutinaDAO import AsignacionRutinaDAO
from DAL.RutinaDAO import RutinaDAO
from DAL.UsuarioDAO import UsuarioDAO 

class AsignacionRutinaBLL:
    def __init__(self):
        self.asignacion_dao = AsignacionRutinaDAO()
        self.rutina_dao = RutinaDAO()
        self.usuario_dao = UsuarioDAO()

    def asignar_rutina_a_cliente(self, id_entrenador, id_cliente, id_rutina):
        """
        Asigna una rutina a un cliente.
        Verifica si la rutina y el cliente existen.
        Si ya hay una asignación activa para el misma rutina y cliente en el día, no se reasigna.
        """
        if not all([id_entrenador, id_cliente, id_rutina]):
            print("Error BLL (Asignación): Todos los IDs son obligatorios.")
            return False

        rutina = self.rutina_dao.obtener_rutina_por_id(id_rutina)
        cliente = self.usuario_dao.obtener_usuario_por_id(id_cliente)

        if not rutina:
            print(f"Error BLL (Asignación): Rutina con ID {id_rutina} no encontrada.")
            return False
        if not cliente or cliente.rol != 'cliente':
            print(f"Error BLL (Asignación): Cliente con ID {id_cliente} no encontrado o no es un cliente válido.")
            return False

        entrenador = self.usuario_dao.obtener_usuario_por_id(id_entrenador)
        if not entrenador or entrenador.rol != 'entrenador':
            print(f"Error BLL (Asignación): Entrenador con ID {id_entrenador} no encontrado o no es un entrenador válido.")
            return False
        fecha_actual = date.today().strftime('%Y-%m-%d') 
        existing_assignment = self.asignacion_dao.obtener_rutinas_asignadas_a_usuario(id_cliente, id_rutina, fecha_actual)
        if existing_assignment:
            print(f"BLL (Asignación): La rutina '{rutina.nombre}' ya fue asignada al cliente '{cliente.nombre}' para hoy.")
            return False 

        return self.asignacion_dao.asignar_rutina(id_cliente, id_rutina, id_entrenador, fecha_actual) 


    def ver_rutinas_asignadas_a_usuario(self, id_cliente):
        """
        Obtiene las rutinas asignadas a un cliente específico, ordenadas por fecha descendente.
        Retorna una lista de diccionarios con el objeto AsignacionRutina y el objeto Rutina.
        """
        if not id_cliente:
            print("Error BLL (Ver Asignaciones): ID de cliente es obligatorio.")
            return []

        cliente = self.usuario_dao.obtener_usuario_por_id(id_cliente)
        if not cliente or cliente.rol != 'cliente':
            print(f"Error BLL (Ver Asignaciones): Cliente con ID {id_cliente} no encontrado o no es un cliente válido.")
            return []
        
        assigned_data = self.asignacion_dao.obtener_asignaciones_y_rutinas_por_cliente(id_cliente)
        return assigned_data


    def ver_clientes_con_rutina_asignada(self, id_entrenador):
        """
        Obtiene una lista de todos los clientes a los que un entrenador ha asignado una rutina,
        junto con el nombre de la rutina y la fecha de asignación.
        Esto es útil para la vista del entrenador.
        """
        if not id_entrenador:
            print("Error BLL (Ver Clientes con Rutinas): ID de entrenador es obligatorio.")
            return []

        entrenador = self.usuario_dao.obtener_usuario_por_id(id_entrenador)
        if not entrenador or entrenador.rol != 'entrenador':
            print(f"Error BLL (Ver Clientes con Rutinas): Entrenador con ID {id_entrenador} no encontrado o no es un entrenador válido.")
            return []
        
        raw_assignments = self.asignacion_dao.obtener_asignaciones_por_entrenador(id_entrenador)
        
        
        result = []
        for assign in raw_assignments:
           
            try:
                id_cliente = assign['fk_usuario']
                id_rutina = assign['fk_rutina']
                fecha_asignado_str = assign['fecha_asignado'] 
                
                id_asignacion = assign['id_asignacion_rutina']

                cliente = self.usuario_dao.obtener_usuario_por_id(id_cliente)
                rutina = self.rutina_dao.obtener_rutina_por_id(id_rutina) 
                if cliente and rutina:
                    result.append({
                        'id_asignacion': id_asignacion,
                        'id_cliente': cliente.id_usuario,
                        'nombre_cliente': cliente.nombre,
                        'apellido_cliente': cliente.apellido,
                        'id_rutina': rutina.id_rutina,
                        'nombre_rutina': rutina.nombre,
                        'fecha_asignado': fecha_asignado_str
                    })
            except Exception as e:
                print(f"ERROR BLL: Error inesperado procesando asignación {assign}: {e}")
                continue
                
        return result
    
    def desasignar_rutina_a_cliente(self, id_asignacion):
        """
        Desasigna una rutina eliminando la asignación por su ID.
        """
        if not id_asignacion:
            print("Error BLL (Desasignar): ID de asignación es obligatorio.")
            return False
        
        success = self.asignacion_dao.eliminar_asignacion_rutina(id_asignacion)
        return success

asignaciones_bll = AsignacionRutinaBLL()


def asignar_rutina_a_cliente(id_entrenador, id_cliente, id_rutina):
    return asignaciones_bll.asignar_rutina_a_cliente(id_entrenador, id_cliente, id_rutina)

def ver_rutinas_asignadas_a_usuario(id_cliente):
    return asignaciones_bll.ver_rutinas_asignadas_a_usuario(id_cliente)

def ver_rutinas_de_clientes(id_entrenador): 
    return asignaciones_bll.ver_clientes_con_rutina_asignada(id_entrenador)

def desasignar_rutina_a_cliente(id_asignacion):
    return asignaciones_bll.desasignar_rutina_a_cliente(id_asignacion)