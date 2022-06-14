from sqlite3 import Row
from tkinter import Label
from tkinter import Tk
from tkinter import ttk
from tkinter import Menu
from tkinter import StringVar
from tkinter import BooleanVar
from tkinter import Entry
from tkinter import Button
from tkinter.colorchooser import askcolor
from turtle import color
from sympy import root

import modelo

class Panel:

    def __init__(self, window):

        """ Función que inicializa el panel y contenido del mismo """

        self.mi_ventana = window
        self.mi_ventana.title("Grupo N°10 Entrega Final UTN")
        self.mi_ventana.iconbitmap("utn_logo.ico")

        
        # -----------LISTAS DATOS A GUARDAR------------
        

        self.lista_carga = []
        self.deudas_tree = []

        self.var_nombre = StringVar()
        self.var_apellido = StringVar()
        self.var_concepto = StringVar()
        self.var_importe = StringVar()
        self.var_diacarga = StringVar()
        self.var_mescarga = StringVar()
        self.var_aniocarga = StringVar()
        self.var_diavenc = StringVar()
        self.var_mesvenc = StringVar()
        self.var_aniovenc = StringVar()
        self.carga = StringVar()
        self.vencimiento = StringVar()
        self.var_pagado = BooleanVar()

        self.titulo = Label(
            self.mi_ventana,
            text="Por favor ingrese los datos de identificación del deudor y el monto de la deuda",
            bg="#808080",
            fg="#ffffff",
            height=1,
            width=20,
        )

        self.titulo.grid(
            row=0, column=0, columnspan=11, padx=1, pady=1, sticky="w" + "e"
        )

        self.nombre = Label(self.mi_ventana, text="Nombre", border=5, width=10)
        self.nombre.grid(row=1, column=0, sticky="w")
        self.entry_nombre = Entry(self.mi_ventana, textvariable=self.var_nombre)
        self.entry_nombre.grid(row=1, column=1)

        self.apellido = Label(self.mi_ventana, text="Apellido", border=5, width=10)
        self.apellido.grid(row=2, column=0, sticky="w")
        self.entry_apellido = Entry(self.mi_ventana, textvariable=self.var_apellido)
        self.entry_apellido.grid(row=2, column=1)

        self.concepto = Label(self.mi_ventana, text="Concepto", border=5, width=10)
        self.concepto.grid(row=1, column=2, sticky="w")
        self.entry_concepto = Entry(self.mi_ventana, textvariable=self.var_concepto)
        self.entry_concepto.grid(row=1, column=3)

        self.importe = Label(self.mi_ventana, text="Importe", border=5, width=10)
        self.importe.grid(row=2, column=2, sticky="w")
        self.entry_importe = Entry(self.mi_ventana, textvariable=self.var_importe)
        self.entry_importe.grid(row=2, column=3)

        self.diacarga = Label(self.mi_ventana, text="Fecha carga:", border=5)
        self.diacarga.grid(row=1, column=4, sticky="w")
        self.ddcarga = Label(self.mi_ventana, text="DD", border=5, width=5)
        self.ddcarga.grid(row=1, column=5, sticky="e")
        self.entry_diacarga = Entry(
            self.mi_ventana, textvariable=self.var_diacarga, width=5
        )
        self.entry_diacarga.grid(row=1, column=6)

        self.mescarga = Label(self.mi_ventana, text="MM", border=5, width=5)
        self.mescarga.grid(row=1, column=7, sticky="e")
        self.entry_mescarga = Entry(
            self.mi_ventana, textvariable=self.var_mescarga, width=5
        )
        self.entry_mescarga.grid(row=1, column=8)

        self.aniocarga = Label(self.mi_ventana, text="AA", border=5, width=5)
        self.aniocarga.grid(row=1, column=9, sticky="e")
        self.entry_aniocarga = Entry(
            self.mi_ventana, textvariable=self.var_aniocarga, width=5
        )
        self.entry_aniocarga.grid(row=1, column=10)

        self.diavenc = Label(self.mi_ventana, text="Fecha vencimiento:", border=5)
        self.diavenc.grid(row=2, column=4, sticky="w")
        self.ddvenc = Label(self.mi_ventana, text="DD", border=5, width=5)
        self.ddvenc.grid(row=2, column=5, sticky="e")
        self.entry_diavenc = Entry(
            self.mi_ventana, textvariable=self.var_diavenc, width=5
        )
        self.entry_diavenc.grid(row=2, column=6)

        self.mesvenc = Label(self.mi_ventana, text="MM", border=5, width=5)
        self.mesvenc.grid(row=2, column=7, sticky="e")
        self.entry_mesvenc = Entry(
            self.mi_ventana, textvariable=self.var_mesvenc, width=5
        )
        self.entry_mesvenc.grid(row=2, column=8)

        self.aniovenc = Label(self.mi_ventana, text="AA", border=5, width=5)
        self.aniovenc.grid(row=2, column=9, sticky="e")
        self.entry_aniovenc = Entry(
            self.mi_ventana, textvariable=self.var_aniovenc, width=5
        )
        self.entry_aniovenc.grid(row=2, column=10)

        
        # -----------TREEVIEW------------
        

        self.tree = ttk.Treeview(self.mi_ventana)
        self.tree["columns"] = ("col", "col1", "col2", "col3", "col4", "col5", "col6")
        self.tree.column("#0", width=30, minwidth=50, anchor="w")
        self.tree.column("col", width=100, minwidth=100, anchor="w")
        self.tree.column("col1", width=100, minwidth=100, anchor="w")
        self.tree.column("col2", width=100, minwidth=100, anchor="w")
        self.tree.column("col3", width=100, minwidth=100, anchor="w")
        self.tree.column("col4", width=100, minwidth=100, anchor="w")
        self.tree.column("col5", width=100, minwidth=100, anchor="w")
        self.tree.column("col6", width=100, minwidth=100, anchor="w")

        self.tree.heading("#0", text="ID")
        self.tree.heading("col", text="Nombre")
        self.tree.heading("col1", text="Apellido")
        self.tree.heading("col2", text="Concepto")
        self.tree.heading("col3", text="Precio")
        self.tree.heading("col4", text="Fecha Carga")
        self.tree.heading("col5", text="Fecha Vto")
        self.tree.heading("col6", text="¿Pagado?")

        self.tree.grid(column=0, row=9, columnspan=11)

        def seleccionar_color():
            resultado = askcolor(color="#00ff00", title="Tema")
            self.mi_ventana.configure(background=str(resultado[1]))
            self.nombre.configure(background=str(resultado[1]))
            self.apellido.configure(background=str(resultado[1]))
            self.concepto.configure(background=str(resultado[1]))
            self.importe.configure(background=str(resultado[1]))
            self.diacarga.configure(background=str(resultado[1]))
            self.ddcarga.configure(background=str(resultado[1]))
            self.mescarga.configure(background=str(resultado[1]))
            self.aniocarga.configure(background=str(resultado[1]))
            self.diavenc.configure(background=str(resultado[1]))
            self.ddvenc.configure(background=str(resultado[1]))
            self.mesvenc.configure(background=str(resultado[1]))
            self.aniovenc.configure(background=str(resultado[1]))

         # -----------BOTONERA------------

        self.boton_agregar = Button(
            self.mi_ventana,
            text="Agregar",
            command=lambda: modelo.BaseDeDatos.agregar(
                self.tree,
                self.var_nombre,
                self.var_apellido,
                self.var_concepto,
                self.var_importe,
                self.var_pagado,
                self.var_aniocarga,
                self.var_mescarga,
                self.var_diacarga,
                self.var_aniovenc,
                self.var_mesvenc,
                self.var_diavenc,
                self.deudas_tree,
                self.lista_carga,
            ),
        )
        self.boton_agregar.grid(row=4, column=0, pady=2, padx=0)
        self.boton_agregar.config(width=12)

        self.boton_baja = Button(
            self.mi_ventana, text="Eliminar", command=lambda: modelo.BaseDeDatos.baja(self.tree)
        )
        self.boton_baja.grid(row=4, column=1, pady=2, padx=0)
        self.boton_baja.config(width=12)

        self.boton_actualizar = Button(
            self.mi_ventana,
            text="Actualizar Pago",
            command=lambda: modelo.BaseDeDatos.actualizar(self.tree),
        )
        self.boton_actualizar.grid(row=4, column=2, pady=3, padx=0)
        self.boton_actualizar.config(width=12)

        
        # -----------MENU BAR------------

        self.menubar = Menu(self.mi_ventana)
        self.menu_archivo = Menu(self.menubar, tearoff=0)
        self.menu_archivo.add_command(
            label="Guardar", command=lambda: modelo.BaseDeDatos.alta(self.lista_carga)
        )
        self.menu_archivo.add_command(
            label="Importar", command=lambda: modelo.BaseDeDatos.importar(self.tree)
        )
        self.menu_archivo.add_command(
            label="Crear Tabla Deudores", command=modelo.Ayuda.no_premium
        )
        self.menu_archivo.add_separator()  # separador
        self.menu_archivo.add_command(label="Salir", command=self.mi_ventana.quit)
        self.menubar.add_cascade(label="Opciones", menu=self.menu_archivo)

        self.menu_tema = Menu(self.menubar, tearoff=0)
        self.menu_tema.add_command(label="Cambiar tema", command=seleccionar_color)
        self.menubar.add_cascade(label="Temas", menu=self.menu_tema)

        self.menu_tema = Menu(self.menubar, tearoff=0)
        self.menu_tema.add_command(label="Integrantes", command=modelo.Ayuda.integrantes)
        self.menu_tema.add_command(label="Docente", command=modelo.Ayuda.docente)
        self.menu_tema.add_command(label="Curso", command=modelo.Ayuda.curso)
        self.menubar.add_cascade(label="Ayuda", menu=self.menu_tema)

        self.mi_ventana.config(menu=self.menubar)

