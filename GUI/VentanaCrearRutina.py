import tkinter as tk
from tkinter import messagebox
from BLL.RutinasBLL import (
    crear_rutina_con_ejercicios
)
from BLL.EjercicioBLL import ( obtener_todos_los_ejercicios)

class VentanaCrearRutina(tk.Toplevel):
    def __init__(self, parent, on_success_callback):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent 
        self.on_success_callback = on_success_callback  
        self.title("Crear Nueva Rutina")
        self.geometry("600x500")
        self.transient(self.parent)
        self.grab_set() 
        self.protocol("WM_DELETE_WINDOW", self._on_closing) 

        tk.Label(self, text="Nombre de la Rutina:").pack(pady=5)
        self.entrada_nombre = tk.Entry(self, width=50)
        self.entrada_nombre.pack(pady=2)

        tk.Label(self, text="Descripción:").pack(pady=5)
        self.texto_descripcion = tk.Text(self, height=5, width=50)
        self.texto_descripcion.pack(pady=2)

        tk.Label(self, text="Duración (ej. '30 minutos'):").pack(pady=5)
        self.entrada_duracion = tk.Entry(self, width=50)
        self.entrada_duracion.pack(pady=2)

        tk.Label(self, text="Seleccionar Ejercicios:").pack(pady=5)
        self.lista_ejercicios = tk.Listbox(self, selectmode=tk.MULTIPLE, height=10, width=60)
        self.lista_ejercicios.pack(pady=5)

        self.ejercicios_disponibles = obtener_todos_los_ejercicios()
        self.mapa_ejercicios = {}
        if self.ejercicios_disponibles:
            for i, ej in enumerate(self.ejercicios_disponibles):
                item_text = f"{ej.nombre} ({ej.tipo})"
                self.lista_ejercicios.insert(tk.END, item_text)
                self.mapa_ejercicios[i] = ej.id_ejercicio
        else:
            self.lista_ejercicios.insert(tk.END, "No hay ejercicios disponibles. Agréguelos en la pestaña 'Gestión de Ejercicios'.")


        tk.Button(self, text="Crear Rutina", command=self._crear_rutina).pack(pady=10) 

        # Centrar la ventana
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
        self.wait_window(self) 

    def _on_closing(self):
        self.grab_release()
        self.destroy()

    def _crear_rutina(self):
        nombre = self.entrada_nombre.get().strip()
        descripcion = self.texto_descripcion.get("1.0", tk.END).strip()
        duracion = self.entrada_duracion.get().strip()

        selected_indices = self.lista_ejercicios.curselection()
        selected_exercise_ids = [self.mapa_ejercicios[i] for i in selected_indices]

        if not nombre or not duracion:
            messagebox.showerror("Error", "Por favor, complete el nombre y la duración de la rutina.")
            return
        
        if not selected_exercise_ids:
            messagebox.showwarning("Advertencia", "No ha seleccionado ningún ejercicio para esta rutina. ¿Desea continuar?", icon="warning", type="yesno")
            if not messagebox.askyesno("Confirmar", "¿Realmente desea crear una rutina sin ejercicios?"):
                return

        new_routine = crear_rutina_con_ejercicios(nombre, descripcion, duracion, selected_exercise_ids)

        if new_routine:
            messagebox.showinfo("Éxito", f"Rutina '{new_routine.nombre}' creada con éxito.")
            self.on_success_callback()  
            self._on_closing() 
        else:
            messagebox.showerror("Error", "No se pudo crear la rutina. Verifique que no haya una rutina con el mismo nombre y duración.")

