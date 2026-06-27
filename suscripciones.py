import tkinter as tk
from tkinter import messagebox
from conexionBD import obtener_conexion

def menu_suscripciones(panel, colores, limpiar_panel, crear_tabla, crear_boton_panel):
    limpiar_panel()
    tk.Label(panel, text="Gestión de Suscripciones", font=("Segoe UI", 22, "bold"),
             fg=colores["dorado"], bg=colores["panel"]).pack(pady=25)

    opciones = tk.Frame(panel, bg=colores["panel"])
    opciones.pack(pady=20)

    crear_boton_panel(opciones, "Ver suscripciones", lambda: mostrar_suscripciones(crear_tabla))
    crear_boton_panel(opciones, "Agregar suscripción", lambda: agregar_suscripcion(panel, colores, limpiar_panel, crear_boton_panel, crear_tabla))
    crear_boton_panel(opciones, "Actualizar suscripción", lambda: actualizar_suscripcion(panel, colores, limpiar_panel, crear_boton_panel, crear_tabla))
    crear_boton_panel(opciones, "Eliminar suscripción", lambda: eliminar_suscripcion(panel, colores, limpiar_panel, crear_tabla))

def mostrar_suscripciones(crear_tabla):
    crear_tabla(
        "Suscripciones registradas",
        ("id", "usuario", "plan", "precio", "inicio", "fin", "estado"),
        {
            "id": "ID",
            "usuario": "ID Usuario",
            "plan": "Plan",
            "precio": "Precio",
            "inicio": "Fecha inicio",
            "fin": "Fecha fin",
            "estado": "Estado"
        },
        "SELECT * FROM Suscripcion"
    )

def agregar_suscripcion(panel, colores, limpiar_panel, crear_boton_panel, crear_tabla):
    limpiar_panel()
    tk.Label(panel, text="Agregar suscripción", font=("Segoe UI", 20, "bold"),
             fg=colores["dorado"], bg=colores["panel"]).pack(pady=15)

    datos = ["ID Usuario", "Tipo plan", "Precio", "Fecha inicio (YYYY-MM-DD)", "Fecha fin (YYYY-MM-DD)", "Estado"]
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
                INSERT INTO Suscripcion
                (id_usuario, tipo_plan, precio, fecha_inicio, fecha_fin, estado)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                valores
            )
            conexion.commit()
            conexion.close()
            messagebox.showinfo("MaxPlay", "Suscripción agregada correctamente.")
            mostrar_suscripciones(crear_tabla)

    crear_boton_panel(panel, "Guardar suscripción", guardar)

def actualizar_suscripcion(panel, colores, limpiar_panel, crear_boton_panel, crear_tabla):
    limpiar_panel()
    tk.Label(panel, text="Actualizar suscripción", font=("Segoe UI", 20, "bold"),
             fg=colores["dorado"], bg=colores["panel"]).pack(pady=15)

    datos = ["ID Suscripción", "Nuevo plan", "Nuevo estado"]
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
        id_suscripcion = campos["ID Suscripción"].get()
        plan = campos["Nuevo plan"].get()
        estado = campos["Nuevo estado"].get()

        if not id_suscripcion or not plan or not estado:
            messagebox.showwarning("MaxPlay", "Completa todos los campos.")
            return

        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute(
                """
                UPDATE Suscripcion
                SET tipo_plan = ?, estado = ?
                WHERE id_suscripcion = ?
                """,
                (plan, estado, id_suscripcion)
            )
            conexion.commit()
            conexion.close()
            messagebox.showinfo("MaxPlay", "Suscripción actualizada correctamente.")
            mostrar_suscripciones(crear_tabla)

    crear_boton_panel(panel, "Actualizar suscripción", guardar)

def eliminar_suscripcion(panel, colores, limpiar_panel, crear_tabla):
    limpiar_panel()
    tk.Label(panel, text="Eliminar suscripción", font=("Segoe UI", 20, "bold"),
             fg=colores["dorado"], bg=colores["panel"]).pack(pady=15)

    tk.Label(panel, text="ID de la suscripción a eliminar", fg=colores["texto"],
             bg=colores["panel"], font=("Segoe UI", 11, "bold")).pack()

    entrada_id = tk.Entry(panel, font=("Segoe UI", 11), width=30)
    entrada_id.pack(pady=10)

    def borrar():
        id_suscripcion = entrada_id.get()
        if not id_suscripcion:
            messagebox.showwarning("MaxPlay", "Ingresa el ID.")
            return

        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM Suscripcion WHERE id_suscripcion = ?", (id_suscripcion,))
            conexion.commit()
            conexion.close()
            messagebox.showinfo("MaxPlay", "Suscripción eliminada correctamente.")
            mostrar_suscripciones(crear_tabla)

    tk.Button(panel, text="Eliminar suscripción", font=("Segoe UI", 12, "bold"),
              bg=colores["rojo"], fg="white", relief="flat", bd=0,
              cursor="hand2", width=22, height=2, command=borrar).pack(pady=20)
