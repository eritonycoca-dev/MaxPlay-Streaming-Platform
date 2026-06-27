import tkinter as tk
from tkinter import messagebox
from conexionBD import obtener_conexion

def menu_usuarios(panel, colores, limpiar_panel, crear_tabla, crear_boton_panel):
    limpiar_panel()

    tk.Label(panel, text="Gestión de Usuarios", font=("Segoe UI", 22, "bold"),
             fg=colores["dorado"], bg=colores["panel"]).pack(pady=25)

    opciones = tk.Frame(panel, bg=colores["panel"])
    opciones.pack(pady=20)

    crear_boton_panel(opciones, "Ver usuarios", lambda: mostrar_usuarios(crear_tabla))
    crear_boton_panel(opciones, "Agregar usuario", lambda: agregar_usuario(panel, colores, limpiar_panel, crear_boton_panel, crear_tabla))
    crear_boton_panel(opciones, "Actualizar usuario", lambda: actualizar_usuario(panel, colores, limpiar_panel, crear_boton_panel, crear_tabla))
    crear_boton_panel(opciones, "Eliminar usuario", lambda: eliminar_usuario(panel, colores, limpiar_panel, crear_tabla))

def mostrar_usuarios(crear_tabla):
    crear_tabla(
        "Usuarios registrados",
        ("id", "nombre", "apellido", "correo", "contrasena", "fecha"),
        {
            "id": "ID",
            "nombre": "Nombre",
            "apellido": "Apellido",
            "correo": "Correo",
            "contrasena": "Contraseña",
            "fecha": "Fecha registro"
        },
        "SELECT * FROM Usuario"
    )

def agregar_usuario(panel, colores, limpiar_panel, crear_boton_panel, crear_tabla):
    limpiar_panel()

    tk.Label(panel, text="Agregar nuevo usuario", font=("Segoe UI", 20, "bold"),
             fg=colores["dorado"], bg=colores["panel"]).pack(pady=15)

    campos = {}
    datos = ["Nombre", "Apellido", "Correo", "Contraseña", "Fecha registro (YYYY-MM-DD)"]

    formulario = tk.Frame(panel, bg=colores["panel"])
    formulario.pack(pady=10)

    for dato in datos:
        tk.Label(formulario, text=dato, fg=colores["texto"], bg=colores["panel"],
                 font=("Segoe UI", 10, "bold")).pack()

        entrada = tk.Entry(formulario, font=("Segoe UI", 10), width=40)
        entrada.pack(pady=5)
        campos[dato] = entrada

    def guardar():
        valores = [campos[dato].get() for dato in datos]

        if "" in valores:
            messagebox.showwarning("MaxPlay", "Completa todos los campos.")
            return

        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute(
                """
                INSERT INTO Usuario (nombre, apellido, correo, contrasena, fecha_registro)
                VALUES (?, ?, ?, ?, ?)
                """,
                valores
            )
            conexion.commit()
            conexion.close()

            messagebox.showinfo("MaxPlay", "Usuario agregado correctamente.")
            mostrar_usuarios(crear_tabla)

    crear_boton_panel(panel, "Guardar usuario", guardar)

def actualizar_usuario(panel, colores, limpiar_panel, crear_boton_panel, crear_tabla):
    limpiar_panel()

    tk.Label(panel, text="Actualizar usuario", font=("Segoe UI", 20, "bold"),
             fg=colores["dorado"], bg=colores["panel"]).pack(pady=15)

    entradas = {}
    datos = ["ID Usuario", "Nuevo correo", "Nueva contraseña"]

    formulario = tk.Frame(panel, bg=colores["panel"])
    formulario.pack(pady=10)

    for dato in datos:
        tk.Label(formulario, text=dato, fg=colores["texto"], bg=colores["panel"],
                 font=("Segoe UI", 10, "bold")).pack()

        entrada = tk.Entry(formulario, font=("Segoe UI", 10), width=40)
        entrada.pack(pady=5)
        entradas[dato] = entrada

    def guardar():
        id_usuario = entradas["ID Usuario"].get()
        correo = entradas["Nuevo correo"].get()
        contrasena = entradas["Nueva contraseña"].get()

        if not id_usuario or not correo or not contrasena:
            messagebox.showwarning("MaxPlay", "Completa todos los campos.")
            return

        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute(
                """
                UPDATE Usuario
                SET correo = ?, contrasena = ?
                WHERE id_usuario = ?
                """,
                (correo, contrasena, id_usuario)
            )
            conexion.commit()
            conexion.close()

            messagebox.showinfo("MaxPlay", "Usuario actualizado correctamente.")
            mostrar_usuarios(crear_tabla)

    crear_boton_panel(panel, "Actualizar", guardar)

def eliminar_usuario(panel, colores, limpiar_panel, crear_tabla):
    limpiar_panel()

    tk.Label(panel, text="Eliminar usuario", font=("Segoe UI", 20, "bold"),
             fg=colores["dorado"], bg=colores["panel"]).pack(pady=15)

    tk.Label(panel, text="ID del usuario a eliminar", fg=colores["texto"],
             bg=colores["panel"], font=("Segoe UI", 11, "bold")).pack()

    entrada_id = tk.Entry(panel, font=("Segoe UI", 11), width=30)
    entrada_id.pack(pady=10)

    def borrar():
        id_usuario = entrada_id.get()

        if not id_usuario:
            messagebox.showwarning("MaxPlay", "Ingresa el ID del usuario.")
            return

        try:
            conexion = obtener_conexion()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM Usuario WHERE id_usuario = ?", (id_usuario,))
                conexion.commit()
                conexion.close()

                messagebox.showinfo("MaxPlay", "Usuario eliminado correctamente.")
                mostrar_usuarios(crear_tabla)

        except Exception:
            messagebox.showerror("MaxPlay", "No se puede eliminar este usuario porque tiene registros relacionados.")

    tk.Button(panel, text="Eliminar", font=("Segoe UI", 12, "bold"),
              bg=colores["rojo"], fg="white", relief="flat", bd=0,
              cursor="hand2", width=22, height=2, command=borrar).pack(pady=20)
