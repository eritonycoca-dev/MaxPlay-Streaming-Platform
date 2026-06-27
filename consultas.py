import tkinter as tk

def menu_consultas(panel, colores, limpiar_panel, crear_tabla, crear_boton_panel):
    limpiar_panel()

    tk.Label(panel, text="Consultas Avanzadas", font=("Segoe UI", 22, "bold"),
             fg=colores["dorado"], bg=colores["panel"]).pack(pady=25)

    opciones = tk.Frame(panel, bg=colores["panel"])
    opciones.pack(pady=20)

    crear_boton_panel(opciones, "Top 3 usuarios con más vistas", lambda: top_usuarios(crear_tabla))
    crear_boton_panel(opciones, "Contenido más visto", lambda: contenido_mas_visto(crear_tabla))
    crear_boton_panel(opciones, "Visualizaciones enero - mayo", lambda: vistas_enero_mayo(crear_tabla))
    crear_boton_panel(opciones, "Ingresos por plan", lambda: ingresos_por_plan(crear_tabla))

def top_usuarios(crear_tabla):
    crear_tabla(
        "Top 3 usuarios con más visualizaciones",
        ("usuario", "visualizaciones"),
        {
            "usuario": "Usuario",
            "visualizaciones": "Visualizaciones"
        },
        """
        SELECT TOP 3
            u.nombre + ' ' + u.apellido AS Usuario,
            COUNT(h.id_historial) AS Visualizaciones
        FROM Historial h
        INNER JOIN Usuario u ON h.id_usuario = u.id_usuario
        GROUP BY u.nombre, u.apellido
        ORDER BY Visualizaciones DESC
        """
    )

def contenido_mas_visto(crear_tabla):
    crear_tabla(
        "Contenido más visto",
        ("contenido", "visualizaciones"),
        {
            "contenido": "Contenido",
            "visualizaciones": "Visualizaciones"
        },
        """
        SELECT
            c.titulo AS Contenido,
            COUNT(h.id_historial) AS Visualizaciones
        FROM Historial h
        INNER JOIN Contenido c ON h.id_contenido = c.id_contenido
        GROUP BY c.titulo
        ORDER BY Visualizaciones DESC
        """
    )

def vistas_enero_mayo(crear_tabla):
    crear_tabla(
        "Visualizaciones entre enero y mayo",
        ("usuario", "contenido", "fecha", "tiempo"),
        {
            "usuario": "Usuario",
            "contenido": "Contenido",
            "fecha": "Fecha",
            "tiempo": "Tiempo visto"
        },
        """
        SELECT
            u.nombre + ' ' + u.apellido AS Usuario,
            c.titulo AS Contenido,
            h.fecha_visualizacion AS Fecha,
            h.tiempo_visto AS Tiempo
        FROM Historial h
        INNER JOIN Usuario u ON h.id_usuario = u.id_usuario
        INNER JOIN Contenido c ON h.id_contenido = c.id_contenido
        WHERE MONTH(h.fecha_visualizacion) BETWEEN 1 AND 5
        ORDER BY h.fecha_visualizacion
        """
    )

def ingresos_por_plan(crear_tabla):
    crear_tabla(
        "Ingresos estimados por plan",
        ("plan", "usuarios", "ingresos"),
        {
            "plan": "Plan",
            "usuarios": "Usuarios",
            "ingresos": "Ingresos"
        },
        """
        SELECT
            tipo_plan AS Plan,
            COUNT(*) AS Usuarios,
            SUM(precio) AS Ingresos
        FROM Suscripcion
        GROUP BY tipo_plan
        ORDER BY Ingresos DESC
        """
    )
