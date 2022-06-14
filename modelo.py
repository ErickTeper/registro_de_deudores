import sqlite3
import re
from tkinter.messagebox import askyesno 
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror


class BaseDeDatos:

        def actualizar_id():
            """ Función que lee el índice de la última fila de la base de datos"""

            try: 
                conn = sqlite3.connect("basedeudas.db")
                cur = conn.cursor()
                cur.execute("SELECT id FROM deudas")
                filas = cur.fetchall()

                ultima_fila = None
                ultima_fila = filas[-1]

                conn.close()
                
                mi_id = 0 if ultima_fila is None else ultima_fila[0]
                return mi_id

            except: 
                mi_id = 0 
                print("Parece haber habido un error con la base de datos, por favor verifica que esta misma exista en el directorio")
                return mi_id 

        def crear_base():
            """ Crea la base de datos en caso de no existir """

            con = sqlite3.connect("basedeudas.db")

            return con

        def crear_tabla(con):
            """ Crea la tabla en caso de que no exista """

            cursor = con.cursor()
            sql = "CREATE TABLE IF NOT EXISTS deudas (id integer PRIMARY KEY AUTOINCREMENT,\
                    nombre varchar(20) NOT NULL, apellido varchar(30) NOT NULL,\
                    concepto varchar(20) NOT NULL, importe real NOT NULL, \
                    fcarga text, fvenc text, pagado BOOLEAN)"

            cursor.execute(sql)
            con.commit()

        def insertar(con, mi_id, nombre, apellido, concepto, importe, fcarga, fvenc, pagado):
            """ Inserta los campos en la base de datos """

            cursor = con.cursor()
            importe = float(importe)
            data = (mi_id, nombre, apellido, concepto, importe, fcarga, fvenc, pagado)
            sql = "INSERT INTO deudas(id, nombre, apellido, concepto, importe, fcarga, fvenc, pagado)\
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?);"
            cursor.execute(sql, data)
            con.commit()
            print("Estoy en alta todo ok")
            print(mi_id, nombre + apellido + concepto + "importe" + fcarga + fvenc, pagado)


        def alta(lista_carga):
            """ Da de alta los campos en la base de datos """
            global mi_id
            for carga in lista_carga:
                miid = carga[0]
                nombre = carga[1]
                apellido = carga[2]
                concepto = carga[3]
                importe = carga[4]
                fcarga = carga[5]
                fvenc = carga[6]
                pagado = carga[7]
                print(miid, nombre + apellido + concepto + importe + fcarga + fvenc, pagado)
                BaseDeDatos.insertar(con, miid, nombre, apellido, concepto, float(importe), fcarga, fvenc, False)
                mi_id += 1


        def importar(tree):
            """ Importa la base de datos al treeview """

            tree.delete(*tree.get_children())
            con = sqlite3.connect("basedeudas.db")
            cursor = con.cursor()
            cursor.execute("SELECT * FROM deudas")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
                tree.insert(
                    "",
                    "end",
                    text=str(row[0]),
                    values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7]),
                )
            con.close()


        def baja(tree):
            """ Da de baja el campo en treeview """

            item = tree.focus()
            dicc = tree.item(item)
            print(dicc)
            borrar_id = dicc["text"]
            print(borrar_id)
            if askyesno("Eliminación", "¿Confirma la eliminación de este registro?"):
                showinfo("Si", "El registro fue eliminado")
                tree.delete(item)
                BaseDeDatos.borrar(con, borrar_id)
            else:
                showinfo("No", "El registro no fue eliminado")


        def borrar(con, borrar_id):
            """ Elimina el campo en base de datos""" 
            cursor = con.cursor()
            borrar_id = int(borrar_id)
            data = (borrar_id,)  # para que se entienda q es una tupla
            sql = "DELETE FROM deudas where id = ?;"
            cursor.execute(sql, data)  # ahora ejecuta tambien la data que se le esta pasando
            con.commit()


        def modificar(con, actualiza_id):
            """ Actualiza los campos en base de datos """ 

            cursor = con.cursor()
            actualiza_id = int(actualiza_id)
            data = (actualiza_id,)  # para que se entienda q es una tupla
            sql = "UPDATE deudas SET pagado = TRUE where id = ?;"
            cursor.execute(sql, data)  # ahora ejecuta tambien la data que se le esta pasando
            con.commit()


        def actualizar(tree):
            """ Actualiza los campos en base de datos """

            item = tree.focus()
            dicc = tree.item(item)
            print(dicc)
            actualiza_id = dicc["text"]
            print(actualiza_id)
            BaseDeDatos.modificar(con, actualiza_id)
            tree.delete(*tree.get_children())
            BaseDeDatos.importar(tree)

        def agregar(tree, var_nombre, var_apellido, var_concepto,
                    var_importe, var_pagado, var_aniocarga,
                    var_mescarga, var_diacarga, var_aniovenc, var_mesvenc,
                    var_diavenc, deudas_tree, lista_carga):
            """ Valida ciertos campos con regex """

            cadena = var_nombre.get()
            patron = "[a-zA-Z\s]+(-[^\W\d_]+)?$"

            if re.match(patron, cadena):

                global mi_id
                mi_id += 1

                dia_carga = (
                    var_aniocarga.get() + "-" + var_mescarga.get() + "-" + var_diacarga.get()
                )
                vencimiento = (
                    var_aniovenc.get() + "-" + var_mesvenc.get() + "-" + var_diavenc.get()
                )

                deuda = tree.insert(
                    "",
                    "end",
                    text=str(mi_id),
                    values=(
                        var_nombre.get(),
                        var_apellido.get(),
                        var_concepto.get(),
                        var_importe.get(),
                        str(dia_carga),
                        str(vencimiento),
                        var_pagado.get(),
                    ),
                )
                deudas_tree.append(deuda)
                lista_carga.append(
                    [
                        mi_id,
                        var_nombre.get(),
                        var_apellido.get(),
                        var_concepto.get(),
                        var_importe.get(),
                        str(dia_carga),
                        str(vencimiento),
                        var_pagado.get(),
                    ]
                )
                print(lista_carga)

            else:

                showerror(
                    "Error: Problema de validación de nombre",
                    "Ha habido un problema con la validación del nombre ingresado. Por favor ingrese un nombre correcto sin incluir números ni carácteres especiales.",
                )


class Ayuda:
    """ Ofrece ayuda adicional sobre el Trabajo Práctico para la Entrega Intermedia """

    def integrantes():
        showinfo(
            "Integrantes del Grupo",
            "Los alumnos integrantes de este grupo son: Ana Inés Kessler, Gustavo keimel, Alex Menéndez, Benjamin Iriarte Crom, Erick Teper",
        )


    def docente():
        showinfo("Docente del Curso", "Docente: Ing.  Juan Marcelo Barreto Rodriguez")


    def curso():
        showinfo("Curso", "Diplomatura en Python, Nivel Intermedio, Año: 2022")


    def no_premium():
        showerror(
            "Opcion no válida en version free",
            "Para crear más de una tabla solicite la version Premium en nuestro sitio web",
        )

con = BaseDeDatos.crear_base()
BaseDeDatos.crear_tabla(con)
mi_id = BaseDeDatos.actualizar_id()

    