from DAL.UsuarioDAO import Usuario, UsuarioDAO

usuario_dao = UsuarioDAO()

def login_usuario(email, contrasena):
    if not email or not contrasena:
        print("Email y contraseña no pueden estar vacíos.")
        return None
    usuario = usuario_dao.obtener_usuario_por_credenciales(email, contrasena)
    if usuario:
        return {"id_usuario": usuario.id_usuario, "nombre": usuario.nombre, "rol": usuario.rol}
    return None

def registrar_usuario(nombre, apellido, email, contrasena, rol):
    if not all([nombre, apellido, email, contrasena, rol]):
        print("Todos los campos son obligatorios.")
        return False
    if "@" not in email or "." not in email:
        print("Formato de email inválido.")
        return False
    
    nuevo_usuario_obj = Usuario(None, nombre, apellido, email, contrasena, rol)
    id_creado = usuario_dao.crear_usuario(nuevo_usuario_obj)
    return id_creado is not None

def obtener_todos_los_clientes():
    return usuario_dao.obtener_todos_los_clientes()

