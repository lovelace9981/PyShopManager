import mariadb
import sys
import time
from tkinter import *
from tkinter import ttk
# Para manejo de fechas en formato SQL
from datetime import date, datetime

class Cliente:
    #Constructor
    def __init__(self, conn, window):
        # variable que almacena el objeto del sistema de ventanas de tkinter
        self.w_client = window    
        # copiamos la referencia del conector
        self.client_db_conn = conn
        # cursor propio de consultas
        self.client_cursor = conn.cursor()
        # list de opciones
        self.opciones_l = ['Ver Productos','Comprar un producto','Mis datos','Mis Pedidos','Salir']
        self.opciones_b = ['Ver','Comprar','Mis datos','Mis Pedidos','Salir']
        self.commands = [self.ver_productos,self.comprar_producto,self.mostrar_datos_cliente,self.mostrar_pedidos,self.w_client.destroy]
        # Obtencion de datos desde entradas, necesario.
        self.auth_id_entry = StringVar()
        self.auth_passwd_entry = StringVar()
        # identificador del cliente al autenticar
        self.id_cliente = -1

    # Cleaning widgets on same windows w_client
    def clean_w(self):
        #Limpiando la ventana Para mostrar los datos correctos
        for widget in self.w_client.winfo_children():
            widget.destroy()

    def mostrar_pedidos(self):
        # Limpiamos ventana para mostrarla al cliente
        self.clean_w()

        # Consulta de lectura de los productos
        self.client_cursor.execute("SELECT * FROM PEDIDO WHERE ID_CLIENTE=?", (self.id_cliente,))

        # Obtencion y definicion de los nombres de las columnas de la tabla
        # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-description.html
        # https://mariadb.com/docs/reference/conpy/api/description/
        # Cada fila incluye en formato read en la primera columna el nombre.
        column_headers = []
        size_columns = len(self.client_cursor.description)
        for d in range(size_columns):
            column_headers.append(self.client_cursor.description[d][0])
        
        #Creamos el treeview para visualizar los elementos, con 10 filas de alto
        table_treeview = ttk.Treeview(self.w_client, columns=column_headers, height=10, show='headings', selectmode="none")
        
        # Ajuste de anchura de las columnas
        for d in range(size_columns):
            table_treeview.column(column_headers[d],width=100,minwidth=100)

        # ANCHOR es la ubicacion del texto
        for d in range(size_columns):
            table_treeview.heading(column_headers[d],text=column_headers[d],anchor=CENTER)

        # Obtencion de los datos de la tabla
        row_data = []
        
        for stock in self.client_cursor:
            for j in range(len(stock)):
                row_data.append(stock[j])
            table_treeview.insert('', END, values=row_data)
            row_data.clear()

        #Creamos un scroll, la orientacion indica como queremos el scroll vertical es a la derecha para subir y bajar con yview
        scrollbar = Scrollbar(self.w_client, orient='vertical',command=table_treeview.yview)
        
        #configuramos el treeview para hacer scroll
        table_treeview.configure(yscrollcommand=scrollbar.set)
        
        #Configuracion de visualizacion
        self.w_client.geometry('800x400')
        #Ajuste para que se vean las 3 columnas de producto
        table_treeview.grid(row=0,column=0,padx=30,pady=30,sticky=NSEW)
        scrollbar.grid(row=0,column=1,padx=3,pady=3,sticky=NS)
      
        exit_button = Button(self.w_client, text="Menu Cliente", command=self.main_client)
        exit_button.grid(row=1,column=0,padx=5,pady=5,sticky=NS)

    def ver_productos(self):
        # Limpiamos ventana para mostrarla al cliente
        self.clean_w()

        # Consulta de lectura de los productos
        self.client_cursor.execute("SELECT * FROM STOCK")

        # Obtencion y definicion de los nombres de las columnas de la tabla
        # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-description.html
        # https://mariadb.com/docs/reference/conpy/api/description/
        # Cada fila incluye en formato read en la primera columna el nombre.
        column_headers = []
        size_columns = len(self.client_cursor.description)
        for d in range(size_columns):
            column_headers.append(self.client_cursor.description[d][0])
        
        #Creamos el treeview para visualizar los elementos, con 10 filas de alto
        table_treeview = ttk.Treeview(self.w_client, columns=column_headers, height=10, show='headings', selectmode="none")
        
        # Ajuste de anchura de las columnas
        for d in range(size_columns):
            table_treeview.column(column_headers[d],width=100,minwidth=100)

        # ANCHOR es la ubicacion del texto
        for d in range(size_columns):
            table_treeview.heading(column_headers[d],text=column_headers[d],anchor=CENTER)

        # Obtencion de los datos de la tabla
        row_data = []
        
        for stock in self.client_cursor:
            for j in range(len(stock)):
                row_data.append(stock[j])
            table_treeview.insert('', END, values=row_data)
            row_data.clear()

        #Creamos un scroll, la orientacion indica como queremos el scroll vertical es a la derecha para subir y bajar con yview
        scrollbar = Scrollbar(self.w_client, orient='vertical',command=table_treeview.yview)
        
        #configuramos el treeview para hacer scroll
        table_treeview.configure(yscrollcommand=scrollbar.set)
        
        #Configuracion de visualizacion
        self.w_client.geometry('800x400')
        #Ajuste para que se vean las 3 columnas de producto
        table_treeview.grid(row=0,column=0,padx=30,pady=30,sticky=NSEW)
        scrollbar.grid(row=0,column=1,padx=3,pady=3,sticky=NS)
      
        exit_button = Button(self.w_client, text="Menu Cliente", command=self.main_client)
        exit_button.grid(row=1,column=0,padx=5,pady=5,sticky=NS)

    def mostrar_datos_cliente(self):
        self.w_client.title("Mis datos")
        self.w_client.geometry("650x150")
        self.client_cursor.execute("SELECT ID_CLIENTE, NOMBRE, TELEFONO, DIRECCION, COD_POSTAL FROM CLIENTE WHERE ID_CLIENTE=?",(self.id_cliente,))
        # Limpiamos ventana para poder mostrar los datos
        self.clean_w()
        
        column_headers = []
        size_columns = len(self.client_cursor.description)
        for d in range(size_columns):
            column_headers.append(self.client_cursor.description[d][0])

        #Creamos el treeview para visualizar los elementos
        # height ajusta el numero de filas a visualizar por el treeview
        # More info on: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-Treeview.html
        table_treeview = ttk.Treeview(self.w_client, columns=column_headers, height=1, show='headings', selectmode="none")
        
        # Ajuste de anchura de las columnas
        for d in range(size_columns):
            table_treeview.column(column_headers[d],width=100,minwidth=100)

        # ANCHOR es la ubicacion del texto
        for d in range(size_columns):
            table_treeview.heading(column_headers[d],text=column_headers[d],anchor=CENTER)

        # Obtencion de los datos de la tabla
        row_data = []
        
        for stock in self.client_cursor:
            for j in range(len(stock)):
                row_data.append(stock[j])
            table_treeview.insert('', END, values=row_data)
            row_data.clear()
        
        # Cofiguracion de filas (row) y columnas (colums) de grid
        Grid.rowconfigure(self.w_client, 0, weight = 2)
        Grid.rowconfigure(self.w_client, 1, weight = 2)
        Grid.columnconfigure(self.w_client, 0, weight = 3)

        # Configuramos el grid para treeview
        table_treeview.grid(row=0,column=0,padx=30,pady=30,sticky=NSEW)

        # Creamos un boton de volver al menu
        check_button = Button(self.w_client, text="Volver al Menu Principal", command=self.main_client)
        check_button.grid(row=1,column=0,padx=5,pady=5,sticky=NSEW)  

    
    def ver_productos_compra(self):
        self.client_cursor.execute("SELECT * FROM STOCK")
        
        column_headers = []
        size_columns = len(self.client_cursor.description)
        for d in range(size_columns):
            column_headers.append(self.client_cursor.description[d][0])
        
        # Creamos la ventana hija a la del cliente como auxiliar
        w_aux_compra = Toplevel(self.w_client)
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
        
        for stock in self.client_cursor:
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

    # FALTA La introduccion de la fecha de reparto
    def transaction_product(self, id_producto, cantidad, date):
        #DEBUG ZONE
        print(id_producto)
        print(cantidad)
        print(date)
        try:
            self.client_cursor.execute("SAVEPOINT COMPRA")
            self.client_cursor.execute("INSERT INTO PEDIDO (ID_CLIENTE, ID_PRODUCTO, CANTIDAD, FECHA_PEDIDO, FECHA_ENTREGA_PROGRAMADA, ESTADO) VALUES (?,?,?,NOW(),?,1)",(self.id_cliente, id_producto, cantidad, date))
            self.client_cursor.execute("UPDATE STOCK SET CANTIDAD=CANTIDAD-? WHERE ID_PRODUCTO=?",(cantidad,id_producto))
            self.client_cursor.execute("COMMIT")

            l_buy_error = Label(self.w_client,fg="blue",text="                     Compra Confirmada. Gracias                       ")
            l_buy_error.grid(row=5,column=0,columnspan=2,padx=5,pady=5)
        except self.client_db_conn.Error as error_execution:
            l_buy_error = Label(self.w_client,fg="red",text=format(error_execution))
            l_buy_error.grid(row=5,column=0,columnspan=2,padx=5,pady=5)
            self.client_cursor.execute("ROLLBACK TO COMPRA")

    def comprar_producto(self):
        # GUI Zone - Limpiamos la ventana
        self.clean_w()

        # Redefine window
        self.w_client.geometry('400x200')
        self.w_client.title('Comprar producto')

        #Ajuste de Grid de las columnas y filas
        # Primera fila Label de ID_PRODUCTO y Entry introducion de datos Col 0 y 1 respectivamente
        # Segunda fila Label de cantidad de producto y Entry introducion de datos Col 0 y 1 respectivamente
        # Tercera fila Label de Ventana Aux De consultar Productos y boton de llamada de consultar dichos productos
        # Cuarta fila Label de fecha de pedido y de entrada de la fecha que requiera  FORMATO YYYY-MM-DD
        # Quinta fila Button de confirmacion de pedido y Button de salir al menu de cliente
        # Sexta fila de error de ejecucion o todo correcto
        # Ajuste de filas
        Grid.rowconfigure(self.w_client, 0, weight = 2)
        Grid.rowconfigure(self.w_client, 1, weight = 2)
        Grid.rowconfigure(self.w_client, 2, weight = 2)
        Grid.rowconfigure(self.w_client, 3, weight = 2)
        Grid.rowconfigure(self.w_client, 4, weight = 2)
        Grid.rowconfigure(self.w_client, 5, weight = 2)

        # Ajuste de columnas
        Grid.columnconfigure(self.w_client, 0, weight = 3)
        Grid.columnconfigure(self.w_client, 1, weight = 1)

        # Fila 1
        #Indicamos que queremos un ID_PRODUCTO
        l_id = Label(self.w_client,text="ID Producto Deseado: ")
        l_id.grid(row=0,column=0,padx=5,pady=5,sticky=NSEW)

        val_id_prod = StringVar()

        #Ponemos la caja de introducion de producto
        id_prod_entry = Entry(self.w_client,textvariable=val_id_prod)
        id_prod_entry.grid(row=0,column=1,padx=5,pady=5,sticky=NSEW)

        # Fila 2
        #Indicamos que queremos la cantidad
        l_id = Label(self.w_client,text="Cantidad Deseada: ")
        l_id.grid(row=1,column=0,padx=5,pady=5,sticky=NSEW)

        val_cantidad = StringVar()

        #Ponemos la caja de introducion de cantidad
        id_prod_entry = Entry(self.w_client,textvariable=val_cantidad)
        id_prod_entry.grid(row=1,column=1,padx=5,pady=5,sticky=NSEW)

        # Fila 3
        l_id = Label(self.w_client,text="No recuerda el ID?: ")
        l_id.grid(row=2,column=0,padx=5,pady=5,sticky=NSEW)

        # Boton de consulta de productos - Ventana Auxiliar
        consulta_button = Button(self.w_client, text="Consultar producto", command=self.ver_productos_compra)
        consulta_button.grid(row=2,column=1,padx=5,pady=5,sticky=NSEW)  
        
        # Fila 4 - Introducion de fecha
        l_date = Label(self.w_client,text="Fecha entrega YYYY-MM-DD: ")
        l_date.grid(row=3,column=0,padx=5,pady=5,sticky=NSEW)

        # Ponemos la fecha de ahora por defecto
        now = datetime.now()
        string_fecha = StringVar(value=now.strftime('%Y-%m-%d'))

        #Ponemos la caja de introducion de cantidad
        fecha_entry = Entry(self.w_client,textvariable=string_fecha)
        fecha_entry.grid(row=3,column=1,padx=5,pady=5,sticky=NSEW)

        # Fila 5 - Boton de confirmar compra y salida al menu
        submit_button = Button(self.w_client, text="Confirmar Compra", command=lambda: self.transaction_product(val_id_prod.get(), val_cantidad.get(),string_fecha.get()))
        submit_button.grid(row=4,column=0,padx=5,pady=5,sticky=NSEW) 
        
        check_button = Button(self.w_client, text="Volver al Menu", command=self.main_client)
        check_button.grid(row=4,column=1,padx=5,pady=5,sticky=NSEW)   
        # Fila 6 - Imprimida en transaction_product

    # Funcion de comprobacion de que el cliente es correcto
    def check_client(self):
        # Obtenemos los datos de las entradas de datos de los cuadros de entrada
        id_cliente = self.auth_id_entry.get()
        password = self.auth_passwd_entry.get()
        
        #query necesaria para comprobar el usuario y contrasenia
        self.client_cursor.execute("SELECT ID_CLIENTE,NOMBRE FROM CLIENTE WHERE ID_CLIENTE=? AND PASSWORD=? AND ID_EMPLEADO_BAJA IS NULL", (id_cliente, password))

        result_password = 0
        #Comprobamos si la columna de ID_CLIENTE es devuelta si devuelve 1 es que el cliente y su contrasenia es correcta
        for resultado in self.client_cursor:
            result_password = result_password + 1

        if (result_password == 0):
            l_pass = Label(self.w_client,fg="red",text="Incorrect id or password, please try again!!!")
            l_pass.grid(row=4,column=0,padx=5,pady=5)
        elif (result_password == 1):
            self.id_cliente=id_cliente
            self.main_client()

    def auth_client(self):
        # Toplevel object which will
        # be treated as a new window
        # sets the title of the
        # Toplevel widget
        self.w_client.title("Autenticacion Cliente")
 
        # sets the geometry of toplevel
        self.w_client.geometry('450x150')

        Grid.rowconfigure(self.w_client, 0, weight = 2)
        Grid.rowconfigure(self.w_client, 1, weight = 2)
        Grid.rowconfigure(self.w_client, 2, weight = 2)
        Grid.rowconfigure(self.w_client, 3, weight = 2)
        Grid.rowconfigure(self.w_client, 4, weight = 2)

        Grid.columnconfigure(self.w_client, 0, weight = 3)
        Grid.columnconfigure(self.w_client, 1, weight = 1)
        
        l_title = Label(self.w_client,text="Autentication del Cliente")
        l_title.grid(row=0,column=0,columnspan=2,padx=5,pady=5,sticky=NSEW)

        #while (self.__auth_ok == 0):
        #Indicamos que queremos un ID_CLIENTE
        l_id = Label(self.w_client,text="ID Cliente: ")
        l_id.grid(row=1,column=0,padx=5,pady=5,sticky=NSEW)

        #Ponemos la caja de introducion de usuario
        id_entry = Entry(self.w_client,textvariable=self.auth_id_entry)
        id_entry.grid(row=1,column=1,padx=5,pady=5,sticky=NSEW)

        #Indicamos que queremos la contrasenia
        l_pass = Label(self.w_client,text="Password: ")
        l_pass.grid(row=2,column=0,padx=5,pady=5,sticky=NSEW)

        # Ponemos la caja de introducion de contrasenia con su * 
        # https://stackoverflow.com/questions/2416486/how-to-create-a-password-entry-field-using-tkinter
        pass_entry = Entry(self.w_client, textvariable=self.auth_passwd_entry,show="*") #Obtencion de los datos de la entrada con contrasenia
        pass_entry.grid(row=2,column=1,padx=5,pady=5,sticky=NSEW)

        #Comprobamos que el cliente sea correcto
        check_button = Button(self.w_client, text="Autenticar", command=self.check_client)
        check_button.grid(row=3,column=0,columnspan=2,padx=5,pady=5,sticky=NSEW)  

    def main_client(self):
        self.w_client.geometry('400x200')
        self.w_client.title('Area Clientes')
        
        # Limpiando widgets si los hay
        self.clean_w()
        
        Grid.rowconfigure(self.w_client, 0, weight = 2)
        Grid.rowconfigure(self.w_client, 1, weight = 2)
        Grid.rowconfigure(self.w_client, 2, weight = 2)
        Grid.rowconfigure(self.w_client, 3, weight = 2)
        Grid.rowconfigure(self.w_client, 4, weight = 2)

        Grid.columnconfigure(self.w_client, 0, weight = 3)
        Grid.columnconfigure(self.w_client, 1, weight = 1)

        for i in range(len(self.opciones_l)):
            l = Label(self.w_client,text=self.opciones_l[i])
            l.grid(row=i,column=0,padx=5,pady=5,sticky=NSEW)
            b = Button(self.w_client, text=self.opciones_b[i], command=self.commands[i])
            b.grid(row=i,column=1,padx=5,pady=5,sticky=NSEW)