"""
Nombre del estudiante: [Sarah Melissa Carrejo Gaitán]
Grupo: [213022A_2204]
Programa: [Ingeniería en IA y ciencias de datos]
Código fuente: autoría propia

Problema 3 - Sistema de reabastecimiento de inventario.
Paradigma utilizado: programación estructurada y modular.
"""

import tkinter as tk
from tkinter import ttk



# Cada fila tiene: código, nombre, stock actual y stock mínimo requerido.
INVENTARIO_INICIAL = [
    ["A-101", "Cuadernos", 18, 30],
    ["A-102", "Lápices", 75, 50],
    ["A-103", "Marcadores", 12, 25],
    ["A-104", "Resmas de papel", 8, 20],
    ["A-105", "Carpetas", 40, 40],
    ["A-106", "Cintas adhesivas", 6, 15],
]

# Paleta inspirada en almacenamiento, abastecimiento y control de inventario.
AZUL_OSCURO = "#7B6CA8"
AZUL = "#8CB8E8"
VERDE = "#5EAD7A"
VERDE_SUAVE = "#E4F5E9"
NARANJA = "#EFA56B"
NARANJA_SUAVE = "#FFF0D8"
ROJO = "#A64D5F"
FONDO = "#F0F9FF"
BLANCO = "#FFFFFF"
TEXTO = "#493E5B"


def calcular_cantidad_pedir(stock_actual, stock_minimo):
    """Retorna las unidades necesarias para alcanzar el stock mínimo."""
    if not isinstance(stock_actual, int) or not isinstance(stock_minimo, int):
        raise TypeError("Los valores de stock deben ser números enteros.")

    if stock_actual < 0 or stock_minimo < 0:
        raise ValueError("Los valores de stock no pueden ser negativos.")

    if stock_actual < stock_minimo:
        return stock_minimo - stock_actual

    return 0


def limpiar_tabla(tabla):
    """Elimina todas las filas visibles de un Treeview."""
    for fila in tabla.get_children():
        tabla.delete(fila)


def cargar_inventario():
    """Carga la matriz base en la tabla superior."""
    limpiar_tabla(tabla_inventario)

    for codigo, nombre, stock_actual, stock_minimo in inventario:
        tabla_inventario.insert(
            "",
            tk.END,
            values=(codigo, nombre, stock_actual, stock_minimo),
        )


def analizar_inventario():
    """Recorre la matriz, usa el módulo de cálculo y muestra el reporte."""
    limpiar_tabla(tabla_reporte)
    articulos_reabastecer = 0

    print("\nREPORTE DE REABASTECIMIENTO")
    print("-" * 48)

    for codigo, nombre, stock_actual, stock_minimo in inventario:
        cantidad_pedir = calcular_cantidad_pedir(stock_actual, stock_minimo)

        if cantidad_pedir > 0:
            estado = "Reabastecer"
            etiqueta = "reabastecer"
            articulos_reabastecer += 1
        else:
            estado = "Stock suficiente"
            etiqueta = "suficiente"

        tabla_reporte.insert(
            "",
            tk.END,
            values=(nombre, stock_actual, stock_minimo, cantidad_pedir, estado),
            tags=(etiqueta,),
        )

        print(f"{nombre}: solicitar {cantidad_pedir} unidad(es)")

    etiqueta_resumen.config(
        text=(
            f"Análisis completado: {articulos_reabastecer} artículo(s) "
            "requieren reabastecimiento."
        ),
        fg=ROJO if articulos_reabastecer else VERDE,
    )


def restaurar_datos():
    """Restaura la matriz original y limpia el reporte."""
    global inventario
    inventario = [fila.copy() for fila in INVENTARIO_INICIAL]
    cargar_inventario()
    limpiar_tabla(tabla_reporte)
    etiqueta_resumen.config(
        text="Datos iniciales restaurados. Presione Analizar inventario.",
        fg=AZUL,
    )


# Copia independiente de la matriz inicial que se procesará en memoria.
inventario = [fila.copy() for fila in INVENTARIO_INICIAL]

# Ventana principal.
ventana = tk.Tk()
ventana.title("Control de inventario - Reabastecimiento")
ventana.geometry("990x730")
ventana.minsize(900, 650)
ventana.configure(bg=FONDO)

estilo = ttk.Style()
estilo.theme_use("clam")
estilo.configure(
    "Inventario.Treeview",
    font=("Segoe UI", 10),
    rowheight=28,
    background=BLANCO,
    fieldbackground=BLANCO,
    foreground=TEXTO,
)
estilo.configure(
    "Inventario.Treeview.Heading",
    font=("Segoe UI", 10, "bold"),
    background=AZUL_OSCURO,
    foreground=BLANCO,
    relief="flat",
)
estilo.map(
    "Inventario.Treeview",
    background=[("selected", "#BAE6FD")],
    foreground=[("selected", TEXTO)],
)

# Encabezado.
encabezado = tk.Frame(ventana, bg=AZUL_OSCURO, padx=32, pady=22)
encabezado.pack(fill="x")

tk.Label(
    encabezado,
    text="CONTROL DE INVENTARIO",
    font=("Segoe UI", 21, "bold"),
    fg=BLANCO,
    bg=AZUL_OSCURO,
).pack(anchor="w")
tk.Label(
    encabezado,
    text="Análisis de existencias y cálculo de reabastecimiento",
    font=("Segoe UI", 11),
    fg="#BAE6FD",
    bg=AZUL_OSCURO,
).pack(anchor="w", pady=(3, 0))

contenido = tk.Frame(ventana, bg=FONDO)
contenido.pack(fill="both", expand=True, padx=32, pady=22)

tk.Label(
    contenido,
    text="Matriz de inventario",
    font=("Segoe UI", 13, "bold"),
    fg=TEXTO,
    bg=FONDO,
).pack(anchor="w")
tk.Label(
    contenido,
    text="Cada artículo contiene código, nombre, stock actual y stock mínimo requerido.",
    font=("Segoe UI", 10),
    fg="#45646C",
    bg=FONDO,
).pack(anchor="w", pady=(2, 9))

marco_tabla_inventario = tk.Frame(contenido, bg=BLANCO, padx=2, pady=2)
marco_tabla_inventario.pack(fill="x")

columnas_inventario = ("codigo", "nombre", "actual", "minimo")
tabla_inventario = ttk.Treeview(
    marco_tabla_inventario,
    columns=columnas_inventario,
    show="headings",
    height=6,
    style="Inventario.Treeview",
)

configuracion_inventario = [
    ("codigo", "Código", 120, "center"),
    ("nombre", "Artículo", 350, "w"),
    ("actual", "Stock actual", 170, "center"),
    ("minimo", "Stock mínimo", 170, "center"),
]
for columna, titulo, ancho, alineacion in configuracion_inventario:
    tabla_inventario.heading(columna, text=titulo)
    tabla_inventario.column(columna, width=ancho, anchor=alineacion, stretch=True)
tabla_inventario.pack(fill="x")

marco_botones = tk.Frame(contenido, bg=FONDO)
marco_botones.pack(fill="x", pady=16)

tk.Button(
    marco_botones,
    text="Analizar inventario",
    command=analizar_inventario,
    font=("Segoe UI", 11, "bold"),
    bg=NARANJA,
    fg=BLANCO,
    activebackground="#C66D09",
    activeforeground=BLANCO,
    relief="flat",
    cursor="hand2",
    padx=18,
    pady=10,
).pack(side="left")

tk.Button(
    marco_botones,
    text="Restaurar datos",
    command=restaurar_datos,
    font=("Segoe UI", 11),
    bg="#DCEFF5",
    fg=AZUL_OSCURO,
    activebackground="#BFDBE5",
    relief="flat",
    cursor="hand2",
    padx=18,
    pady=10,
).pack(side="left", padx=10)

tk.Button(
    marco_botones,
    text="Salir",
    command=ventana.destroy,
    font=("Segoe UI", 11),
    bg="#FEE2E2",
    fg=ROJO,
    activebackground="#FECACA",
    relief="flat",
    cursor="hand2",
    padx=18,
    pady=10,
).pack(side="right")

tk.Label(
    contenido,
    text="Reporte de reabastecimiento",
    font=("Segoe UI", 13, "bold"),
    fg=TEXTO,
    bg=FONDO,
).pack(anchor="w")

marco_tabla_reporte = tk.Frame(contenido, bg=BLANCO, padx=2, pady=2)
marco_tabla_reporte.pack(fill="both", expand=True, pady=(9, 0))

columnas_reporte = ("nombre", "actual", "minimo", "pedir", "estado")
tabla_reporte = ttk.Treeview(
    marco_tabla_reporte,
    columns=columnas_reporte,
    show="headings",
    height=6,
    style="Inventario.Treeview",
)

configuracion_reporte = [
    ("nombre", "Artículo", 300, "w"),
    ("actual", "Stock actual", 140, "center"),
    ("minimo", "Stock mínimo", 140, "center"),
    ("pedir", "Cantidad a pedir", 160, "center"),
    ("estado", "Estado", 180, "center"),
]
for columna, titulo, ancho, alineacion in configuracion_reporte:
    tabla_reporte.heading(columna, text=titulo)
    tabla_reporte.column(columna, width=ancho, anchor=alineacion, stretch=True)
tabla_reporte.pack(fill="both", expand=True)

tabla_reporte.tag_configure("reabastecer", background=NARANJA_SUAVE, foreground=ROJO)
tabla_reporte.tag_configure("suficiente", background=VERDE_SUAVE, foreground="#065F46")

etiqueta_resumen = tk.Label(
    ventana,
    text="Presione Analizar inventario para generar el reporte.",
    font=("Segoe UI", 10, "bold"),
    fg=AZUL,
    bg=FONDO,
)
etiqueta_resumen.pack(anchor="w", padx=32, pady=(0, 18))

cargar_inventario()
ventana.mainloop()
