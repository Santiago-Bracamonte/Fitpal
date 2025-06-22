import tkinter as tk
from tkinter import messagebox
import sqlite3

def abrir_ventana_registro():
    ventana = tk.Toplevel()
    ventana.title("Registro de Usuario")
    ventana.geometry("300x350")
    
    tk.Label(ventana, text="Nombre").pack()
    entry_nombre = tk.Entry(ventana)
    entry_nombre.pack()

    tk.Label(ventana, text="Apellido").pack()
    entry_apellido = tk.Entry(ventana)
    entry_apellido.pack()

    tk.Label(ventana, text="Email").pack()
    entry_email = tk.Entry(ventana)
    entry_email.pack()

    tk.Label(ventana, text="Contraseña").pack()
    entry_contrasena = tk.Entry(ventana, show="*")
    entry_contrasena.pack()

    tk.Label(ventana, text="Rol (cliente / entrenador)").pack()
    entry_rol = tk.Entry(ventana)
    entry_rol.pack()

    def registrar_usuario():
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        email = entry_email.get()
        contrasena = entry_contrasena.get()
        rol = entry_rol.get()

        if not all([nombre, apellido, email, contrasena, rol]):
            messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos.")
            return
        
    
        try:
            conn = sqlite3.connect("fitpal.db")
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Usuario (nombre, apellido, email, contrasena, rol)
                VALUES (?, ?, ?, ?, ?)
            ''', (nombre, apellido, email, contrasena, rol))
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            ventana.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    tk.Button(ventana, text="Registrarse", command=registrar_usuario).pack(pady=10)
