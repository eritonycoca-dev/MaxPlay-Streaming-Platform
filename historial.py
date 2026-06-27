import tkinter as tk
from tkinter import messagebox
from conexionBD import obtener_conexion

def menu_historial(panel, colores, limpiar_panel, crear_tabla, crear_boton_panel):
    limpiar_panel()
    tk.Label(panel, text="Gestión de Historial", font=("Segoe UI", 22, "bold"),
             fg=colores["dorado"], bg=colores["panel"]).pack(pady=25)

    opciones = tk.Frame(panel, bg=colores["panel"])
    opciones.pack(pady=20)

    crear_boton_panel(opciones, "Ver historial", lambda: mostrar_historial(crear_tabla))
    crear_boton_panel(opciones, "Agregar visualización", lambda: agregar_historial(panel, colores, limpiar_panel, crear_boton_panel, crear_tabla))
    crear_boton_panel(opciones, "Eliminar visualización", lambda: eliminar_historial(panel, colores, limpiar_panel, crear_tabla))

def mostrar_historial(crear_tabla):
    crear_tabla(
        "Historial de visualización",
        ("id", "usuario", "contenido", "fecha", "tiempo"),
        {
            "id": "ID",
            "usuario": "ID Usuario",
            "contenido": "ID Contenido",
            "fecha": "Fecha visualización",
            "tiempo": "Tiempo visto"
        },
        "SELECT * FROM Historial"
    )

def agregar_historial(panel, colores, limpiar_panel, crear_boton_panel, crear_tabla):
    limpiar_panel()
    tk.Label(panel, text="Agregar visualización", font=("Segoe UI", 20, "bold"),
             fg=colores["dorado"], bg=colores["panel"]).pack(pady=15)

    datos = ["ID Usuario", "ID Contenido", "Fecha visualización (YYYY-MM-DD)", "Tiempo visto"]
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
                INSERT INTO Historial
                (id_usuario, id_contenido, fecha_visualizacion, tiempo_visto)
                VALUES (?, ?, ?, ?)
                """,
                valores
            )
            conexion.commit()
            conexion.close()
            messagebox.showinfo("MaxPlay", "Visualización agregada correctamente.")
            mostrar_historial(crear_tabla)

    crear_boton_panel(panel, "Guardar visualización", guardar)

def eliminar_historial(panel, colores, limpiar_panel, crear_tabla):
    limpiar_panel()
    tk.Label(panel, text="Eliminar visualización", font=("Segoe UI", 20, "bold"),
             fg=colores["dorado"], bg=colores["panel"]).pack(pady=15)

    tk.Label(panel, text="ID del historial a eliminar", fg=colores["texto"],
             bg=colores["panel"], font=("Segoe UI", 11, "bold")).pack()

    entrada_id = tk.Entry(panel, font=("Segoe UI", 11), width=30)
    entrada_id.pack(pady=10)

    def borrar():
        id_historial = entrada_id.get()
        if not id_historial:
            messagebox.showwarning("MaxPlay", "Ingresa el ID.")
            return

        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM Historial WHERE id_historial = ?", (id_historial,))
            conexion.commit()
            conexion.close()
            messagebox.showinfo("MaxPlay", "Registro eliminado correctamente.")
            mostrar_historial(crear_tabla)

    tk.Button(panel, text="Eliminar visualización", font=("Segoe UI", 12, "bold"),
              bg=colores["rojo"], fg="white", relief="flat", bd=0,
              cursor="hand2", width=22, height=2, command=borrar).pack(pady=20)
