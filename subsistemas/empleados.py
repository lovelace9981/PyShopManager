import mariadb
import sys
import time
#Generador de contrasenias
import random
import string
from tkinter import *
from tkinter import ttk
# Para manejo de fechas en formato SQL
from datetime import date, datetime


class Empleado:
    def __init__(self, conn, window):
        # variable que almacena el objeto del sistema de ventanas de tkinter
        self.w_empleado = window    
        # copiamos la referencia del conector
        self.empleado_db_conn = conn
        # cursor propio de consultas
        self.empleado_cursor = conn.cursor()
        # list de opciones
        self.opciones_l = ['Alta Cliente','Baja Cliente','Pedir Stock','Ventas','Salir']
        self.opciones_b = ['Alta','Baja','Pedir','Ventas','Salir']
        self.commands = [self.alta_cliente,self.baja_cliente,self.pedir_stock,self.mostrar_ventas,self.w_empleado.destroy]
        # Obtencion de datos desde entradas, necesario.
        self.auth_id_entry = StringVar()
        self.auth_passwd_entry = StringVar()
        # identificador del cliente al autenticar
        self.id_empleado = -1

  # Cleaning widgets on same windows w_empleado
    def clean_w(self):
        #Limpiando la ventana Para mostrar los datos correctos
        for widget in self.w_empleado.winfo_children():
            widget.destroy()
    
    def trans_cod_postal(self, cod_postal, ciudad, w_aux):  
        try:
            self.empleado_cursor.execute("SAVEPOINT NEW_COD_POSTAL")
            self.empleado_cursor.execute("INSERT INTO CIUDADES VALUES (?,?)",(cod_postal,ciudad))
            self.empleado_cursor.execute("COMMIT")

            l_ok_cod = Label(w_aux,fg="blue",text="                     COD_POSTAL confirmado. Gracias                       ")
            l_ok_cod.grid(row=4,column=0,columnspan=2,padx=5,pady=5)
        except self.empleado_db_conn.Error as error_execution:
            l_err_cod = Label(w_aux,fg="red",text=format(error_execution))
            l_err_cod.grid(row=4,column=0,columnspan=2,padx=5,pady=5)
            self.empleado_cursor.execute("ROLLBACK TO NEW_COD_POSTAL")
        
    def cod_postal(self):
        self.empleado_cursor.execute("SELECT * FROM CIUDADES")
        
        column_headers = []
        size_columns = len(self.empleado_cursor.description)
        for d in range(size_columns):
            column_headers.append(self.empleado_cursor.description[d][0])
        
        # Creamos la ventana hija a la del cliente como auxiliar
        w_aux_postal = Toplevel(self.w_empleado)
        w_aux_postal.title('Introducion Cod Postal y Ciudad nueva.')
        
        #Creamos el treeview para visualizar los elementos, con 10 filas de alto
        table_treeview = ttk.Treeview(w_aux_postal, columns=column_headers, show='headings', selectmode="none")
        
        # Ajuste de anchura de las columnas
        for d in range(size_columns):
            table_treeview.column(column_headers[d],width=100,minwidth=100)

        # ANCHOR es la ubicacion del texto
        for d in range(size_columns):
            table_treeview.heading(column_headers[d],text=column_headers[d],anchor=CENTER)

        # Obtencion de los datos de la tabla
        row_data = []
        
        for stock in self.empleado_cursor:
            for j in range(len(stock)):
                row_data.append(stock[j])
            table_treeview.insert('', END, values=row_data)
            row_data.clear()

        #Creamos un scroll, la orientacion indica como queremos el scroll vertical es a la derecha para subir y bajar con yview
        scrollbar = Scrollbar(w_aux_postal, orient='vertical',command=table_treeview.yview)
        
        #configuramos el treeview para hacer scroll
        table_treeview.configure(yscrollcommand=scrollbar.set)
        
        #Configuracion de visualizacion
        w_aux_postal.geometry('800x400')

        #Ajuste de Grid de las columnas y filas
        # Primera fila TreeView y scroll Col 0 y 1 respectivamente
        Grid.rowconfigure(w_aux_postal, 0, weight = 2)
        Grid.rowconfigure(w_aux_postal, 1, weight = 2)
        Grid.rowconfigure(w_aux_postal, 2, weight = 2)
        Grid.rowconfigure(w_aux_postal, 3, weight = 2)
        Grid.rowconfigure(w_aux_postal, 4, weight = 2)


        # Ajuste de columnas
        Grid.columnconfigure(w_aux_postal, 0, weight = 3)
        Grid.columnconfigure(w_aux_postal, 1, weight = 1)

        #Ajuste para que se vean las 10 columnas de producto
        table_treeview.grid(row=0,column=0,padx=30,pady=30,sticky=NSEW)
        scrollbar.grid(row=0,column=1,padx=3,pady=3,sticky=NS)

        # Segunda fila con introducion de nuevo cod postal y ciudad
        l_cod_postal = Label(w_aux_postal,text="Nuevo Cod Postal: ")
        l_cod_postal.grid(row=1,column=0,padx=5,pady=5,sticky=NSEW)

        val_cod_postal = StringVar()

        id_prod_entry = Entry(w_aux_postal,textvariable=val_cod_postal)
        id_prod_entry.grid(row=1,column=1,padx=5,pady=5,sticky=NSEW)

        # Segunda fila con introducion de nuevo cod postal y ciudad
        l_cod_postal = Label(w_aux_postal,text="Nombre Ciudad: ")
        l_cod_postal.grid(row=2,column=0,padx=5,pady=5,sticky=NSEW)

        val_ciudad = StringVar()

        #Ponemos la caja de introducion de nombre de cliente
        id_prod_entry = Entry(w_aux_postal,textvariable=val_ciudad)
        id_prod_entry.grid(row=2,column=1,padx=5,pady=5,sticky=NSEW)

        # Tercera fila de introducion de Nuevo cod postal o de salir
        submit_cod_postal = Button(w_aux_postal, text="Submit CodPostal", command=lambda: self.trans_cod_postal(val_cod_postal.get(), val_ciudad.get(),w_aux_postal))
        submit_cod_postal.grid(row=3,column=0,padx=5,pady=5,sticky=NSEW)

        exit_button = Button(w_aux_postal, text="Salir", command=w_aux_postal.destroy)
        exit_button.grid(row=3,column=1,padx=5,pady=5,sticky=NS)

    def get_random_password(self):
        letters_type = string.ascii_lowercase
        result_passwd = ''.join(random.choice(letters_type) for i in range(10))

        return result_passwd

    def transaction_alta_cliente(self,nombre_cliente,telefono,direccion,cod_postal):
        # Generador de contrasenias
        password = self.get_random_password()

        try:
            self.empleado_cursor.execute("SAVEPOINT NEW_CLIENTE")
            self.empleado_cursor.execute("INSERT INTO CLIENTE (NOMBRE,TELEFONO,DIRECCION,COD_POSTAL,PASSWORD,ID_EMPLEADO_ALTA) VALUES (?,?,?,?,?,?)", (nombre_cliente,telefono,direccion,cod_postal,password,self.id_empleado))
            self.empleado_cursor.execute("COMMIT")
            self.empleado_cursor.execute("SELECT ID_CLIENTE, PASSWORD FROM CLIENTE WHERE TELEFONO=? AND PASSWORD=?",(telefono,password))
            
            for data in self.empleado_cursor:
                for i in range(len(data)):
                    if i == 0:
                        datos = "ID: " + str(data[i]) + " "
                    elif i==1:
                        datos = datos + "Passwd: " + str(data[i]) + " Gracias por registrarse."                    
            
            l_alta_ok = Label(self.w_empleado,fg="blue",text=datos)
            l_alta_ok.grid(row=6,column=0,columnspan=2,padx=5,pady=5)
        except self.empleado_db_conn.Error as error_execution:
            l_alta_error = Label(self.w_empleado,fg="red",text=format(error_execution))
            l_alta_error.grid(row=6,column=0,columnspan=2,padx=5,pady=5)
            self.empleado_cursor.execute("ROLLBACK TO NEW_CLIENTE")

    def alta_cliente(self):
        # GUI Zone - Limpiamos la ventana
        self.clean_w()

        # Redefine window
        self.w_empleado.geometry('400x200')
        self.w_empleado.title('Alta Cliente')

        #Ajuste de Grid de las columnas y filas
        # Primera fila Label de NOMBRE y Entry introducion de datos Col 0 y 1 respectivamente
        # Segunda Fila Label de TELEFONO y Entry
        # Tercera Fila de introduccion de Direccion del cliente y su entry
        # Cuarta Fila de introducion del COD_POSTAL y su Entry.
        # Quinta Fila de comprobacion de COD_POSTAL existente.
        # Sexta fila Button de confirmacion de transaccion y Button de salir al menu de cliente
        # Septima fila de error de ejecucion o todo correcto
        # Ajuste de filas
        Grid.rowconfigure(self.w_empleado, 0, weight = 2)
        Grid.rowconfigure(self.w_empleado, 1, weight = 2)
        Grid.rowconfigure(self.w_empleado, 2, weight = 2)
        Grid.rowconfigure(self.w_empleado, 3, weight = 2)
        Grid.rowconfigure(self.w_empleado, 4, weight = 2)
        Grid.rowconfigure(self.w_empleado, 5, weight = 2)
        Grid.rowconfigure(self.w_empleado, 6, weight = 2)

        # Ajuste de columnas
        Grid.columnconfigure(self.w_empleado, 0, weight = 3)
        Grid.columnconfigure(self.w_empleado, 1, weight = 1)

        # Fila 1 - Nombre
        l_id = Label(self.w_empleado,text="Nombre Cliente: ")
        l_id.grid(row=0,column=0,padx=5,pady=5,sticky=NSEW)

        val_nombre_cliente = StringVar()

        id_prod_entry = Entry(self.w_empleado,textvariable=val_nombre_cliente)
        id_prod_entry.grid(row=0,column=1,padx=5,pady=5,sticky=NSEW)

        # Fila 2 - Telefono
        l_id = Label(self.w_empleado,text="Telefono Cliente: ")
        l_id.grid(row=1,column=0,padx=5,pady=5,sticky=NSEW)

        val_telefono = StringVar()

        entry_telefono = Entry(self.w_empleado,textvariable=val_telefono)
        entry_telefono.grid(row=1,column=1,padx=5,pady=5,sticky=NSEW)

        # Fila 3 - Direccion
        l_id = Label(self.w_empleado,text="Direccion Cliente: ")
        l_id.grid(row=2,column=0,padx=5,pady=5,sticky=NSEW)

        val_direccion = StringVar()

        entry_direccion = Entry(self.w_empleado,textvariable=val_direccion)
        entry_direccion.grid(row=2,column=1,padx=5,pady=5,sticky=NSEW)

        # Fila 4 - Cod postal
        l_id = Label(self.w_empleado,text="Cod Postal Cliente: ")
        l_id.grid(row=3,column=0,padx=5,pady=5,sticky=NSEW)

        val_cod_postal = StringVar()

        entry_cod_postal = Entry(self.w_empleado,textvariable=val_cod_postal)
        entry_cod_postal.grid(row=3,column=1,padx=5,pady=5,sticky=NSEW)

        # Fila - 5 Boton de consulta de Cod_Postal y introducir si no existe
        consulta_button = Button(self.w_empleado, text="Consultar COD_POSTAL", command=self.cod_postal)
        consulta_button.grid(row=4,column=1, columnspan=2, padx=5,pady=5,sticky=NSEW)  

        # Fila 6 - Boton de confirmar Cliente y salida al menu
        submit_button = Button(self.w_empleado, text="Confirmar Cliente", command=lambda: self.transaction_alta_cliente(val_nombre_cliente.get(), val_telefono.get(), val_direccion.get(),val_cod_postal.get()))
        submit_button.grid(row=5,column=0,padx=5,pady=5,sticky=NSEW) 
        
        check_button = Button(self.w_empleado, text="Volver al Menu", command=self.main_empleado)
        check_button.grid(row=5,column=1,padx=5,pady=5,sticky=NSEW)   
        # Fila 7 - Imprimida en transaction_cliente

    def mostrar_ventas(self):
        # Limpiamos ventana para mostrarla al cliente
        self.clean_w()

        # Consulta de lectura de las ventas a traves del VIEW creado
        self.empleado_cursor.execute("SELECT * FROM VENTAS")
        self.w_empleado.title("Ventas")

        # Obtencion y definicion de los nombres de las columnas de la tabla
        # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-description.html
        # https://mariadb.com/docs/reference/conpy/api/description/
        # Cada fila incluye en formato read en la primera columna el nombre.
        column_headers = []
        size_columns = len(self.empleado_cursor.description)
        for d in range(size_columns):
            column_headers.append(self.empleado_cursor.description[d][0])
        
        #Creamos el treeview para visualizar los elementos, con 10 filas de alto
        table_treeview = ttk.Treeview(self.w_empleado, columns=column_headers, height=10, show='headings', selectmode="none")
        
        # Ajuste de anchura de las columnas
        for d in range(size_columns):
            table_treeview.column(column_headers[d],width=100,minwidth=100)

        # ANCHOR es la ubicacion del texto
        for d in range(size_columns):
            table_treeview.heading(column_headers[d],text=column_headers[d],anchor=CENTER)

        # Obtencion de los datos de la tabla
        row_data = []
        
        for stock in self.empleado_cursor:
            for j in range(len(stock)):
                row_data.append(stock[j])
            table_treeview.insert('', END, values=row_data)
            row_data.clear()

        #Creamos un scroll, la orientacion indica como queremos el scroll vertical es a la derecha para subir y bajar con yview
        scrollbar = Scrollbar(self.w_empleado, orient='vertical',command=table_treeview.yview)
        
        #configuramos el treeview para hacer scroll
        table_treeview.configure(yscrollcommand=scrollbar.set)
        
        #Configuracion de visualizacion
        self.w_empleado.geometry('800x400')
        #Ajuste para que se vean las 3 columnas de producto
        table_treeview.grid(row=0,column=0,padx=30,pady=30,sticky=NSEW)
        scrollbar.grid(row=0,column=1,padx=3,pady=3,sticky=NS)
      
        exit_button = Button(self.w_empleado, text="Menu Empleado", command=self.main_empleado)
        exit_button.grid(row=1,column=0,padx=5,pady=5,sticky=NS)

    def transaction_baja_cliente(self,id_cliente,telefono):
        try:
            self.empleado_cursor.execute("SAVEPOINT BAJA_CLIENTE")
            self.empleado_cursor.execute("UPDATE CLIENTE SET ID_EMPLEADO_BAJA=? WHERE ID_CLIENTE=? AND TELEFONO=?", (self.id_empleado,id_cliente,telefono))
            columnas_afectadas = format(self.empleado_cursor.rowcount)
            self.empleado_cursor.execute("COMMIT")
            
            l_baja_ok = Label(self.w_empleado,fg="blue",text="          BAJA REALIZADA si 1 - si es 0 el dato no es correcto. \n " + "Ha afectado a " + columnas_afectadas)
            l_baja_ok.grid(row=3,column=0,columnspan=2,padx=5,pady=5)
        except self.empleado_db_conn.Error as error_execution:
            l_baja_error = Label(self.w_empleado,fg="red",text=format(error_execution))
            l_baja_error.grid(row=3,column=0,columnspan=2,padx=5,pady=5)
            self.empleado_cursor.execute("ROLLBACK TO BAJA_CLIENTE")

    def baja_cliente(self):
        # GUI Zone - Limpiamos la ventana
        self.clean_w()

        # Redefine window
        self.w_empleado.geometry('400x200')
        self.w_empleado.title('Baja Cliente')

        #Ajuste de Grid de las columnas y filas
        # Primera fila Label de ID_CLIENTE y Entry introducion de datos Col 0 y 1 respectivamente
        # Segunda fila Label de TELEFONO de cliente y Entry introducion de datos Col 0 y 1 respectivamente
        # Tercera fila Boton de Input y boton de salir al menu
        # Cuarta fila Informacion del estado de la BD y su transaccion
        # Ajuste de filas
        Grid.rowconfigure(self.w_empleado, 0, weight = 2)
        Grid.rowconfigure(self.w_empleado, 1, weight = 2)
        Grid.rowconfigure(self.w_empleado, 2, weight = 2)
        Grid.rowconfigure(self.w_empleado, 3, weight = 2)

        # Ajuste de columnas
        Grid.columnconfigure(self.w_empleado, 0, weight = 3)
        Grid.columnconfigure(self.w_empleado, 1, weight = 1)

        # Fila 1
        # Indicamos que queremos un ID_CLIENTE
        l_id = Label(self.w_empleado,text="ID Cliente baja: ")
        l_id.grid(row=0,column=0,padx=5,pady=5,sticky=NSEW)

        val_id_cliente = StringVar()

        #Ponemos la caja de introducion de producto
        id_id_entry = Entry(self.w_empleado,textvariable=val_id_cliente)
        id_id_entry.grid(row=0,column=1,padx=5,pady=5,sticky=NSEW)

        # Fila 2
        # Indicamos que queremos un TELEFONO
        l_tel = Label(self.w_empleado,text="Telefono Cliente: ")
        l_tel.grid(row=1,column=0,padx=5,pady=5,sticky=NSEW)

        val_telefono = StringVar()

        id_tel_entry = Entry(self.w_empleado,textvariable=val_telefono)
        id_tel_entry.grid(row=1,column=1,padx=5,pady=5,sticky=NSEW)

        # Fila 3 - boton de submit y de salida
        # Indicamos que queremos un TELEFONO
        submit_button = Button(self.w_empleado, text="Confirmar Baja", command=lambda: self.transaction_baja_cliente(val_id_cliente.get(), val_telefono.get()))
        submit_button.grid(row=2,column=0,padx=5,pady=5,sticky=NSEW) 
        
        check_button = Button(self.w_empleado, text="Volver al Menu", command=self.main_empleado)
        check_button.grid(row=2,column=1,padx=5,pady=5,sticky=NSEW)   

        # Fila 4 - Mensajes de error o confirmacion

    def ver_stock(self):
        self.empleado_cursor.execute("SELECT * FROM STOCK")
        
        column_headers = []
        size_columns = len(self.empleado_cursor.description)
        for d in range(size_columns):
            column_headers.append(self.empleado_cursor.description[d][0])
        
        # Creamos la ventana hija a la del cliente como auxiliar
        w_aux_compra = Toplevel(self.w_empleado)
        w_aux_compra.title('Area Clientes')
        
        #Creamos el treeview para visualizar los elementos, con 10 filas de alto
        table_treeview = ttk.Treeview(w_aux_compra, columns=column_headers, show='headings', selectmode="none")
        
        # Ajuste de anchura de las columnas
        for d in range(size_columns):
            table_treeview.column(column_headers[d],width=100,minwidth=100)

        # ANCHOR es la ubicacion del texto
        for d in range(size_columns):
            table_treeview.heading(column_headers[d],text=column_headers[d],anchor=CENTER)

        # Obtencion de los datos de la tabla
        row_data = []
        
        for stock in self.empleado_cursor:
            for j in range(len(stock)):
                row_data.append(stock[j])
            table_treeview.insert('', END, values=row_data)
            row_data.clear()

        #Creamos un scroll, la orientacion indica como queremos el scroll vertical es a la derecha para subir y bajar con yview
        scrollbar = Scrollbar(w_aux_compra, orient='vertical',command=table_treeview.yview)
        
        #configuramos el treeview para hacer scroll
        table_treeview.configure(yscrollcommand=scrollbar.set)
        
        #Configuracion de visualizacion
        w_aux_compra.geometry('800x400')

        #Ajuste de Grid de las columnas y filas
        # Primera fila TreeView y scroll Col 0 y 1 respectivamente
        Grid.rowconfigure(w_aux_compra, 0, weight = 2)

        # Ajuste de columnas
        Grid.columnconfigure(w_aux_compra, 0, weight = 3)
        Grid.columnconfigure(w_aux_compra, 1, weight = 1)

        #Ajuste para que se vean las 10 columnas de producto
        table_treeview.grid(row=0,column=0,padx=30,pady=30,sticky=NSEW)
        scrollbar.grid(row=0,column=1,padx=3,pady=3,sticky=NS)
      
        exit_button = Button(w_aux_compra, text="Salir", command=w_aux_compra.destroy)
        exit_button.grid(row=1,column=0,padx=5,pady=5,sticky=NS)

    def transaction_stock(self, id_producto, cantidad):
        # Si introducimos un producto que no exista, simplemente no afectara a ninguna fila.
        # Obtenemos el dato de afectado o no a traves de rowcount
        try:
            self.empleado_cursor.execute("SAVEPOINT REPONER_STOCK")
            self.empleado_cursor.execute("UPDATE STOCK SET CANTIDAD=CANTIDAD+? WHERE ID_PRODUCTO=?",(cantidad,id_producto))
            columnas_afectadas = format(self.empleado_cursor.rowcount)
            self.empleado_cursor.execute("COMMIT")

            l_buy_error = Label(self.w_empleado,fg="blue",text="Ha afectado a " + columnas_afectadas)
            l_buy_error.grid(row=5,column=0,columnspan=2,padx=5,pady=5)
        except self.empleado_db_conn.Error as error_execution:
            l_buy_error = Label(self.w_empleado,fg="red",text=format(error_execution))
            l_buy_error.grid(row=5,column=0,columnspan=2,padx=5,pady=5)
            self.empleado_cursor.execute("ROLLBACK TO REPONER_STOCK")

    def pedir_stock(self):
        # GUI Zone - Limpiamos la ventana
        self.clean_w()

        # Redefine window
        self.w_empleado.geometry('400x200')
        self.w_empleado.title('Pedir stock')

        #Ajuste de Grid de las columnas y filas
        # Primera fila Label de ID_PRODUCTO y Entry introducion de datos Col 0 y 1 respectivamente
        # Segunda fila Label de cantidad de producto y Entry introducion de datos Col 0 y 1 respectivamente
        # Tercera fila Label de Ventana Aux De consultar Productos y boton de llamada de consultar dichos productos
        # Cuarta fila Label de fecha de pedido y de entrada de la fecha que requiera  FORMATO YYYY-MM-DD
        # Quinta fila Button de confirmacion de pedido y Button de salir al menu de cliente
        # Sexta fila de error de ejecucion o todo correcto
        # Ajuste de filas
        Grid.rowconfigure(self.w_empleado, 0, weight = 2)
        Grid.rowconfigure(self.w_empleado, 1, weight = 2)
        Grid.rowconfigure(self.w_empleado, 2, weight = 2)
        Grid.rowconfigure(self.w_empleado, 3, weight = 2)
        Grid.rowconfigure(self.w_empleado, 4, weight = 2)
        Grid.rowconfigure(self.w_empleado, 5, weight = 2)

        # Ajuste de columnas
        Grid.columnconfigure(self.w_empleado, 0, weight = 3)
        Grid.columnconfigure(self.w_empleado, 1, weight = 1)

        # Fila 1
        #Indicamos que queremos un ID_PRODUCTO
        l_id = Label(self.w_empleado,text="ID Producto reponer: ")
        l_id.grid(row=0,column=0,padx=5,pady=5,sticky=NSEW)

        val_id_prod = StringVar()

        #Ponemos la caja de introducion de producto
        id_prod_entry = Entry(self.w_empleado,textvariable=val_id_prod)
        id_prod_entry.grid(row=0,column=1,padx=5,pady=5,sticky=NSEW)

        # Fila 2
        #Indicamos que queremos la cantidad
        l_id = Label(self.w_empleado,text="Cantidad Deseada: ")
        l_id.grid(row=1,column=0,padx=5,pady=5,sticky=NSEW)

        val_cantidad = StringVar()

        #Ponemos la caja de introducion de cantidad
        id_prod_entry = Entry(self.w_empleado,textvariable=val_cantidad)
        id_prod_entry.grid(row=1,column=1,padx=5,pady=5,sticky=NSEW)

        # Fila 3
        l_id = Label(self.w_empleado,text="No recuerda el ID?: ")
        l_id.grid(row=2,column=0,padx=5,pady=5,sticky=NSEW)

        # Boton de consulta de productos - Ventana Auxiliar
        consulta_button = Button(self.w_empleado, text="Consultar producto", command=self.ver_stock)
        consulta_button.grid(row=2,column=1,padx=5,pady=5,sticky=NSEW)  

        # Fila 4 - Boton de confirmar compra y salida al menu
        submit_button = Button(self.w_empleado, text="Confirmar Stock", command=lambda: self.transaction_stock(val_id_prod.get(), val_cantidad.get()))
        submit_button.grid(row=4,column=0,padx=5,pady=5,sticky=NSEW) 
        
        check_button = Button(self.w_empleado, text="Volver al Menu", command=self.main_empleado)
        check_button.grid(row=4,column=1,padx=5,pady=5,sticky=NSEW)   
        # Fila 5 - Imprimida en transaction_product

    def mostrar_ventas(self):
        # Limpiamos ventana para mostrarla al cliente
        self.clean_w()

        # Consulta de lectura de las ventas a traves del VIEW creado
        self.empleado_cursor.execute("SELECT * FROM VENTAS")
        self.w_empleado.title("Ventas")

        # Obtencion y definicion de los nombres de las columnas de la tabla
        # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-description.html
        # https://mariadb.com/docs/reference/conpy/api/description/
        # Cada fila incluye en formato read en la primera columna el nombre.
        column_headers = []
        size_columns = len(self.empleado_cursor.description)
        for d in range(size_columns):
            column_headers.append(self.empleado_cursor.description[d][0])
        
        #Creamos el treeview para visualizar los elementos, con 10 filas de alto
        table_treeview = ttk.Treeview(self.w_empleado, columns=column_headers, height=10, show='headings', selectmode="none")
        
        # Ajuste de anchura de las columnas
        for d in range(size_columns):
            table_treeview.column(column_headers[d],width=100,minwidth=100)

        # ANCHOR es la ubicacion del texto
        for d in range(size_columns):
            table_treeview.heading(column_headers[d],text=column_headers[d],anchor=CENTER)

        # Obtencion de los datos de la tabla
        row_data = []
        
        for stock in self.empleado_cursor:
            for j in range(len(stock)):
                row_data.append(stock[j])
            table_treeview.insert('', END, values=row_data)
            row_data.clear()

        #Creamos un scroll, la orientacion indica como queremos el scroll vertical es a la derecha para subir y bajar con yview
        scrollbar = Scrollbar(self.w_empleado, orient='vertical',command=table_treeview.yview)
        
        #configuramos el treeview para hacer scroll
        table_treeview.configure(yscrollcommand=scrollbar.set)
        
        #Configuracion de visualizacion
        self.w_empleado.geometry('800x400')
        #Ajuste para que se vean las 3 columnas de producto
        table_treeview.grid(row=0,column=0,padx=30,pady=30,sticky=NSEW)
        scrollbar.grid(row=0,column=1,padx=3,pady=3,sticky=NS)
      
        exit_button = Button(self.w_empleado, text="Menu Empleado", command=self.main_empleado)
        exit_button.grid(row=1,column=0,padx=5,pady=5,sticky=NS)

    # Funcion de comprobacion de que el empleado es correcto
    def check_empleado(self):
        # Obtenemos los datos de las entradas de datos de los cuadros de entrada
        id_empleado = self.auth_id_entry.get()
        password = self.auth_passwd_entry.get()
        
        #query necesaria para comprobar el usuario y contrasenia
        # Hacerlo con trigger?
        self.empleado_cursor.execute("SELECT ID_EMPLEADO,NOMBRE FROM EMPLEADO WHERE ID_EMPLEADO=? AND PASSWORD=?", (id_empleado, password))

        result_password = 0
        #Comprobamos si la columna de ID_CLIENTE es devuelta si devuelve 1 es que el cliente y su contrasenia es correcta
        for resultado in self.empleado_cursor:
            result_password = result_password + 1

        if (result_password == 0):
            l_pass = Label(self.w_empleado,fg="red",text="Incorrect id or password, please try again!!!")
            l_pass.grid(row=4,column=0,padx=5,pady=5)
        elif (result_password == 1):
            self.id_empleado=id_empleado
            self.main_empleado()

    def auth_employee(self):
        # Toplevel object which will
        # be treated as a new window
        # sets the title of the
        # Toplevel widget
        self.w_empleado.title("Autenticacion Empleado")
 
        # sets the geometry of toplevel
        self.w_empleado.geometry('450x150')

        Grid.rowconfigure(self.w_empleado, 0, weight = 2)
        Grid.rowconfigure(self.w_empleado, 1, weight = 2)
        Grid.rowconfigure(self.w_empleado, 2, weight = 2)
        Grid.rowconfigure(self.w_empleado, 3, weight = 2)
        Grid.rowconfigure(self.w_empleado, 4, weight = 2)

        Grid.columnconfigure(self.w_empleado, 0, weight = 3)
        Grid.columnconfigure(self.w_empleado, 1, weight = 1)
        
        l_title = Label(self.w_empleado,text="Autentication del Empleado")
        l_title.grid(row=0,column=0,columnspan=2,padx=5,pady=5,sticky=NSEW)

        #while (self.__auth_ok == 0):
        #Indicamos que queremos un ID_CLIENTE
        l_id = Label(self.w_empleado,text="ID Empleado: ")
        l_id.grid(row=1,column=0,padx=5,pady=5,sticky=NSEW)

        #Ponemos la caja de introducion de usuario
        id_entry = Entry(self.w_empleado,textvariable=self.auth_id_entry)
        id_entry.grid(row=1,column=1,padx=5,pady=5,sticky=NSEW)

        #Indicamos que queremos la contrasenia
        l_pass = Label(self.w_empleado,text="Password: ")
        l_pass.grid(row=2,column=0,padx=5,pady=5,sticky=NSEW)

        # Ponemos la caja de introducion de contrasenia con su * 
        # https://stackoverflow.com/questions/2416486/how-to-create-a-password-entry-field-using-tkinter
        pass_entry = Entry(self.w_empleado, textvariable=self.auth_passwd_entry,show="*") #Obtencion de los datos de la entrada con contrasenia
        pass_entry.grid(row=2,column=1,padx=5,pady=5,sticky=NSEW)

        #Comprobamos que el cliente sea correcto
        check_button = Button(self.w_empleado, text="Autenticar", command=self.check_empleado)
        check_button.grid(row=3,column=0,columnspan=2,padx=5,pady=5,sticky=NSEW)  

    def main_empleado(self):
        self.w_empleado.geometry('400x200')
        self.w_empleado.title('Area Empleados')
        
        # Limpiando widgets si los hay
        self.clean_w()
        
        Grid.rowconfigure(self.w_empleado, 0, weight = 2)
        Grid.rowconfigure(self.w_empleado, 1, weight = 2)
        Grid.rowconfigure(self.w_empleado, 2, weight = 2)
        Grid.rowconfigure(self.w_empleado, 3, weight = 2)
        Grid.rowconfigure(self.w_empleado, 4, weight = 2)

        Grid.columnconfigure(self.w_empleado, 0, weight = 3)
        Grid.columnconfigure(self.w_empleado, 1, weight = 1)

        for i in range(len(self.opciones_l)):
            l = Label(self.w_empleado,text=self.opciones_l[i])
            l.grid(row=i,column=0,padx=5,pady=5,sticky=NSEW)
            b = Button(self.w_empleado, text=self.opciones_b[i], command=self.commands[i])
            b.grid(row=i,column=1,padx=5,pady=5,sticky=NSEW)