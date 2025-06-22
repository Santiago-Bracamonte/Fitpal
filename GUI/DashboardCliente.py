import tkinter as tk
from tkinter import messagebox

from BLL.RutinasBLL import obtener_detalles_rutina_con_ejercicios
from BLL.AsignacionRutinaBLL import ver_rutinas_asignadas_a_usuario 

class DashboardCliente:
    def __init__(self, master, user_info, on_logout_callback):
        self.master = master
        self.user_info = user_info 
        self.on_logout_callback = on_logout_callback 
        
        self.exercises_data = {} 

        self.master.title(f"FitPal - Dashboard de Cliente: {self.user_info['nombre']}")
        self.master.geometry("1000x700")

        self.create_widgets()
        
        self.load_data() 

    def create_widgets(self):
        top_frame = tk.Frame(self.master, bd=2, relief="groove")
        top_frame.pack(side="top", fill="x", pady=10, padx=10)
        
        tk.Label(top_frame, text=f"Bienvenido, {self.user_info['nombre']}", font=("Arial", 20, "bold")).pack(side="left", padx=10)
        tk.Button(top_frame, text="Cerrar Sesión", command=self._logout).pack(side="right", padx=10)

        main_frame = tk.Frame(self.master, bd=2, relief="groove")
        main_frame.pack(pady=10, padx=10, fill="both", expand=True)

        tk.Label(main_frame, text="Mi Rutina Asignada:", font=("Arial", 16, "bold")).pack(pady=5)
        self.routine_name_label = tk.Label(main_frame, text="Nombre de la rutina:")
        self.routine_name_label.pack()
        self.routine_desc_label = tk.Label(main_frame, text="Descripción:")
        self.routine_desc_label.pack()
        self.routine_duration_label = tk.Label(main_frame, text="Duración:")
        self.routine_duration_label.pack()

        tk.Label(main_frame, text="Ejercicios:", font=("Arial", 14, "underline")).pack(pady=10)
        
        self.exercises_listbox = tk.Listbox(main_frame, height=10, width=80)
        self.exercises_listbox.pack(pady=5, padx=10, fill="both", expand=True)
        self.exercises_listbox.bind("<<ListboxSelect>>", self.mostrar_detalles_ejercicios)
        
        tk.Label(main_frame, text="Detalles del Ejercicio Seleccionado:", font=("Arial", 12, "bold")).pack(pady=5)
        self.exercise_details_label = tk.Label(main_frame, text="", justify=tk.LEFT, wraplength=400, anchor="nw")
        self.exercise_details_label.pack(pady=5, padx=10, fill="x")

    def load_data(self):
       
        assigned_routines_data = ver_rutinas_asignadas_a_usuario(self.user_info['id_usuario'])
        
        self.routine_name_label.config(text="Cargando rutina...")
        self.routine_desc_label.config(text="")
        self.routine_duration_label.config(text="")
        self.exercises_listbox.delete(0, tk.END)
        self.exercise_details_label.config(text="")
        
        if assigned_routines_data:
            latest_routine_id = assigned_routines_data[0]['id_rutina']
            routine_with_exercises = obtener_detalles_rutina_con_ejercicios(latest_routine_id)

            if routine_with_exercises:
                rutina = routine_with_exercises['rutina']
                ejercicios = routine_with_exercises['ejercicios']

                self.routine_name_label.config(text=f"Mi Rutina Asignada: {rutina.nombre}")
                self.routine_desc_label.config(text=f"Descripción: {rutina.descripcion}")
                self.routine_duration_label.config(text=f"Duración: {rutina.duracion}")
                
                self.exercises_data = {} 
                if ejercicios:
                    for i, ejercicio in enumerate(ejercicios):
                        self.exercises_listbox.insert(tk.END, f"{i+1}. {ejercicio.nombre} ({ejercicio.tipo})")
                        self.exercises_data[i] = ejercicio
                else:
                    self.exercises_listbox.insert(tk.END, "Esta rutina no tiene ejercicios asignados.")
            else:
                 messagebox.showerror("Error", "No se pudieron cargar los detalles de la rutina asignada.")
        else:
            self.routine_name_label.config(text="No tienes ninguna rutina asignada aún.")
            self.exercises_listbox.insert(tk.END, "Contacta a tu entrenador para que te asigne una rutina.")

    def mostrar_detalles_ejercicios(self, event):
        selected_index = self.exercises_listbox.curselection()
        
    
        if not selected_index:
            self.exercise_details_label.config(text="Ningún ejercicio seleccionado.")
            return 

        index = selected_index[0]
        ejercicio = self.exercises_data.get(index)
        
    

        if ejercicio:
            details = (f"Nombre: {ejercicio.nombre}\n"
                       f"Tipo: {ejercicio.tipo}\n"
                       f"Repeticiones: {ejercicio.repeticiones if ejercicio.repeticiones is not None else 'N/A'}\n"
                       f"Series: {ejercicio.series if ejercicio.series is not None else 'N/A'}\n"
                       f"Descripción: {ejercicio.descripcion if ejercicio.descripcion else 'Sin descripción detallada.'}")
            self.exercise_details_label.config(text=details)
        else:
            self.exercise_details_label.config(text="No se pudo cargar los detalles del ejercicio seleccionado.")

    def _logout(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Estás seguro de que quieres cerrar sesión?"):
            self.master.destroy()
            self.on_logout_callback() 