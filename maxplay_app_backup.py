import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from conexionBD import obtener_conexion

# ===============================
# COLORES MAXPLAY
# ===============================
COLOR_FONDO = "#0B0B0B"
COLOR_PANEL = "#151515"
COLOR_PANEL_2 = "#1F1F1F"
COLOR_DORADO = "#D4AF37"
COLOR_VERDE = "#556B2F"
COLOR_VERDE_OSCURO = "#3E4F22"
COLOR_TEXTO = "#F5F5F5"
COLOR_ROJO = "#8C1A1A"


# ===============================
# FUNCIONES GENERALES
# ===============================
def limpiar_panel():
    for widget in panel_contenido.winfo_children():
        widget.destroy()


def obtener_total(tabla):
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
        total = cursor.fetchone()[0]
        conexion.close()
        return total
    return 0


def probar_conexion():
    conexion = obtener_conexion()
    if conexion:
        messagebox.showinfo("MaxPlay", "Conexión exitosa a la base de datos.")
        conexion.close()
    else:
        messagebox.showerror("MaxPlay", "No se pudo conectar a la base de datos.")


# ===============================
# ESTILO DE TABLAS
# ===============================
def configurar_estilo_tabla():
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Treeview",
        background=COLOR_PANEL_2,
        foreground=COLOR_TEXTO,
        fieldbackground=COLOR_PANEL_2,
        rowheight=28,
        font=("Segoe UI", 10)
    )

    style.configure(
        "Treeview.Heading",
        background=COLOR_VERDE,
        foreground="white",
        font=("Segoe UI", 10, "bold")
    )

    style.map(
        "Treeview",
        background=[("selected", COLOR_DORADO)],
        foreground=[("selected", "black")]
    )


def crear_tabla(titulo, columnas, encabezados, consulta):
    limpiar_panel()

    tk.Label(
        panel_contenido,
        text=titulo,
        font=("Segoe UI", 20, "bold"),
        fg=COLOR_DORADO,
        bg=COLOR_PANEL
    ).pack(pady=15)

    contenedor_tabla = tk.Frame(panel_contenido, bg=COLOR_PANEL)
    contenedor_tabla.pack(fill="both", expand=True, padx=20, pady=10)

    scroll_y = ttk.Scrollbar(contenedor_tabla, orient="vertical")
    scroll_x = ttk.Scrollbar(contenedor_tabla, orient="horizontal")

    tabla = ttk.Treeview(
        contenedor_tabla,
        columns=columnas,
        show="headings",
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )

    scroll_y.config(command=tabla.yview)
    scroll_x.config(command=tabla.xview)

    scroll_y.pack(side="right", fill="y")
    scroll_x.pack(side="bottom", fill="x")
    tabla.pack(side="left", fill="both", expand=True)

    for col, texto in encabezados.items():
        tabla.heading(col, text=texto)
        tabla.column(col, width=140, anchor="center")

    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute(consulta)

        for fila in cursor.fetchall():
            tabla.insert("", tk.END, values=tuple(fila))

        conexion.close()
    else:
        messagebox.showerror("MaxPlay", "No se pudo conectar a la base de datos.")


# ===============================
# DASHBOARD
# ===============================
def mostrar_dashboard():
    limpiar_panel()

    tk.Label(
        panel_contenido,
        text="Panel Administrativo de MaxPlay",
        font=("Segoe UI", 22, "bold"),
        fg=COLOR_DORADO,
        bg=COLOR_PANEL
    ).pack(pady=25)

    tk.Label(
        panel_contenido,
        text="Resumen general de la plataforma de streaming",
        font=("Segoe UI", 12),
        fg=COLOR_TEXTO,
        bg=COLOR_PANEL
    ).pack(pady=5)

    tarjetas = tk.Frame(panel_contenido, bg=COLOR_PANEL)
    tarjetas.pack(pady=35)

    datos = [
        ("👤 Usuarios", obtener_total("Usuario")),
        ("🎬 Contenido", obtener_total("Contenido")),
        ("💳 Suscripciones", obtener_total("Suscripcion")),
        ("⭐ Favoritos", obtener_total("Favorito")),
        ("📺 Historial", obtener_total("Historial")),
    ]

    for i, (titulo, valor) in enumerate(datos):
        card = tk.Frame(
            tarjetas,
            bg=COLOR_PANEL_2,
            width=190,
            height=110,
            highlightbackground=COLOR_VERDE,
            highlightthickness=1
        )
        card.grid(row=i // 3, column=i % 3, padx=15, pady=15)
        card.pack_propagate(False)

        tk.Label(
            card,
            text=titulo,
            font=("Segoe UI", 12, "bold"),
            fg=COLOR_TEXTO,
            bg=COLOR_PANEL_2
        ).pack(pady=(18, 5))

        tk.Label(
            card,
            text=str(valor),
            font=("Segoe UI", 24, "bold"),
            fg=COLOR_DORADO,
            bg=COLOR_PANEL_2
        ).pack()


# ===============================
# VISUALIZACIÓN DE TABLAS
# ===============================
def mostrar_usuarios():
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


def mostrar_contenido():
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


def mostrar_suscripciones():
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


def mostrar_favoritos():
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


def mostrar_historial():
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


# ===============================
# CRUD USUARIOS
# ===============================
def menu_usuarios():
    limpiar_panel()

    tk.Label(
        panel_contenido,
        text="Gestión de Usuarios",
        font=("Segoe UI", 22, "bold"),
        fg=COLOR_DORADO,
        bg=COLOR_PANEL
    ).pack(pady=25)

    opciones = tk.Frame(panel_contenido, bg=COLOR_PANEL)
    opciones.pack(pady=20)

    crear_boton_panel(opciones, "Ver usuarios", mostrar_usuarios)
    crear_boton_panel(opciones, "Agregar usuario", agregar_usuario)
    crear_boton_panel(opciones, "Actualizar usuario", actualizar_usuario)
    crear_boton_panel(opciones, "Eliminar usuario", eliminar_usuario)


def crear_boton_panel(padre, texto, comando):
    tk.Button(
        padre,
        text=texto,
        font=("Segoe UI", 12, "bold"),
        bg=COLOR_VERDE,
        fg="white",
        activebackground="#8C6A1A",
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        width=22,
        height=2,
        command=comando
    ).pack(pady=8)


def agregar_usuario():
    limpiar_panel()

    tk.Label(
        panel_contenido,
        text="Agregar nuevo usuario",
        font=("Segoe UI", 20, "bold"),
        fg=COLOR_DORADO,
        bg=COLOR_PANEL
    ).pack(pady=15)

    campos = {}
    datos = ["Nombre", "Apellido", "Correo", "Contraseña", "Fecha registro (YYYY-MM-DD)"]

    formulario = tk.Frame(panel_contenido, bg=COLOR_PANEL)
    formulario.pack(pady=10)

    for dato in datos:
        tk.Label(
            formulario,
            text=dato,
            font=("Segoe UI", 10, "bold"),
            fg=COLOR_TEXTO,
            bg=COLOR_PANEL
        ).pack()

        entrada = tk.Entry(formulario, font=("Segoe UI", 10), width=40)
        entrada.pack(pady=5)
        campos[dato] = entrada

    def guardar_usuario():
        nombre = campos["Nombre"].get()
        apellido = campos["Apellido"].get()
        correo = campos["Correo"].get()
        contrasena = campos["Contraseña"].get()
        fecha = campos["Fecha registro (YYYY-MM-DD)"].get()

        if not nombre or not apellido or not correo or not contrasena or not fecha:
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
                (nombre, apellido, correo, contrasena, fecha)
            )
            conexion.commit()
            conexion.close()

            messagebox.showinfo("MaxPlay", "Usuario agregado correctamente.")
            mostrar_usuarios()

    crear_boton_panel(panel_contenido, "Guardar usuario", guardar_usuario)


def actualizar_usuario():
    limpiar_panel()

    tk.Label(
        panel_contenido,
        text="Actualizar usuario",
        font=("Segoe UI", 20, "bold"),
        fg=COLOR_DORADO,
        bg=COLOR_PANEL
    ).pack(pady=15)

    entradas = {}
    labels = ["ID Usuario", "Nuevo correo", "Nueva contraseña"]

    formulario = tk.Frame(panel_contenido, bg=COLOR_PANEL)
    formulario.pack(pady=10)

    for label in labels:
        tk.Label(
            formulario,
            text=label,
            font=("Segoe UI", 10, "bold"),
            fg=COLOR_TEXTO,
            bg=COLOR_PANEL
        ).pack()

        entrada = tk.Entry(formulario, font=("Segoe UI", 10), width=40)
        entrada.pack(pady=5)
        entradas[label] = entrada

    def guardar_cambios():
        id_usuario = entradas["ID Usuario"].get()
        nuevo_correo = entradas["Nuevo correo"].get()
        nueva_contrasena = entradas["Nueva contraseña"].get()

        if not id_usuario or not nuevo_correo or not nueva_contrasena:
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
                (nuevo_correo, nueva_contrasena, id_usuario)
            )
            conexion.commit()
            conexion.close()

            messagebox.showinfo("MaxPlay", "Usuario actualizado correctamente.")
            mostrar_usuarios()

    crear_boton_panel(panel_contenido, "Actualizar", guardar_cambios)


def eliminar_usuario():
    limpiar_panel()

    tk.Label(
        panel_contenido,
        text="Eliminar usuario",
        font=("Segoe UI", 20, "bold"),
        fg=COLOR_DORADO,
        bg=COLOR_PANEL
    ).pack(pady=15)

    tk.Label(
        panel_contenido,
        text="ID del usuario a eliminar",
        font=("Segoe UI", 11, "bold"),
        fg=COLOR_TEXTO,
        bg=COLOR_PANEL
    ).pack()

    entrada_id = tk.Entry(panel_contenido, font=("Segoe UI", 11), width=30)
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
                cursor.execute(
                    "DELETE FROM Usuario WHERE id_usuario = ?",
                    (id_usuario,)
                )
                conexion.commit()
                conexion.close()

                messagebox.showinfo("MaxPlay", "Usuario eliminado correctamente.")
                mostrar_usuarios()

        except Exception:
            messagebox.showerror(
                "MaxPlay",
                "No se puede eliminar este usuario porque tiene registros relacionados."
            )

    tk.Button(
        panel_contenido,
        text="Eliminar",
        font=("Segoe UI", 12, "bold"),
        bg=COLOR_ROJO,
        fg="white",
        activebackground="#B22222",
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        width=22,
        height=2,
        command=borrar
    ).pack(pady=20)


# ===============================
# VENTANA PRINCIPAL
# ===============================
ventana = tk.Tk()
ventana.title("MaxPlay Admin")
ventana.geometry("1180x720")
ventana.configure(bg=COLOR_FONDO)
ventana.resizable(False, False)

configurar_estilo_tabla()

# HEADER
header = tk.Frame(ventana, bg=COLOR_FONDO)
header.pack(fill="x", pady=8)

try:
    imagen = Image.open("logo.png")
    imagen = imagen.resize((115, 70))
    logo = ImageTk.PhotoImage(imagen)

    tk.Label(header, image=logo, bg=COLOR_FONDO).pack()
except:
    tk.Label(
        header,
        text="MAXPLAY",
        font=("Segoe UI", 28, "bold"),
        fg=COLOR_DORADO,
        bg=COLOR_FONDO
    ).pack()

tk.Label(
    header,
    text="MAXPLAY ADMIN",
    font=("Segoe UI", 24, "bold"),
    fg=COLOR_DORADO,
    bg=COLOR_FONDO
).pack()

tk.Label(
    header,
    text="Sistema administrativo de plataforma de streaming",
    font=("Segoe UI", 11),
    fg=COLOR_TEXTO,
    bg=COLOR_FONDO
).pack()

# CONTENEDOR PRINCIPAL
contenedor = tk.Frame(ventana, bg=COLOR_FONDO)
contenedor.pack(fill="both", expand=True, padx=18, pady=8)

# MENÚ LATERAL
menu_lateral = tk.Frame(contenedor, bg=COLOR_PANEL, width=210)
menu_lateral.pack(side="left", fill="y", padx=(0, 15))
menu_lateral.pack_propagate(False)

tk.Label(
    menu_lateral,
    text="MENÚ",
    font=("Segoe UI", 16, "bold"),
    fg=COLOR_DORADO,
    bg=COLOR_PANEL
).pack(pady=18)


def boton_menu(texto, comando):
    tk.Button(
        menu_lateral,
        text=texto,
        font=("Segoe UI", 10, "bold"),
        bg=COLOR_VERDE,
        fg="white",
        activebackground="#8C6A1A",
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        width=22,
        height=2,
        command=comando
    ).pack(pady=5)


boton_menu("🏠 Dashboard", mostrar_dashboard)
boton_menu("🔌 Probar conexión", probar_conexion)
boton_menu("👤 Usuarios", menu_usuarios)
boton_menu("🎬 Contenido", mostrar_contenido)
boton_menu("💳 Suscripciones", mostrar_suscripciones)
boton_menu("⭐ Favoritos", mostrar_favoritos)
boton_menu("📺 Historial", mostrar_historial)
boton_menu("🚪 Salir", ventana.destroy)

# PANEL PRINCIPAL
panel_contenido = tk.Frame(contenedor, bg=COLOR_PANEL)
panel_contenido.pack(side="right", fill="both", expand=True)

mostrar_dashboard()

ventana.mainloop()
