import tkinter as tk
from tkinter import messagebox
from conexionBD import obtener_conexion

def menu_contenido(panel, colores, limpiar_panel, crear_tabla, crear_boton_panel):
    limpiar_panel()

    tk.Label(panel, text="Gestión de Contenido", font=("Segoe UI", 22, "bold"),
             fg=colores["dorado"], bg=colores["panel"]).pack(pady=25)

    opciones = tk.Frame(panel, bg=colores["panel"])
    opciones.pack(pady=20)

    crear_boton_panel(opciones, "Ver contenido", lambda: mostrar_contenido(crear_tabla))
    crear_boton_panel(opciones, "Agregar contenido", lambda: agregar_contenido(panel, colores, limpiar_panel, crear_boton_panel, crear_tabla))
    crear_boton_panel(opciones, "Actualizar contenido", lambda: actualizar_contenido(panel, colores, limpiar_panel, crear_boton_panel, crear_tabla))
    crear_boton_panel(opciones, "Eliminar contenido", lambda: eliminar_contenido(panel, colores, limpiar_panel, crear_tabla))

def mostrar_contenido(crear_tabla):
    crear_tabla(
        "Catálogo de contenido",
        ("id", "titulo", "tipo", "anio", "clasificacion", "genero"),
        {
            "id": "ID",
            "titulo": "Título",
            "tipo": "Tipo",
            "anio": "Año",
            "clasificacion": "Clasificación",
            "genero": "ID Género"
        },
        "SELECT * FROM Contenido"
    )

def agregar_contenido(panel, colores, limpiar_panel, crear_boton_panel, crear_tabla):
    limpiar_panel()

    tk.Label(panel, text="Agregar contenido", font=("Segoe UI", 20, "bold"),
             fg=colores["dorado"], bg=colores["panel"]).pack(pady=15)

    campos = {}
    datos = ["Título", "Tipo contenido", "Año lanzamiento", "Clasificación", "ID Género"]

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
                INSERT INTO Contenido
                (titulo, tipo_contenido, anio_lanzamiento, clasificacion, id_genero)
                VALUES (?, ?, ?, ?, ?)
                """,
                valores
            )
            conexion.commit()
            conexion.close()

            messagebox.showinfo("MaxPlay", "Contenido agregado correctamente.")
            mostrar_contenido(crear_tabla)

    crear_boton_panel(panel, "Guardar contenido", guardar)

def actualizar_contenido(panel, colores, limpiar_panel, crear_boton_panel, crear_tabla):
    limpiar_panel()

    tk.Label(panel, text="Actualizar contenido", font=("Segoe UI", 20, "bold"),
             fg=colores["dorado"], bg=colores["panel"]).pack(pady=15)

    campos = {}
    datos = ["ID Contenido", "Nuevo título", "Nueva clasificación"]

    formulario = tk.Frame(panel, bg=colores["panel"])
    formulario.pack(pady=10)

    for dato in datos:
        tk.Label(formulario, text=dato, fg=colores["texto"], bg=colores["panel"],
                 font=("Segoe UI", 10, "bold")).pack()

        entrada = tk.Entry(formulario, font=("Segoe UI", 10), width=40)
        entrada.pack(pady=5)
        campos[dato] = entrada

    def guardar():
        id_contenido = campos["ID Contenido"].get()
        titulo = campos["Nuevo título"].get()
        clasificacion = campos["Nueva clasificación"].get()

        if not id_contenido or not titulo or not clasificacion:
            messagebox.showwarning("MaxPlay", "Completa todos los campos.")
            return

        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute(
                """
                UPDATE Contenido
                SET titulo = ?, clasificacion = ?
                WHERE id_contenido = ?
                """,
                (titulo, clasificacion, id_contenido)
            )
            conexion.commit()
            conexion.close()

            messagebox.showinfo("MaxPlay", "Contenido actualizado correctamente.")
            mostrar_contenido(crear_tabla)

    crear_boton_panel(panel, "Actualizar contenido", guardar)

def eliminar_contenido(panel, colores, limpiar_panel, crear_tabla):
    limpiar_panel()

    tk.Label(panel, text="Eliminar contenido", font=("Segoe UI", 20, "bold"),
             fg=colores["dorado"], bg=colores["panel"]).pack(pady=15)

    tk.Label(panel, text="ID del contenido a eliminar", fg=colores["texto"],
             bg=colores["panel"], font=("Segoe UI", 11, "bold")).pack()

    entrada_id = tk.Entry(panel, font=("Segoe UI", 11), width=30)
    entrada_id.pack(pady=10)

    def borrar():
        id_contenido = entrada_id.get()

        if not id_contenido:
            messagebox.showwarning("MaxPlay", "Ingresa el ID del contenido.")
            return

        try:
            conexion = obtener_conexion()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM Contenido WHERE id_contenido = ?", (id_contenido,))
                conexion.commit()
                conexion.close()

                messagebox.showinfo("MaxPlay", "Contenido eliminado correctamente.")
                mostrar_contenido(crear_tabla)

        except Exception:
            messagebox.showerror("MaxPlay", "No se puede eliminar este contenido porque tiene registros relacionados.")

    tk.Button(panel, text="Eliminar contenido", font=("Segoe UI", 12, "bold"),
              bg=colores["rojo"], fg="white", relief="flat", bd=0,
              cursor="hand2", width=22, height=2, command=borrar).pack(pady=20)
