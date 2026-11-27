"""
Nombre del estudiante: [Sarah Melissa Carrejo Gaitán]
Grupo: [213022A_2204]
Programa: [Ingeniería en IA y ciencias de datos]
Código fuente: autoría propia

Problema 3 - Sistema de reabastecimiento de inventario.
Paradigma utilizado: programación estructurada y modular.
"""

import csv
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


# Cada fila contiene: código, nombre, stock actual y stock mínimo requerido.
INVENTARIO_INICIAL = [
    ["A-101", "Cuadernos", 18, 30],
    ["A-102", "Lápices", 75, 50],
    ["A-103", "Marcadores", 12, 25],
    ["A-104", "Resmas de papel", 8, 20],
    ["A-105", "Carpetas", 40, 40],
    ["A-106", "Cintas adhesivas", 6, 15],
]

# Paleta pastel. El naranja conserva los pendientes y el verde el stock suficiente.
MORADO = "#7B6CA8"
AZUL = "#8CB8E8"
AZUL_SUAVE = "#EAF4FF"
ROSADO = "#F4B6C2"
ROSADO_SUAVE = "#FCEEF2"
VERDE = "#5EAD7A"
VERDE_SUAVE = "#E4F5E9"
NARANJA = "#EFA56B"
NARANJA_SUAVE = "#FFF0D8"
ROJO = "#A64D5F"
FONDO = "#FCF6FF"
BLANCO = "#FFFFFF"
TEXTO = "#493E5B"


def calcular_cantidad_pedir(stock_actual, stock_minimo):
    """Retorna las unidades necesarias para alcanzar el stock mínimo."""
    if not isinstance(stock_actual, int) or not isinstance(stock_minimo, int):
        raise TypeError("Los valores de stock deben ser números enteros.")
    if stock_actual < 0 or stock_minimo < 0:
        raise ValueError("Los valores de stock no pueden ser negativos.")
    return max(stock_minimo - stock_actual, 0)


def crear_articulo(codigo, nombre, stock_actual, stock_minimo):
    """Valida y devuelve una fila de inventario con datos normalizados."""
    codigo_limpio = str(codigo).strip().upper()
    nombre_limpio = str(nombre).strip()

    if not codigo_limpio or not nombre_limpio:
        raise ValueError("El código y el nombre del artículo son obligatorios.")

    try:
        actual = int(stock_actual)
        minimo = int(stock_minimo)
    except (TypeError, ValueError) as error:
        raise ValueError("Los valores de stock deben ser enteros.") from error

    if actual < 0 or minimo < 0:
        raise ValueError("Los valores de stock no pueden ser negativos.")

    return [codigo_limpio, nombre_limpio, actual, minimo]


def generar_reporte(inventario):
    """Crea filas de reporte: código, nombre, existencias, pedido y estado."""
    reporte = []
    for codigo, nombre, stock_actual, stock_minimo in inventario:
        cantidad_pedir = calcular_cantidad_pedir(stock_actual, stock_minimo)
        estado = "Reabastecer" if cantidad_pedir > 0 else "Stock suficiente"
        reporte.append(
            [codigo, nombre, stock_actual, stock_minimo, cantidad_pedir, estado]
        )
    return reporte


class AplicacionInventario(tk.Tk):
    """Interfaz gráfica para gestionar y analizar una matriz de inventario."""

    def __init__(self):
        super().__init__()
        self.inventario = [fila.copy() for fila in INVENTARIO_INICIAL]
        self.filtro_var = tk.StringVar(value="Todos")
        self._crear_ventana()
        self._crear_estilos()
        self._crear_interfaz()
        self.mostrar_inventario()
        self.actualizar_indicadores()

    def _crear_ventana(self):
        self.title("Control de inventario - Reabastecimiento")
        self.geometry("1120x900")
        self.minsize(980, 760)
        self.configure(bg=FONDO)

    def _crear_estilos(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure(
            "Inventario.Treeview",
            font=("Segoe UI", 10),
            rowheight=29,
            background=BLANCO,
            fieldbackground=BLANCO,
            foreground=TEXTO,
        )
        estilo.configure(
            "Inventario.Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background=MORADO,
            foreground=BLANCO,
            relief="flat",
        )
        estilo.map(
            "Inventario.Treeview",
            background=[("selected", "#DDD6FE")],
            foreground=[("selected", TEXTO)],
        )
        estilo.configure("Filtro.TCombobox", font=("Segoe UI", 10), padding=4)

    def _crear_interfaz(self):
        encabezado = tk.Frame(self, bg=MORADO, padx=32, pady=19)
        encabezado.pack(fill="x")
        tk.Label(
            encabezado,
            text="CONTROL DE INVENTARIO",
            font=("Segoe UI", 21, "bold"),
            fg=BLANCO,
            bg=MORADO,
        ).pack(anchor="w")
        tk.Label(
            encabezado,
            text="Gestione existencias y calcule el reabastecimiento necesario",
            font=("Segoe UI", 11),
            fg="#F3E8FF",
            bg=MORADO,
        ).pack(anchor="w", pady=(3, 0))

        contenido = tk.Frame(self, bg=FONDO)
        contenido.pack(fill="both", expand=True, padx=30, pady=18)
        self._crear_indicadores(contenido)
        self._crear_tabla_inventario(contenido)
        self._crear_formulario(contenido)
        self._crear_controles(contenido)
        self._crear_reporte(contenido)

        self.etiqueta_estado = tk.Label(
            self,
            text="Seleccione un artículo para editarlo o agregue uno nuevo.",
            font=("Segoe UI", 10, "bold"),
            fg=MORADO,
            bg=FONDO,
        )
        self.etiqueta_estado.pack(anchor="w", padx=30, pady=(0, 14))

    def _crear_indicadores(self, padre):
        marco = tk.Frame(padre, bg=FONDO)
        marco.pack(fill="x", pady=(0, 14))
        self.indicador_articulos = self._crear_tarjeta_indicador(
            marco, "ARTÍCULOS", AZUL_SUAVE, AZUL
        )
        self.indicador_pendientes = self._crear_tarjeta_indicador(
            marco, "PENDIENTES", NARANJA_SUAVE, NARANJA
        )
        self.indicador_unidades = self._crear_tarjeta_indicador(
            marco, "UNIDADES A PEDIR", ROSADO_SUAVE, ROJO
        )

    def _crear_tarjeta_indicador(self, padre, titulo, fondo, color):
        tarjeta = tk.Frame(padre, bg=fondo, padx=18, pady=12)
        tarjeta.pack(side="left", fill="x", expand=True, padx=4)
        tk.Label(
            tarjeta,
            text=titulo,
            font=("Segoe UI", 9, "bold"),
            fg=TEXTO,
            bg=fondo,
        ).pack(anchor="w")
        valor = tk.Label(
            tarjeta,
            text="0",
            font=("Segoe UI", 20, "bold"),
            fg=color,
            bg=fondo,
        )
        valor.pack(anchor="w", pady=(2, 0))
        return valor

    def _crear_tabla_inventario(self, padre):
        encabezado = tk.Frame(padre, bg=FONDO)
        encabezado.pack(fill="x")
        tk.Label(
            encabezado,
            text="Matriz de inventario",
            font=("Segoe UI", 13, "bold"),
            fg=TEXTO,
            bg=FONDO,
        ).pack(side="left")
        tk.Label(
            encabezado,
            text="Filtro:",
            font=("Segoe UI", 10),
            fg=TEXTO,
            bg=FONDO,
        ).pack(side="right", padx=(8, 4))
        filtro = ttk.Combobox(
            encabezado,
            textvariable=self.filtro_var,
            values=("Todos", "Solo pendientes", "Stock suficiente"),
            state="readonly",
            width=18,
            style="Filtro.TCombobox",
        )
        filtro.pack(side="right")
        filtro.bind("<<ComboboxSelected>>", lambda evento: self.mostrar_inventario())

        marco = tk.Frame(padre, bg=BLANCO, padx=2, pady=2)
        marco.pack(fill="x", pady=(8, 14))
        columnas = ("codigo", "nombre", "actual", "minimo")
        self.tabla_inventario = ttk.Treeview(
            marco,
            columns=columnas,
            show="headings",
            height=6,
            style="Inventario.Treeview",
        )
        configuracion = [
            ("codigo", "Código", 130, "center"),
            ("nombre", "Artículo", 390, "w"),
            ("actual", "Stock actual", 180, "center"),
            ("minimo", "Stock mínimo", 180, "center"),
        ]
        for columna, titulo, ancho, alineacion in configuracion:
            self.tabla_inventario.heading(columna, text=titulo)
            self.tabla_inventario.column(
                columna, width=ancho, anchor=alineacion, stretch=True
            )
        self.tabla_inventario.pack(fill="x")
        self.tabla_inventario.bind("<<TreeviewSelect>>", self.cargar_articulo_seleccionado)

    def _crear_formulario(self, padre):
        marco = tk.LabelFrame(
            padre,
            text="Agregar o editar artículo",
            font=("Segoe UI", 11, "bold"),
            fg=MORADO,
            bg=BLANCO,
            padx=14,
            pady=12,
        )
        marco.pack(fill="x", pady=(0, 12))
        self.entrada_codigo = self._crear_campo(marco, "Código", 0, 0, 15)
        self.entrada_nombre = self._crear_campo(marco, "Nombre", 0, 2, 29)
        self.entrada_actual = self._crear_campo(marco, "Stock actual", 0, 4, 11)
        self.entrada_minimo = self._crear_campo(marco, "Stock mínimo", 0, 6, 11)

        botones = [
            ("Agregar", self.agregar_articulo, AZUL, BLANCO),
            ("Actualizar", self.actualizar_articulo, MORADO, BLANCO),
            ("Eliminar", self.eliminar_articulo, ROSADO, TEXTO),
            ("Limpiar campos", self.limpiar_formulario, "#EEE9F9", TEXTO),
        ]
        for indice, (texto, accion, fondo, color) in enumerate(botones):
            tk.Button(
                marco,
                text=texto,
                command=accion,
                font=("Segoe UI", 10, "bold" if indice < 2 else "normal"),
                bg=fondo,
                fg=color,
                relief="flat",
                cursor="hand2",
                padx=12,
                pady=8,
            ).grid(row=0, column=8 + indice, padx=4, pady=5)

    def _crear_campo(self, padre, etiqueta, fila, columna, ancho):
        tk.Label(
            padre,
            text=etiqueta,
            font=("Segoe UI", 9, "bold"),
            fg=TEXTO,
            bg=BLANCO,
        ).grid(row=fila, column=columna, sticky="w", padx=(0, 5))
        entrada = tk.Entry(
            padre,
            width=ancho,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1,
        )
        entrada.grid(row=fila, column=columna + 1, padx=(0, 12), pady=5)
        return entrada

    def _crear_controles(self, padre):
        marco = tk.Frame(padre, bg=FONDO)
        marco.pack(fill="x", pady=(0, 12))
        botones = [
            ("Analizar inventario", self.analizar_inventario, NARANJA, BLANCO),
            ("Exportar CSV", self.exportar_csv, AZUL_SUAVE, TEXTO),
            ("Importar CSV", self.importar_csv, "#EEE9F9", TEXTO),
            ("Restaurar datos", self.restaurar_datos, "#F3E8FF", TEXTO),
        ]
        for texto, accion, fondo, color in botones:
            tk.Button(
                marco,
                text=texto,
                command=accion,
                font=("Segoe UI", 10, "bold" if texto.startswith("Analizar") else "normal"),
                bg=fondo,
                fg=color,
                relief="flat",
                cursor="hand2",
                padx=14,
                pady=9,
            ).pack(side="left", padx=(0, 7))
        tk.Button(
            marco,
            text="Salir",
            command=self.destroy,
            font=("Segoe UI", 10),
            bg=ROSADO_SUAVE,
            fg=ROJO,
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=9,
        ).pack(side="right")

    def _crear_reporte(self, padre):
        tk.Label(
            padre,
            text="Reporte de reabastecimiento",
            font=("Segoe UI", 13, "bold"),
            fg=TEXTO,
            bg=FONDO,
        ).pack(anchor="w")
        marco = tk.Frame(padre, bg=BLANCO, padx=2, pady=2)
        marco.pack(fill="both", expand=True, pady=(8, 0))
        columnas = ("codigo", "nombre", "actual", "minimo", "pedir", "estado")
        self.tabla_reporte = ttk.Treeview(
            marco,
            columns=columnas,
            show="headings",
            height=7,
            style="Inventario.Treeview",
        )
        configuracion = [
            ("codigo", "Código", 100, "center"),
            ("nombre", "Artículo", 280, "w"),
            ("actual", "Stock actual", 125, "center"),
            ("minimo", "Stock mínimo", 125, "center"),
            ("pedir", "Cantidad a pedir", 145, "center"),
            ("estado", "Estado", 170, "center"),
        ]
        for columna, titulo, ancho, alineacion in configuracion:
            self.tabla_reporte.heading(columna, text=titulo)
            self.tabla_reporte.column(
                columna, width=ancho, anchor=alineacion, stretch=True
            )
        self.tabla_reporte.pack(fill="both", expand=True)
        self.tabla_reporte.tag_configure(
            "reabastecer", background=NARANJA_SUAVE, foreground=ROJO
        )
        self.tabla_reporte.tag_configure(
            "suficiente", background=VERDE_SUAVE, foreground="#28683F"
        )

    def limpiar_tabla(self, tabla):
        for fila in tabla.get_children():
            tabla.delete(fila)

    def mostrar_inventario(self):
        self.limpiar_tabla(self.tabla_inventario)
        filtro = self.filtro_var.get()
        for articulo in self.inventario:
            codigo, nombre, actual, minimo = articulo
            pedido = calcular_cantidad_pedir(actual, minimo)
            mostrar = (
                filtro == "Todos"
                or (filtro == "Solo pendientes" and pedido > 0)
                or (filtro == "Stock suficiente" and pedido == 0)
            )
            if mostrar:
                self.tabla_inventario.insert("", tk.END, iid=codigo, values=articulo)

    def actualizar_indicadores(self):
        reporte = generar_reporte(self.inventario)
        pendientes = [fila for fila in reporte if fila[4] > 0]
        unidades = sum(fila[4] for fila in pendientes)
        self.indicador_articulos.config(text=str(len(self.inventario)))
        self.indicador_pendientes.config(text=str(len(pendientes)))
        self.indicador_unidades.config(text=str(unidades))

    def cargar_articulo_seleccionado(self, evento=None):
        seleccion = self.tabla_inventario.selection()
        if not seleccion:
            return
        codigo, nombre, actual, minimo = self.tabla_inventario.item(seleccion[0], "values")
        self._poner_campos(codigo, nombre, actual, minimo)
        self.etiqueta_estado.config(text=f"Artículo {codigo} cargado para edición.", fg=MORADO)

    def _poner_campos(self, codigo, nombre, actual, minimo):
        for campo, valor in (
            (self.entrada_codigo, codigo),
            (self.entrada_nombre, nombre),
            (self.entrada_actual, actual),
            (self.entrada_minimo, minimo),
        ):
            campo.delete(0, tk.END)
            campo.insert(0, str(valor))

    def _leer_formulario(self):
        return crear_articulo(
            self.entrada_codigo.get(),
            self.entrada_nombre.get(),
            self.entrada_actual.get(),
            self.entrada_minimo.get(),
        )

    def agregar_articulo(self):
        try:
            articulo = self._leer_formulario()
        except ValueError as error:
            messagebox.showerror("Datos no válidos", str(error), parent=self)
            return
        if any(fila[0] == articulo[0] for fila in self.inventario):
            messagebox.showerror("Código repetido", "Ya existe un artículo con ese código.", parent=self)
            return
        self.inventario.append(articulo)
        self._refrescar_despues_de_cambio("Artículo agregado correctamente.")

    def actualizar_articulo(self):
        seleccion = self.tabla_inventario.selection()
        if not seleccion:
            messagebox.showwarning("Seleccione un artículo", "Seleccione una fila para actualizarla.", parent=self)
            return
        codigo_original = seleccion[0]
        try:
            articulo = self._leer_formulario()
        except ValueError as error:
            messagebox.showerror("Datos no válidos", str(error), parent=self)
            return
        if articulo[0] != codigo_original and any(fila[0] == articulo[0] for fila in self.inventario):
            messagebox.showerror("Código repetido", "Ya existe un artículo con ese código.", parent=self)
            return
        for indice, fila in enumerate(self.inventario):
            if fila[0] == codigo_original:
                self.inventario[indice] = articulo
                break
        self._refrescar_despues_de_cambio("Artículo actualizado correctamente.")

    def eliminar_articulo(self):
        seleccion = self.tabla_inventario.selection()
        if not seleccion:
            messagebox.showwarning("Seleccione un artículo", "Seleccione una fila para eliminarla.", parent=self)
            return
        if len(self.inventario) <= 5:
            messagebox.showwarning("Mínimo requerido", "El inventario debe conservar al menos cinco artículos.", parent=self)
            return
        codigo = seleccion[0]
        if messagebox.askyesno("Confirmar eliminación", f"¿Desea eliminar el artículo con código {codigo}?", parent=self):
            self.inventario = [fila for fila in self.inventario if fila[0] != codigo]
            self._refrescar_despues_de_cambio("Artículo eliminado correctamente.")

    def limpiar_formulario(self):
        for campo in (self.entrada_codigo, self.entrada_nombre, self.entrada_actual, self.entrada_minimo):
            campo.delete(0, tk.END)
        self.tabla_inventario.selection_remove(self.tabla_inventario.selection())
        self.entrada_codigo.focus_set()

    def _refrescar_despues_de_cambio(self, mensaje):
        self.mostrar_inventario()
        self.actualizar_indicadores()
        self.mostrar_reporte()
        self.limpiar_formulario()
        self.etiqueta_estado.config(text=mensaje, fg=VERDE)

    def mostrar_reporte(self):
        self.limpiar_tabla(self.tabla_reporte)
        for fila in generar_reporte(self.inventario):
            etiqueta = "reabastecer" if fila[4] > 0 else "suficiente"
            self.tabla_reporte.insert("", tk.END, values=fila, tags=(etiqueta,))

    def analizar_inventario(self):
        self.mostrar_reporte()
        reporte = generar_reporte(self.inventario)
        pendientes = [fila for fila in reporte if fila[4] > 0]
        print("\nREPORTE DE REABASTECIMIENTO")
        print("-" * 55)
        for codigo, nombre, actual, minimo, pedido, estado in reporte:
            print(f"{codigo} | {nombre}: solicitar {pedido} unidad(es) - {estado}")
        self.etiqueta_estado.config(
            text=f"Análisis completado: {len(pendientes)} artículo(s) requieren reabastecimiento.",
            fg=ROJO if pendientes else VERDE,
        )

    def restaurar_datos(self):
        if messagebox.askyesno("Restaurar inventario", "Se perderán los cambios no guardados. ¿Desea continuar?", parent=self):
            self.inventario = [fila.copy() for fila in INVENTARIO_INICIAL]
            self.filtro_var.set("Todos")
            self._refrescar_despues_de_cambio("Datos iniciales restaurados.")

    def exportar_csv(self):
        ruta = filedialog.asksaveasfilename(
            parent=self,
            title="Exportar inventario",
            defaultextension=".csv",
            filetypes=[("Archivo CSV", "*.csv")],
            initialfile="inventario.csv",
        )
        if not ruta:
            return
        with Path(ruta).open("w", newline="", encoding="utf-8-sig") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["codigo", "nombre", "stock_actual", "stock_minimo"])
            escritor.writerows(self.inventario)
        self.etiqueta_estado.config(text="Inventario exportado correctamente a CSV.", fg=VERDE)

    def importar_csv(self):
        ruta = filedialog.askopenfilename(parent=self, title="Importar inventario", filetypes=[("Archivo CSV", "*.csv")])
        if not ruta:
            return
        try:
            with Path(ruta).open("r", newline="", encoding="utf-8-sig") as archivo:
                lector = csv.DictReader(archivo)
                requeridos = {"codigo", "nombre", "stock_actual", "stock_minimo"}
                if not lector.fieldnames or not requeridos.issubset(lector.fieldnames):
                    raise ValueError("El CSV no contiene las columnas requeridas.")
                inventario_nuevo = []
                codigos = set()
                for numero_fila, fila in enumerate(lector, start=2):
                    articulo = crear_articulo(fila["codigo"], fila["nombre"], fila["stock_actual"], fila["stock_minimo"])
                    if articulo[0] in codigos:
                        raise ValueError(f"Código repetido en la fila {numero_fila}: {articulo[0]}.")
                    codigos.add(articulo[0])
                    inventario_nuevo.append(articulo)
            if len(inventario_nuevo) < 5:
                raise ValueError("El archivo debe contener al menos cinco artículos.")
        except (OSError, ValueError) as error:
            messagebox.showerror("No se pudo importar", str(error), parent=self)
            return
        self.inventario = inventario_nuevo
        self.filtro_var.set("Todos")
        self._refrescar_despues_de_cambio("Inventario importado correctamente desde CSV.")


if __name__ == "__main__":
    aplicacion = AplicacionInventario()
    aplicacion.mainloop()
