
import tkinter as tk
from tkinter import messagebox

from BLL.UsuarioBLL import login_usuario, registrar_usuario
from DAL.fitpalDB import crear_tablas 

from GUI.DashboardCliente import DashboardCliente 
from GUI.DashboardEntrenador import DashboardEntrenador 



class FitPalApp:
    def __init__(self, master):
        self.master = master
        master.title("FitPal App - Iniciar Sesión / Registrarse")
        master.geometry("500x400")

      
        crear_tablas() 

        self.current_user_info = None

        self.frames = {}
        self._setup_initial_frames()
        self.show_frame("Login")

    def _setup_initial_frames(self):
        self.login_frame = LoginFrame(self.master, self)
        self.frames["Login"] = self.login_frame
        self.login_frame.grid(row=0, column=0, sticky="nsew")

        self.register_frame = RegisterFrame(self.master, self)
        self.frames["Register"] = self.register_frame
        self.register_frame.grid(row=0, column=0, sticky="nsew")

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()

    def handle_login_success(self, user_info):
        self.current_user_info = user_info
        messagebox.showinfo("Login Exitoso", f"Bienvenido, {user_info['nombre']} ({user_info['rol']})!")
        
        self.master.destroy() 
        
        if self.current_user_info['rol'] == "cliente":
            self._start_client_dashboard()
        elif self.current_user_info['rol'] == "entrenador":
            self._start_trainer_dashboard()

    def _start_client_dashboard(self):
        dashboard_root = tk.Tk()
        dashboard_root.geometry("1000x700")
        dashboard_root.title("FitPal - Dashboard Cliente")
        app = DashboardCliente(dashboard_root, self.current_user_info, self._reopen_main_window)
        dashboard_root.mainloop()

    def _start_trainer_dashboard(self):
        dashboard_root = tk.Tk()
        dashboard_root.geometry("1200x800")
        dashboard_root.title("FitPal - Dashboard Entrenador")
        app = DashboardEntrenador(dashboard_root, self.current_user_info, self._reopen_main_window)
        dashboard_root.mainloop()

    def _reopen_main_window(self):
        root = tk.Tk()
        app = FitPalApp(root)
        root.mainloop()


class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="INICIAR SESIÓN", font=("Arial", 24)).pack(pady=20)

        tk.Label(self, text="Email:").pack()
        self.email_entry = tk.Entry(self, width=40)
        self.email_entry.pack(pady=5)

        tk.Label(self, text="Contraseña:").pack()
        self.password_entry = tk.Entry(self, width=40, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self, text="Login", command=self._login_button_click).pack(pady=10)
        tk.Button(self, text="Registrarse", command=lambda: self.controller.show_frame("Register")).pack(pady=5)

    def _login_button_click(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        user_info = login_usuario(email, password)
        
        if user_info:
            self.controller.handle_login_success(user_info)
            self.email_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error de Login", "Email o contraseña incorrectos.")

class RegisterFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="REGISTRAR NUEVO USUARIO", font=("Arial", 24)).pack(pady=20)

        tk.Label(self, text="Nombre:").pack()
        self.nombre_entry = tk.Entry(self, width=40)
        self.nombre_entry.pack(pady=2)

        tk.Label(self, text="Apellido:").pack()
        self.apellido_entry = tk.Entry(self, width=40)
        self.apellido_entry.pack(pady=2)

        tk.Label(self, text="Email:").pack()
        self.email_entry = tk.Entry(self, width=40)
        self.email_entry.pack(pady=2)

        tk.Label(self, text="Contraseña:").pack()
        self.password_entry = tk.Entry(self, width=40, show="*")
        self.password_entry.pack(pady=2)

        tk.Label(self, text="Rol:").pack()
        self.rol_var = tk.StringVar(self)
        self.rol_var.set("cliente")
        self.rol_menu = tk.OptionMenu(self, self.rol_var, "cliente", "entrenador")
        self.rol_menu.pack(pady=2)

        tk.Button(self, text="Registrar", command=self._register_button_click).pack(pady=10)
        tk.Button(self, text="Volver al Login", command=lambda: self.controller.show_frame("Login")).pack(pady=5)

    def _register_button_click(self):
        nombre = self.nombre_entry.get()
        apellido = self.apellido_entry.get()
        email = self.email_entry.get()
        contrasena = self.password_entry.get()
        rol = self.rol_var.get()

        if not all([nombre, apellido, email, contrasena, rol]):
            messagebox.showerror("Error de Registro", "Todos los campos son obligatorios.")
            return

        success = registrar_usuario(nombre, apellido, email, contrasena, rol) 
        
        if success:
            messagebox.showinfo("Registro Exitoso", "Usuario registrado correctamente. ¡Ahora puedes iniciar sesión!")
            self.email_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.nombre_entry.delete(0, tk.END)
            self.apellido_entry.delete(0, tk.END)
            self.controller.show_frame("Login")
        else:
            messagebox.showerror("Error de Registro", "El email ya está registrado.")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = FitPalApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Ha ocurrido un error inesperado al iniciar la aplicación: {e}")
        # Opcional: mostrar un messagebox de error
        messagebox.showerror("Error de Aplicación", f"La aplicación ha encontrado un error y se cerrará: {e}")
