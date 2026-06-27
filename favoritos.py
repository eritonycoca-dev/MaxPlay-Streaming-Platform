import tkinter as tk
from tkinter import messagebox
from conexionBD import obtener_conexion

def menu_favoritos(panel, colores, limpiar_panel, crear_tabla, crear_boton_panel):
    limpiar_panel()
    tk.Label(panel, text="Gestión de Favoritos", font=("Segoe UI", 22, "bold"),
             fg=colores["dorado"], bg=colores["panel"]).pack(pady=25)

    opciones = tk.Frame(panel, bg=colores["panel"])
    opciones.pack(pady=20)

    crear_boton_panel(opciones, "Ver favoritos", lambda: mostrar_favoritos(crear_tabla))
    crear_boton_panel(opciones, "Agregar favorito", lambda: agregar_favorito(panel, colores, limpiar_panel, crear_boton_panel, crear_tabla))
    crear_boton_panel(opciones, "Eliminar favorito", lambda: eliminar_favorito(panel, colores, limpiar_panel, crear_tabla))

def mostrar_favoritos(crear_tabla):
    crear_tabla(
        "Contenido favorito",
        ("id", "usuario", "contenido", "fecha"),
        {
            "id": "ID",
            "usuario": "ID Usuario",
            "contenido": "ID Contenido",
            "fecha": "Fecha agregado"
        },
        "SELECT * FROM Favorito"
    )

def agregar_favorito(panel, colores, limpiar_panel, crear_boton_panel, crear_tabla):
    limpiar_panel()
    tk.Label(panel, text="Agregar favorito", font=("Segoe UI", 20, "bold"),
             fg=colores["dorado"], bg=colores["panel"]).pack(pady=15)

    datos = ["ID Usuario", "ID Contenido", "Fecha agregado (YYYY-MM-DD)"]
    campos = {}
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
                INSERT INTO Favorito (id_usuario, id_contenido, fecha_agregado)
                VALUES (?, ?, ?)
                """,
                valores
            )
            conexion.commit()
            conexion.close()
            messagebox.showinfo("MaxPlay", "Favorito agregado correctamente.")
            mostrar_favoritos(crear_tabla)

    crear_boton_panel(panel, "Guardar favorito", guardar)

def eliminar_favorito(panel, colores, limpiar_panel, crear_tabla):
    limpiar_panel()
    tk.Label(panel, text="Eliminar favorito", font=("Segoe UI", 20, "bold"),
             fg=colores["dorado"], bg=colores["panel"]).pack(pady=15)

    tk.Label(panel, text="ID del favorito a eliminar", fg=colores["texto"],
             bg=colores["panel"], font=("Segoe UI", 11, "bold")).pack()

    entrada_id = tk.Entry(panel, font=("Segoe UI", 11), width=30)
    entrada_id.pack(pady=10)

    def borrar():
        id_favorito = entrada_id.get()
        if not id_favorito:
            messagebox.showwarning("MaxPlay", "Ingresa el ID.")
            return

        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM Favorito WHERE id_favorito = ?", (id_favorito,))
            conexion.commit()
            conexion.close()
            messagebox.showinfo("MaxPlay", "Favorito eliminado correctamente.")
            mostrar_favoritos(crear_tabla)

    tk.Button(panel, text="Eliminar favorito", font=("Segoe UI", 12, "bold"),
              bg=colores["rojo"], fg="white", relief="flat", bd=0,
              cursor="hand2", width=22, height=2, command=borrar).pack(pady=20)
