import tkinter as tk
from tkinter import messagebox
from BLL.UsuarioBLL import obtener_todos_los_clientes
from BLL.RutinasBLL import (
    crear_rutina_con_ejercicios, modificar_rutina_y_ejercicios,
    eliminar_rutina_completa, obtener_listado_rutinas, obtener_detalles_rutina_con_ejercicios
)
from BLL.AsignacionRutinaBLL import asignar_rutina_a_cliente, desasignar_rutina_a_cliente, ver_rutinas_de_clientes
from BLL.EjercicioBLL import (
    crear_nuevo_ejercicio, modificar_ejercicio_existente,
    eliminar_ejercicio_existente, obtener_todos_los_ejercicios,
    obtener_ejercicio_por_id
)



class VentanaEliminarRutina(tk.Toplevel):
    def __init__(self, parent, on_success_callback):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.on_success_callback = on_success_callback
        self.title("Eliminar Rutina")
        self.geometry("300x200")
        self.transient(self.parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

        tk.Label(self, text="Seleccionar Rutina a Eliminar:").pack(pady=5)
        self.variable_rutinas = tk.StringVar(self)
        self.todas_las_rutinas = obtener_listado_rutinas()  
        if not self.todas_las_rutinas:
            tk.Label(self, text="No hay rutinas para eliminar.").pack()
            tk.Button(self, text="Cerrar", command=self._on_closing).pack(pady=10)
            self.wait_window(self)
            return

        self.nombres_rutinas = [r.nombre for r in self.todas_las_rutinas]
        self.mapa_rutinas = {r.nombre: r.id_rutina for r in self.todas_las_rutinas}

        self.variable_rutinas.set(self.nombres_rutinas[0])
        self.menu_rutinas = tk.OptionMenu(self, self.variable_rutinas, *self.nombres_rutinas)
        self.menu_rutinas.pack(pady=2)

        tk.Button(self, text="Eliminar Rutina", command=self._eliminar_rutina).pack(pady=10)
        
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
        self.wait_window(self)

    def _on_closing(self):
        self.grab_release()
        self.destroy()

    def _eliminar_rutina(self):
        selected_name = self.variable_rutinas.get()
        routine_id = self.mapa_rutinas[selected_name]

        if messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que quieres eliminar la rutina '{selected_name}'? Esto también eliminará sus asociaciones con ejercicios y clientes."):
            success = eliminar_rutina_completa(routine_id) 
            if success:
                messagebox.showinfo("Éxito", "Rutina eliminada correctamente.")
                self.on_success_callback()  
                self._on_closing()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la rutina. Asegúrate de que no esté asignada a clientes activos o que la base de datos permita la eliminación en cascada.")