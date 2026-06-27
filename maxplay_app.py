import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from conexionBD import obtener_conexion

from usuarios import menu_usuarios
from contenido import menu_contenido
from suscripciones import menu_suscripciones
from favoritos import menu_favoritos
from historial import menu_historial
from consultas import menu_consultas

COLOR_FONDO = "#0B0B0B"
COLOR_PANEL = "#151515"
COLOR_PANEL_2 = "#1F1F1F"
COLOR_DORADO = "#D4AF37"
COLOR_VERDE = "#556B2F"
COLOR_TEXTO = "#F5F5F5"

COLORES = {
    "fondo": COLOR_FONDO,
    "panel": COLOR_PANEL,
    "panel2": COLOR_PANEL_2,
    "dorado": COLOR_DORADO,
    "verde": COLOR_VERDE,
    "texto": COLOR_TEXTO,
    "rojo": "#8C1A1A"
}

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

def mostrar_dashboard():
    limpiar_panel()

    tk.Label(
        panel_contenido,
        text="Panel Administrativo de MaxPlay",
        font=("Segoe UI", 22, "bold"),
        fg=COLOR_DORADO,
        bg=COLOR_PANEL
    ).pack(pady=25)

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

        tk.Label(card, text=titulo, font=("Segoe UI", 12, "bold"),
                 fg=COLOR_TEXTO, bg=COLOR_PANEL_2).pack(pady=(18, 5))

        tk.Label(card, text=str(valor), font=("Segoe UI", 24, "bold"),
                 fg=COLOR_DORADO, bg=COLOR_PANEL_2).pack()

ventana = tk.Tk()
ventana.title("MaxPlay Admin")
ventana.geometry("1180x720")
ventana.configure(bg=COLOR_FONDO)
ventana.resizable(False, False)

configurar_estilo_tabla()

header = tk.Frame(ventana, bg=COLOR_FONDO)
header.pack(fill="x", pady=8)

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

contenedor = tk.Frame(ventana, bg=COLOR_FONDO)
contenedor.pack(fill="both", expand=True, padx=18, pady=8)

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

panel_contenido = tk.Frame(contenedor, bg=COLOR_PANEL)
panel_contenido.pack(side="right", fill="both", expand=True)

boton_menu("🏠 Dashboard", mostrar_dashboard)
boton_menu("🔌 Probar conexión", probar_conexion)
boton_menu("👤 Usuarios", lambda: menu_usuarios(panel_contenido, COLORES, limpiar_panel, crear_tabla, crear_boton_panel))
boton_menu("🎬 Contenido", lambda: menu_contenido(panel_contenido, COLORES, limpiar_panel, crear_tabla, crear_boton_panel))

boton_menu("💳 Suscripciones", lambda: menu_suscripciones(panel_contenido, COLORES, limpiar_panel, crear_tabla, crear_boton_panel))
boton_menu("⭐ Favoritos", lambda: menu_favoritos(panel_contenido, COLORES, limpiar_panel, crear_tabla, crear_boton_panel))
boton_menu("📺 Historial", lambda: menu_historial(panel_contenido, COLORES, limpiar_panel, crear_tabla, crear_boton_panel))
boton_menu("📊 Reportes", lambda: menu_consultas(panel_contenido, COLORES, limpiar_panel, crear_tabla, crear_boton_panel))

boton_menu("🚪 Salir", ventana.destroy)

mostrar_dashboard()
ventana.mainloop()
