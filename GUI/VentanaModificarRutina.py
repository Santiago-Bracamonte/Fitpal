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

class VentanaModificarRutina(tk.Toplevel):
    def __init__(self, parent, on_success_callback):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.on_success_callback = on_success_callback
        self.title("Modificar Rutina")
        self.geometry("600x600")
        self.transient(self.parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

        tk.Label(self, text="Seleccionar Rutina a Modificar:").pack(pady=5)
        self.variable_rutinas = tk.StringVar(self)
        self.todas_las_rutinas = obtener_listado_rutinas()  
        if not self.todas_las_rutinas:
            tk.Label(self, text="No hay rutinas para modificar.").pack()
            tk.Button(self, text="Cerrar", command=self._on_closing).pack(pady=10)
            self.wait_window(self)
            return

        self.nombres_rutinas = [r.nombre for r in self.todas_las_rutinas]
        self.mapa_rutinas = {r.nombre: r.id_rutina for r in self.todas_las_rutinas}

        self.variable_rutinas.set(self.nombres_rutinas[0])
        self.menu_rutinas = tk.OptionMenu(self, self.variable_rutinas, *self.nombres_rutinas, command=self._cargar_detalles_rutina)
        self.menu_rutinas.pack(pady=2)

        tk.Label(self, text="Nombre:").pack(pady=5)
        self.entrada_nombre = tk.Entry(self, width=50)
        self.entrada_nombre.pack(pady=2)

        tk.Label(self, text="Descripción:").pack(pady=5)
        self.texto_descripcion = tk.Text(self, height=5, width=50)
        self.texto_descripcion.pack(pady=2)

        tk.Label(self, text="Duración:").pack(pady=5)
        self.entrada_duracion = tk.Entry(self, width=50)
        self.entrada_duracion.pack(pady=2)

        tk.Label(self, text="Ejercicios (Seleccionar/Deseleccionar):").pack(pady=5)
        self.lista_ejercicios = tk.Listbox(self, selectmode=tk.MULTIPLE, height=10, width=60)
        self.lista_ejercicios.pack(pady=5)

        self.ejercicios_disponibles = obtener_todos_los_ejercicios()  
        self.id_ejercicio_a_indice = {ej.id_ejercicio: i for i, ej in enumerate(self.ejercicios_disponibles)}
        self.indice_a_id_ejercicio = {i: ej.id_ejercicio for i, ej in enumerate(self.ejercicios_disponibles)}

        if self.ejercicios_disponibles:
            for i, ej in enumerate(self.ejercicios_disponibles):
                self.lista_ejercicios.insert(tk.END, f"{ej.nombre} ({ej.tipo})")
        else:
            self.lista_ejercicios.insert(tk.END, "No hay ejercicios disponibles. Agréguelos en la pestaña 'Gestión de Ejercicios'.")


        tk.Button(self, text="Guardar Cambios", command=self._guardar_cambios).pack(pady=10)

        self._cargar_detalles_rutina(self.variable_rutinas.get())
        
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
        self.wait_window(self)

    def _on_closing(self):
        self.grab_release()
        self.destroy()

    def _cargar_detalles_rutina(self, selected_name):
        selected_id = self.mapa_rutinas[selected_name]
        routine_data = obtener_detalles_rutina_con_ejercicios(selected_id) 

        if routine_data:
            rutina = routine_data['rutina']
            ejercicios_rutina = routine_data['ejercicios']

            self.entrada_nombre.delete(0, tk.END)
            self.entrada_nombre.insert(0, rutina.nombre)
            self.texto_descripcion.delete("1.0", tk.END)
            self.texto_descripcion.insert("1.0", rutina.descripcion)
            self.entrada_duracion.delete(0, tk.END)
            self.entrada_duracion.insert(0, rutina.duracion)

            self.lista_ejercicios.selection_clear(0, tk.END)
            for ej_rutina in ejercicios_rutina:
                if ej_rutina.id_ejercicio in self.id_ejercicio_a_indice:
                    index = self.id_ejercicio_a_indice[ej_rutina.id_ejercicio]
                    self.lista_ejercicios.select_set(index)
        else:
            messagebox.showerror("Error", "No se pudieron cargar los detalles de la rutina.")

    def _guardar_cambios(self):
        selected_name = self.variable_rutinas.get()
        routine_id = self.mapa_rutinas[selected_name]

        new_name = self.entrada_nombre.get().strip()
        new_desc = self.texto_descripcion.get("1.0", tk.END).strip()
        new_duration = self.entrada_duracion.get().strip()

        selected_indices = self.lista_ejercicios.curselection()
        new_exercise_ids = [self.indice_a_id_ejercicio[i] for i in selected_indices]

        if not new_name or not new_duration:
            messagebox.showerror("Error", "El nombre y la duración de la rutina no pueden estar vacíos.")
            return
        
        if not new_exercise_ids:
            response = messagebox.askyesno("Advertencia", "¿Realmente desea guardar la rutina sin ejercicios? Esto eliminará cualquier ejercicio previamente asociado.", icon="warning")
            if not response:
                return

        success = modificar_rutina_y_ejercicios(routine_id, new_name, new_desc, new_duration, new_exercise_ids)

        if success:
            messagebox.showinfo("Éxito", "Rutina modificada con éxito.")
            self.on_success_callback()  
            self._on_closing()
        else:
            messagebox.showerror("Error", "No se pudo modificar la rutina. Verifique los datos o si el nombre/duración ya existen en otra rutina.")
