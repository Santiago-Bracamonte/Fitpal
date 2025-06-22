import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from BLL.UsuarioBLL import obtener_todos_los_clientes
from BLL.RutinasBLL import (
     obtener_listado_rutinas, obtener_detalles_rutina_con_ejercicios
)
from BLL.AsignacionRutinaBLL import asignar_rutina_a_cliente, desasignar_rutina_a_cliente, ver_rutinas_de_clientes
from BLL.EjercicioBLL import (
    crear_nuevo_ejercicio, modificar_ejercicio_existente,
    eliminar_ejercicio_existente, obtener_todos_los_ejercicios 
)

from GUI.VentanaCrearRutina import VentanaCrearRutina
from GUI.VentanaEliminarRutina import VentanaEliminarRutina
from GUI.VentanaModificarRutina import VentanaModificarRutina

class DashboardEntrenador:
    def __init__(self, master, user_info, on_logout_callback):
        self.master = master
        self.user_info = user_info 
        self.on_logout_callback = on_logout_callback  

        master.title(f"FitPal - Panel de Entrenador: {self.user_info['nombre']}")
        master.geometry("1200x800")

        self.crear_widgets()
       
    def crear_widgets(self):
        top_frame = tk.Frame(self.master, bd=2, relief="groove")
        top_frame.pack(side="top", fill="x", pady=10, padx=10)

        tk.Label(top_frame, text=f"Panel de Entrenador: {self.user_info['nombre']}", font=("Arial", 20, "bold")).pack(side="left", padx=10)
        tk.Button(top_frame, text="Cerrar Sesión", command=self._cerrar_sesion).pack(side="right", padx=10)

        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(pady=10, padx=10, expand=True, fill="both")

        self.pestana_rutinas = tk.Frame(self.notebook)
        self.notebook.add(self.pestana_rutinas, text="Gestión de Rutinas")
        self._configurar_pestana_rutinas()

        self.pestana_asignacion = tk.Frame(self.notebook)
        self.notebook.add(self.pestana_asignacion, text="Asignar Rutinas")
        self._configurar_pestana_asignacion()

        self.pestana_ejercicios = tk.Frame(self.notebook)
        self.notebook.add(self.pestana_ejercicios, text="Gestión de Ejercicios")
        self._configurar_pestana_ejercicios()

        self.pestana_clientes_rutinas = tk.Frame(self.notebook)
        self.notebook.add(self.pestana_clientes_rutinas, text="Ver Clientes y Rutinas")
        self._configurar_pestana_clientes_rutinas()

        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)

    def _on_tab_change(self, event):
        selected_tab = self.notebook.tab(self.notebook.select(), "text")
        if selected_tab == "Gestión de Rutinas":
            self.cargar_lista_rutinas()
        elif selected_tab == "Asignar Rutinas":
            
            self._recargar_opciones_asignacion()
        elif selected_tab == "Gestión de Ejercicios":
            self.cargar_lista_ejercicios()
        elif selected_tab == "Ver Clientes y Rutinas":
            self.cargar_datos_rutina_clientes()

    

    def _cerrar_sesion(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Estás seguro de que quieres cerrar sesión?"):
            self.master.destroy()  
            self.on_logout_callback()  

    def _configurar_pestana_rutinas(self):
        tk.Label(self.pestana_rutinas, text="GESTIÓN DE RUTINAS", font=("Arial", 18)).pack(pady=10)

        button_frame = tk.Frame(self.pestana_rutinas)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Crear Nueva Rutina", command=self._abrir_ventana_crear_rutina).pack(side="left", padx=5)
        tk.Button(button_frame, text="Modificar Rutina", command=self._abrir_ventana_modificar_rutina).pack(side="left", padx=5)
        tk.Button(button_frame, text="Eliminar Rutina", command=self._abrir_ventana_eliminar_rutina).pack(side="left", padx=5)

        tk.Label(self.pestana_rutinas, text="Lista de Rutinas Existentes:", font=("Arial", 14)).pack(pady=10)
        self.lista_rutinas = tk.Listbox(self.pestana_rutinas, height=15, width=80)
        self.lista_rutinas.pack(pady=5, padx=10, fill="both", expand=True)
        self.lista_rutinas.bind("<<ListboxSelect>>", self._mostrar_detalles_rutina)

        self.etiqueta_detalles_rutina = tk.Label(self.pestana_rutinas, text="", justify=tk.LEFT, wraplength=700)
        self.etiqueta_detalles_rutina.pack(pady=10)

        self.cargar_lista_rutinas()  
    def cargar_lista_rutinas(self):
        self.lista_rutinas.delete(0, tk.END)
        self.todas_las_rutinas = obtener_listado_rutinas()  
        self.mapa_rutinas = {}  
        for i, r in enumerate(self.todas_las_rutinas):
            self.lista_rutinas.insert(tk.END, f"{r.nombre} ({r.duracion})")
            self.mapa_rutinas[i] = r

    def _mostrar_detalles_rutina(self, event):
        selected_index = self.lista_rutinas.curselection()
        if selected_index:
            index = selected_index[0]
            rutina_obj = self.mapa_rutinas.get(index)
            if rutina_obj:
                routine_data = obtener_detalles_rutina_con_ejercicios(rutina_obj.id_rutina) 
                if routine_data:
                    rutina = routine_data['rutina']
                    ejercicios = routine_data['ejercicios']
                    details = (f"Nombre: {rutina.nombre}\n"
                               f"Descripción: {rutina.descripcion}\n"
                               f"Duración: {rutina.duracion}\n\n"
                               f"Ejercicios Asociados:\n")
                    if ejercicios:
                        for ej in ejercicios:
                            reps_str = f"{ej.repeticiones} reps" if ej.repeticiones is not None else "N/A reps"
                            series_str = f"{ej.series} series" if ej.series is not None else "N/A series"
                            details += f"  - {ej.nombre} ({ej.tipo}, {reps_str}, {series_str})\n"
                    else:
                        details += "  (Ningún ejercicio asociado)\n"
                    self.etiqueta_detalles_rutina.config(text=details)
                else:
                    self.etiqueta_detalles_rutina.config(text="Error al cargar detalles de la rutina.")
            else:
                self.etiqueta_detalles_rutina.config(text="Selecciona una rutina para ver detalles.")
        else:
            self.etiqueta_detalles_rutina.config(text="Selecciona una rutina para ver detalles.")
            

    def _abrir_ventana_crear_rutina(self):
        VentanaCrearRutina(self.master, self.cargar_lista_rutinas)

    def _abrir_ventana_modificar_rutina(self):
        VentanaModificarRutina(self.master, self.cargar_lista_rutinas)

    def _abrir_ventana_eliminar_rutina(self):
        VentanaEliminarRutina(self.master, self.cargar_lista_rutinas)


    def _configurar_pestana_asignacion(self):
        tk.Label(self.pestana_asignacion, text="ASIGNAR RUTINAS A CLIENTES", font=("Arial", 18)).pack(pady=10)

        tk.Label(self.pestana_asignacion, text="Seleccionar Cliente:").pack(pady=5)
        self.variable_clientes_asignar = tk.StringVar(self.pestana_asignacion)
        self.menu_clientes_asignar = tk.OptionMenu(self.pestana_asignacion, self.variable_clientes_asignar, "") 
        self.menu_clientes_asignar.pack(pady=2)

        tk.Label(self.pestana_asignacion, text="Seleccionar Rutina:").pack(pady=5)
        self.variable_rutinas_asignar = tk.StringVar(self.pestana_asignacion)
        self.menu_rutinas_asignar = tk.OptionMenu(self.pestana_asignacion, self.variable_rutinas_asignar, "") 
        self.menu_rutinas_asignar.pack(pady=2)

        tk.Button(self.pestana_asignacion, text="Asignar Rutina Ahora", command=self._asignar_rutina_ahora).pack(pady=20)

        self._recargar_opciones_asignacion() 

    def _recargar_opciones_asignacion(self):
        self.todos_los_clientes = obtener_todos_los_clientes() 
        self.nombres_clientes_asignar = [f"{c.nombre} {c.apellido} ({c.email})" for c in self.todos_los_clientes]
        self.mapa_clientes_asignar = {name: c.id_usuario for name, c in zip(self.nombres_clientes_asignar, self.todos_los_clientes)}

        self.menu_clientes_asignar['menu'].delete(0, 'end')
        if self.nombres_clientes_asignar:
            for choice in self.nombres_clientes_asignar:
                self.menu_clientes_asignar['menu'].add_command(label=choice, command=tk._setit(self.variable_clientes_asignar, choice))
            self.variable_clientes_asignar.set(self.nombres_clientes_asignar[0])
        else:
            self.variable_clientes_asignar.set("No hay clientes")

        self.todas_las_rutinas_asignar = obtener_listado_rutinas() 
        self.nombres_rutinas_asignar = [r.nombre for r in self.todas_las_rutinas_asignar]
        self.mapa_rutinas_asignar = {r.nombre: r.id_rutina for r in self.todas_las_rutinas_asignar}

        self.menu_rutinas_asignar['menu'].delete(0, 'end')
        if self.nombres_rutinas_asignar:
            for choice in self.nombres_rutinas_asignar:
                self.menu_rutinas_asignar['menu'].add_command(label=choice, command=tk._setit(self.variable_rutinas_asignar, choice))
            self.variable_rutinas_asignar.set(self.nombres_rutinas_asignar[0])
        else:
            self.variable_rutinas_asignar.set("No hay rutinas")


    def _asignar_rutina_ahora(self):
        if not self.nombres_clientes_asignar or not self.nombres_rutinas_asignar:
            messagebox.showerror("Error de Asignación", "No hay clientes o rutinas disponibles para asignar.")
            return

        client_id = self.mapa_clientes_asignar[self.variable_clientes_asignar.get()]
        routine_id = self.mapa_rutinas_asignar[self.variable_rutinas_asignar.get()]

        success = asignar_rutina_a_cliente(self.user_info['id_usuario'], client_id, routine_id)  
        if success:
            messagebox.showinfo("Éxito", "Rutina asignada correctamente.")
            self.cargar_datos_rutina_clientes()
        else:
            messagebox.showerror("Error", "El cliente ya tiene rutina asignada")


    def _configurar_pestana_ejercicios(self):
        tk.Label(self.pestana_ejercicios, text="GESTIÓN DE EJERCICIOS", font=("Arial", 18)).pack(pady=10)

        manage_exercises_frame = tk.Frame(self.pestana_ejercicios)
        manage_exercises_frame.pack(fill="both", expand=True)

        list_frame = tk.Frame(manage_exercises_frame, bd=2, relief="groove")
        list_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        tk.Label(list_frame, text="Ejercicios Existentes", font=("Arial", 14)).pack(pady=5)
        self.lista_ejercicios_entrenador = tk.Listbox(list_frame, height=15, width=40)
        self.lista_ejercicios_entrenador.pack(pady=5, padx=5, fill="both", expand=True)
        self.lista_ejercicios_entrenador.bind("<<ListboxSelect>>", self._cargar_detalles_ejercicio_para_editar)
        self.cargar_lista_ejercicios()

        edit_frame = tk.Frame(manage_exercises_frame, bd=2, relief="groove")
        edit_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        tk.Label(edit_frame, text="Detalles del Ejercicio", font=("Arial", 14)).pack(pady=5)

        tk.Label(edit_frame, text="ID (Solo lectura):").pack(pady=2)
        self.entrada_id_ejercicio = tk.Entry(edit_frame, width=30, state='readonly')
        self.entrada_id_ejercicio.pack(pady=2)

        tk.Label(edit_frame, text="Nombre:").pack(pady=2)
        self.entrada_nombre_ej = tk.Entry(edit_frame, width=30)
        self.entrada_nombre_ej.pack(pady=2)

        tk.Label(edit_frame, text="Tipo:").pack(pady=2)
        self.entrada_tipo_ej = tk.Entry(edit_frame, width=30)
        self.entrada_tipo_ej.pack(pady=2)

        tk.Label(edit_frame, text="Repeticiones (opcional):").pack(pady=2)
        self.entrada_reps_ej = tk.Entry(edit_frame, width=30)
        self.entrada_reps_ej.pack(pady=2)

        tk.Label(edit_frame, text="Series (opcional):").pack(pady=2)
        self.entrada_series_ej = tk.Entry(edit_frame, width=30)
        self.entrada_series_ej.pack(pady=2)

        tk.Label(edit_frame, text="Descripción (opcional):").pack(pady=2)
        self.texto_desc_ej = tk.Text(edit_frame, height=4, width=30)
        self.texto_desc_ej.pack(pady=2)

       
        button_ej_frame = tk.Frame(edit_frame)
        button_ej_frame.pack(pady=10)
        tk.Button(button_ej_frame, text="Nuevo Ejercicio", command=self._limpiar_formulario_ejercicio).pack(side="left", padx=5)
        tk.Button(button_ej_frame, text="Guardar Cambios", command=self._guardar_o_actualizar_ejercicio).pack(side="left", padx=5)
        tk.Button(button_ej_frame, text="Eliminar Seleccionado", command=self._eliminar_ejercicio_seleccionado).pack(side="left", padx=5)


    def cargar_lista_ejercicios(self):
        self.lista_ejercicios_entrenador.delete(0, tk.END)
        self.todos_los_ejercicios_entrenador = obtener_todos_los_ejercicios() 
        self.mapa_ejercicios_entrenador = {}  
        if self.todos_los_ejercicios_entrenador:
            for i, ej in enumerate(self.todos_los_ejercicios_entrenador):
                self.lista_ejercicios_entrenador.insert(tk.END, f"{ej.nombre} ({ej.tipo})")
                self.mapa_ejercicios_entrenador[i] = ej
        else:
            self.lista_ejercicios_entrenador.insert(tk.END, "No hay ejercicios disponibles. Crea uno nuevo.")


    def _limpiar_formulario_ejercicio(self):
        self.entrada_id_ejercicio.config(state='normal')
        self.entrada_id_ejercicio.delete(0, tk.END)
        self.entrada_id_ejercicio.config(state='readonly')
        self.entrada_nombre_ej.delete(0, tk.END)
        self.entrada_tipo_ej.delete(0, tk.END)
        self.entrada_reps_ej.delete(0, tk.END)
        self.entrada_series_ej.delete(0, tk.END)
        self.texto_desc_ej.delete("1.0", tk.END)
        self.lista_ejercicios_entrenador.selection_clear(0, tk.END) 


    def _cargar_detalles_ejercicio_para_editar(self, event):
        selected_index = self.lista_ejercicios_entrenador.curselection()
        if selected_index:
            index = selected_index[0]
            ejercicio = self.mapa_ejercicios_entrenador.get(index)
            if ejercicio:
                self.entrada_id_ejercicio.config(state='normal')
                self.entrada_id_ejercicio.delete(0, tk.END)
                self.entrada_id_ejercicio.insert(0, str(ejercicio.id_ejercicio))
                self.entrada_id_ejercicio.config(state='readonly')

                self.entrada_nombre_ej.delete(0, tk.END)
                self.entrada_nombre_ej.insert(0, ejercicio.nombre)
                self.entrada_tipo_ej.delete(0, tk.END)
                self.entrada_tipo_ej.insert(0, ejercicio.tipo)
                self.entrada_reps_ej.delete(0, tk.END)
                self.entrada_reps_ej.insert(0, str(ejercicio.repeticiones) if ejercicio.repeticiones is not None else "")
                self.entrada_series_ej.delete(0, tk.END)
                self.entrada_series_ej.insert(0, str(ejercicio.series) if ejercicio.series is not None else "")
                self.texto_desc_ej.delete("1.0", tk.END)
                self.texto_desc_ej.insert("1.0", ejercicio.descripcion if ejercicio.descripcion is not None else "")
        else:
            self._limpiar_formulario_ejercicio()

    def _guardar_o_actualizar_ejercicio(self):
        ej_id_str = self.entrada_id_ejercicio.get()
        nombre = self.entrada_nombre_ej.get().strip()
        tipo = self.entrada_tipo_ej.get().strip()
        reps_str = self.entrada_reps_ej.get().strip()
        series_str = self.entrada_series_ej.get().strip()
        descripcion = self.texto_desc_ej.get("1.0", tk.END).strip()

        if not nombre or not tipo:
            messagebox.showerror("Error", "Nombre y Tipo de ejercicio son obligatorios.")
            return

        reps = None
        series = None
        if reps_str:
            try:
                reps = int(reps_str)
                if reps < 0: raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Repeticiones debe ser un número entero positivo o vacío.")
                return
        
        if series_str:
            try:
                series = int(series_str)
                if series < 0: raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Series debe ser un número entero positivo o vacío.")
                return

        success = False
        if ej_id_str:  
            ej_id = int(ej_id_str)
            success = modificar_ejercicio_existente(ej_id, nombre, tipo, reps, series, descripcion) 
            if success:
                messagebox.showinfo("Éxito", "Ejercicio actualizado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo actualizar el ejercicio. Puede que el nombre/tipo ya existan para otro ejercicio.")
        else:  
            new_ej = crear_nuevo_ejercicio(nombre, tipo, reps, series, descripcion)  
            if new_ej:
                messagebox.showinfo("Éxito", "Ejercicio creado con éxito.") 
                success = True
            else:
                messagebox.showerror("Error", "No se pudo crear el ejercicio. Puede que el nombre/tipo ya exista.")

        if success:
            self.cargar_lista_ejercicios()
            self._limpiar_formulario_ejercicio()


    def _eliminar_ejercicio_seleccionado(self):
        selected_index = self.lista_ejercicios_entrenador.curselection()
        if selected_index:
            index = selected_index[0]
            ejercicio = self.mapa_ejercicios_entrenador.get(index)
            if ejercicio:
                if messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que quieres eliminar el ejercicio '{ejercicio.nombre}'?"):
                    success = eliminar_ejercicio_existente(ejercicio.id_ejercicio) 
                    if success:
                        messagebox.showinfo("Éxito", "Ejercicio eliminado correctamente.")
                        self.cargar_lista_ejercicios()
                        self._limpiar_formulario_ejercicio()
                    else:
                        messagebox.showerror("Error", "No se pudo eliminar el ejercicio. Asegúrate de que no esté asociado a ninguna rutina activa.")
            else:
                messagebox.showerror("Error", "No se encontró el ejercicio seleccionado.")
        else:
            messagebox.showerror("Error", "Por favor, selecciona un ejercicio para eliminar.")


    def _configurar_pestana_clientes_rutinas(self):
        tk.Label(self.pestana_clientes_rutinas, text="VISUALIZAR RUTINAS DE CLIENTES", font=("Arial", 18)).pack(pady=10)

        columns = ("Cliente", "Rutina Asignada", "Fecha Asignación")
        self.arbol_clientes_rutinas = ttk.Treeview(self.pestana_clientes_rutinas, columns=columns, show="headings")
        self.arbol_clientes_rutinas.pack(pady=10, padx=10, fill="both", expand=True)

        for col in columns:
            self.arbol_clientes_rutinas.heading(col, text=col)
            self.arbol_clientes_rutinas.column(col, width=150, anchor="center")  

        self.cargar_datos_rutina_clientes()

        tk.Button(self.pestana_clientes_rutinas, text="Refrescar Lista", command=self.cargar_datos_rutina_clientes).pack(pady=10)

    def cargar_datos_rutina_clientes(self):
        for item in self.arbol_clientes_rutinas.get_children():
            self.arbol_clientes_rutinas.delete(item)

        clients_routines_data = ver_rutinas_de_clientes(self.user_info['id_usuario']) 

        if clients_routines_data:
            for entry in clients_routines_data:
                client_name = f"{entry['nombre_cliente']} {entry['apellido_cliente']}"
                routine_name = entry['nombre_rutina']
                fecha_asignado = entry['fecha_asignado']
                self.arbol_clientes_rutinas.insert("", tk.END, values=(client_name, routine_name, fecha_asignado))
        else:
            self.arbol_clientes_rutinas.insert("", tk.END, values=("No hay datos.", "", ""))

    def _desasignar_rutina_seleccionada(self):
        """
        Maneja la desasignación de una rutina seleccionada en el Treeview.
        """
        selected_item_iid = self.arbol_clientes_rutinas.focus() 
        
        if not selected_item_iid:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una asignación para desasignar.")
            return

        id_asignacion_a_eliminar = int(selected_item_iid) 

        if messagebox.askyesno("Confirmar Desasignación", 
                               f"¿Estás seguro de que quieres desasignar la rutina con ID de Asignación: {id_asignacion_a_eliminar}?"):
            success = desasignar_rutina_a_cliente(id_asignacion_a_eliminar) 
            if success:
                messagebox.showinfo("Éxito", "Rutina desasignada correctamente.")
                self.cargar_datos_rutina_clientes() 
            else:
                messagebox.showerror("Error", "No se pudo desasignar la rutina. Puede que ya no exista o haya un error.")
