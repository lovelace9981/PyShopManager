import mariadb
import sys
import time
from tkinter import *
from tkinter import ttk
from datetime import date,datetime

class Repartidor:
    # CONSTRUCTOR
    def __init__(self, conn, window):
        # Variable para almacenar el objeto del sistema de ventanas de tkinter
        self.w_deliveryman = window
        # Cursor de la conexion a la base de datos
        self.deliveryman_cursor = conn.cursor()
        # Copia de la conexion a la BD
        self.deliveryman_conn = conn
        # Declaracion de opciones
        self.opciones = ['Ver pedidos pendientes de envio', 'Seleccionar pedido para repartir', 'Modificar datos de envio', 'Confirmar envio', 'Cancelar envio','Salir']
        self.opciones_b = ['Ver pedidos', 'Seleccionar', 'Modificar datos', 'Confirmar', 'Cancelar','Salir']
        self.comandos = [self.ver_pedidos, self.seleccionar_pedido, self.modificar_datos, self.confirmar_pedido, self.cancelar_pedido, self.w_deliveryman.destroy]       
        # Obtencion de credenciales del repartidor
        self.auth_id_repartidor = StringVar()
        self.passwd_repartidor = StringVar()
        # ID del repartidor al autenticar
        self.id_repartidor = -1

    # AUTENTICACION DEL REPARTIDOR
    def auth_deliveryman(self):
        # Definimos el titulo de la ventana
        self.w_deliveryman.title("Autenticacion Repartidor")

        # Definimos la geometria de la ventana
        self.w_deliveryman.geometry('450x150')

        Grid.rowconfigure(self.w_deliveryman, 0, weight = 2)
        Grid.rowconfigure(self.w_deliveryman, 1, weight = 2)
        Grid.rowconfigure(self.w_deliveryman, 2, weight = 2)
        Grid.rowconfigure(self.w_deliveryman, 3, weight = 2)
        Grid.rowconfigure(self.w_deliveryman, 4, weight = 2)

        Grid.columnconfigure(self.w_deliveryman, 0, weight = 3)
        Grid.columnconfigure(self.w_deliveryman, 1, weight = 1)

        etiqueta_titulo = Label(self.w_deliveryman, text="Autenticacion del Repartidor")
        etiqueta_titulo.grid(row=0,column=0,padx=5,pady=5,columnspan=2,sticky=NSEW)

        # Casilla para introducir el ID de Repartidor
        etiqueta_id = Label(self.w_deliveryman,text="ID Repartidor ")
        etiqueta_id.grid(row=1,column=0,padx=5,pady=5,sticky=NSEW)

        intro_id = Entry(self.w_deliveryman,textvariable=self.auth_id_repartidor)
        intro_id.grid(row=1,column=1,padx=5,pady=5,sticky=NSEW)

        # Casilla para introducir la contrasenia
        etiqueta_pass = Label(self.w_deliveryman,text="Password ")
        etiqueta_pass.grid(row=2,column=0,padx=5,pady=5,sticky=NSEW)

        intro_pass = Entry(self.w_deliveryman,textvariable=self.passwd_repartidor,show="*")
        intro_pass.grid(row=2,column=1,padx=5,pady=5,sticky=NSEW)

        # Boton para comprobar si son correctos los datos
        comprobacion = Button(self.w_deliveryman,text="Autenticar",command=self.check_deliveryman)
        comprobacion.grid(row=3,column=0,padx=5,pady=5,columnspan=2,sticky=NSEW)

    # COMPROBACION DE CREDENCIALES DEL REPARTIDOR
    def check_deliveryman(self):
        # Obtenemos los datos de entrada del repartidor
        id_repartidor = self.auth_id_repartidor.get()
        password = self.passwd_repartidor.get()

        # Query para comprobar el usuario y la contrasenia
        self.deliveryman_cursor.execute("SELECT ID_REPARTIDOR,NOMBRE FROM REPARTIDOR WHERE ID_REPARTIDOR=? AND PASSWORD=?",(id_repartidor,password))

        resultado_contrasenia = 0

        for resultado in self.deliveryman_cursor:
            resultado_contrasenia = resultado_contrasenia + 1

        if (resultado_contrasenia == 0):
            etiqueta_password = Label(self.w_deliveryman,fg="red",text="        ID o password incorrecto, intentelo de nuevo        ")
            etiqueta_password.grid(row=4,column=0,padx=5,pady=5,sticky=NSEW)
        elif (resultado_contrasenia == 1):
            self.id_repartidor=id_repartidor
            self.main_repartidor()

    # LIMPIEZA DE WIDGETS EN LA VENTANA W_DELIVERYMAN
    def clean_w(self):
        for widget in self.w_deliveryman.winfo_children():
            widget.destroy()

    # VENTANA PRINCIPAL DEL REPARTIDOR DONDE TENDRA TODAS SUS FUNCIONALIDADES
    def main_repartidor(self):
        self.w_deliveryman.geometry('400x200')
        self.w_deliveryman.title('Area Repartidores')

        # Limpiamos widgets si los hay
        self.clean_w()

        Grid.rowconfigure(self.w_deliveryman, 0, weight = 2)
        Grid.rowconfigure(self.w_deliveryman, 1, weight = 2)
        Grid.rowconfigure(self.w_deliveryman, 2, weight = 2)
        Grid.rowconfigure(self.w_deliveryman, 3, weight = 2)
        Grid.rowconfigure(self.w_deliveryman, 4, weight = 2)
        Grid.rowconfigure(self.w_deliveryman, 5, weight = 2)

        Grid.columnconfigure(self.w_deliveryman, 0, weight = 3)
        Grid.columnconfigure(self.w_deliveryman, 1, weight = 1)

        etiquetas = range(len(self.opciones))
        for i in etiquetas:
            l = Label(self.w_deliveryman,text=self.opciones[i])
            l.grid(row=i,column=0,padx=5,pady=5,sticky=NSEW)
            b = Button(self.w_deliveryman, text=self.opciones_b[i], command=self.comandos[i])
            b.grid(row=i, column=1,padx=5,pady=5,sticky=NSEW)

    # FUNCIONALIDAD DEL REPARTIDOR PARA VISUALIZAR LOS PEDIDOS PENDIENTES DE ENVIO
    def ver_pedidos(self):
        # Limpiamos la ventana principal para reutilizarla
        self.clean_w()

        # Consulta para ver los pedidos pendientes de envio
        self.deliveryman_cursor.execute("SELECT * FROM PEDIDO WHERE ESTADO=1 AND FECHA_ENTREGA_PROGRAMADA<=NOW()")

        # Obtenemos los nombres de las columnas
        column_headers = []
        size_columns = len(self.deliveryman_cursor.description)
        # Por cada una de las columnas de la tabla PEDIDOS, cogemos su cabecera y la guardamos en el array column_headers
        for i in range(size_columns):
            column_headers.append(self.deliveryman_cursor.description[i][0])

        # Creamos el treeview para visualizar los elementos
        tabla = ttk.Treeview(self.w_deliveryman, columns=column_headers, height=10, show='headings', selectmode="none")
                  
        # Ajuste de anchura de las columnas
        for d in range(size_columns):
            tabla.column(column_headers[d],width=100,minwidth=100)

        # Ubicamos el texto en la ventana
        for i in range(size_columns):
            tabla.heading(column_headers[i], text=column_headers[i], anchor=CENTER)

        # Obtenemos los datos de la tabla
        datos_fila = []

        for pedidos in self.deliveryman_cursor:
            for i in range(len(pedidos)):
                datos_fila.append(pedidos[i])
            print(datos_fila)
            tabla.insert('', END, values=datos_fila) # Datos fila obviamente no esta obteniendo nada
            datos_fila.clear()

        # Creamos un scroll vertical a la derecha
        scrollbar = Scrollbar(self.w_deliveryman, orient='vertical', command=tabla.yview)

        # Configuramos la tabla para hacer scroll
        tabla.configure(yscrollcommand=scrollbar.set)

        # Configuramos la visualizacion
        self.w_deliveryman.geometry('1100x400')
        
        # Ajustamos para que se vean bien las columnas de los pedidos
        tabla.grid(row=0,column=0,padx=30,pady=30,sticky=NSEW)
        scrollbar.grid(row=0,column=1,padx=3,pady=3,sticky=NS)

        boton_salir = Button(self.w_deliveryman, text="Salir", command=self.main_repartidor)
        boton_salir.grid(row=1,column=0,padx=5,pady=5,sticky=NS)

    
    # FUNCION PARA SELECCIONAR UN PEDIDO Y EMPEZAR A REPARTIRLO
    def seleccionar_pedido(self):
        # Limpiamos los widgets
        self.clean_w()

        # Redefinimos la ventana
        self.w_deliveryman.geometry('400x200')
        self.w_deliveryman.title('Seleccionar pedido para repartir')
        
        # PRIMERA FILA para introducir el ID Pedido deseado
        # SEGUNDA FILA de consulta de pedidos pendientes de envio
        # TERCERA FILA de seleccion de pedido
        # CUARTA FILA de boton de salir 
        Grid.rowconfigure(self.w_deliveryman,0,weight=2)
        Grid.rowconfigure(self.w_deliveryman,1,weight=2)
        Grid.rowconfigure(self.w_deliveryman,2,weight=2)
        Grid.rowconfigure(self.w_deliveryman,3,weight=2)

        # PRIMERA FILA
        etiqueta = Label(self.w_deliveryman,text="ID Pedido a elegir: ")
        etiqueta.grid(row=0,column=0,padx=5,pady=5,sticky=NSEW)

        id_ped = StringVar()

        # Caja de introduccion de pedido
        intro_id_pedido = Entry(self.w_deliveryman,textvariable=id_ped)
        intro_id_pedido.grid(row=0,column=1,padx=5,pady=5,sticky=NSEW)

        # SEGUNDA FILA consulta de pedidos pendientes de envio
        etiqueta = Label(self.w_deliveryman,text="Consulta los pedidos pendientes")
        etiqueta.grid(row=1,column=0,padx=5,pady=5,sticky=NSEW)

        boton_consulta = Button(self.w_deliveryman, text="Consultar pedidos", command=self.ver_pedidos_aux)
        boton_consulta.grid(row=1,column=1,padx=5,pady=5,sticky=NSEW)

        # TERCERA FILA seleccionar pedido
        seleccion = Button(self.w_deliveryman, text="Seleccionar pedido", command=lambda: self.order_selection(id_ped.get()))
        seleccion.grid(row=2,column=0,padx=5,pady=5,sticky=NSEW)

        # CUARTA FILA salir al menu de repartidor
        boton_salir = Button(self.w_deliveryman, text="Salir", command=self.main_repartidor)
        boton_salir.grid(row=2,column=1,padx=5,pady=5,sticky=NSEW)

    # FUNCIONALIDAD PARA PODER VISUALIZAR LOS PEDIDOS DENTRO DE SELECCION DE PEDIDO
    def ver_pedidos_aux(self):
        self.deliveryman_cursor.execute("SELECT * FROM PEDIDO WHERE ESTADO=1 AND FECHA_ENTREGA_PROGRAMADA<=NOW()")

        column_headers = []
        size_columns = len(self.deliveryman_cursor.description)
        # Por cada una de las columnas de la tabla PEDIDOS, cogemos su cabecera y la guardamos en el array column_headers
        for i in range(size_columns):
            column_headers.append(self.deliveryman_cursor.description[i][0])

        # Creamos una ventana auxiliar donde visualizarlo
        w_aux_pedidos = Toplevel(self.w_deliveryman)
        w_aux_pedidos.title('Pedidos Pendientes')

        # Creamos el treeview para visualizar los elementos
        tabla = ttk.Treeview(w_aux_pedidos, columns=column_headers, height=10, show='headings', selectmode="none")
                  
        # Ajuste de anchura de las columnas
        for d in range(size_columns):
            tabla.column(column_headers[d],width=100,minwidth=100)

        # Ubicamos el texto en la ventana
        for i in range(size_columns):
            tabla.heading(column_headers[i], text=column_headers[i], anchor=CENTER)

        # Obtenemos los datos de la tabla
        datos_fila = []

        for pedidos in self.deliveryman_cursor:
            for i in range(len(pedidos)):
                datos_fila.append(pedidos[i])
            print(datos_fila)
            tabla.insert('', END, values=datos_fila) # Datos fila obviamente no esta obteniendo nada
            datos_fila.clear()

        # Creamos un scroll vertical a la derecha
        scrollbar = Scrollbar(w_aux_pedidos, orient='vertical', command=tabla.yview)

        # Configuramos la tabla para hacer scroll
        tabla.configure(yscrollcommand=scrollbar.set)

        # Configuramos la visualizacion
        w_aux_pedidos.geometry('1100x400')

        #Ajuste de Grid de las columnas y filas
        # Primera fila TreeView y scroll Col 0 y 1 respectivamente
        Grid.rowconfigure(w_aux_pedidos, 0, weight = 2)

        # Ajuste de columnas
        Grid.columnconfigure(w_aux_pedidos, 0, weight = 3)
        Grid.columnconfigure(w_aux_pedidos, 1, weight = 1)
        
        # Ajustamos para que se vean bien las columnas de los pedidos
        tabla.grid(row=0,column=0,padx=30,pady=30,sticky=NSEW)
        scrollbar.grid(row=0,column=1,padx=3,pady=3,sticky=NS)

        boton_salir = Button(w_aux_pedidos, text="Salir", command=w_aux_pedidos.destroy)
        boton_salir.grid(row=1,column=0,padx=5,pady=5,sticky=NS)

    # FUNCION AUXILIAR PARA LA SELECCION DE PEDIDOS QUE REALIZA OPERACIONES EN LA BASE DE DATOS
    def order_selection(self, id_pedido):
        print(id_pedido)
        # Como controlo que el pedido no este vacio y me de un error?
        try:
            self.deliveryman_cursor.execute("SAVEPOINT SELECCION_PEDIDO")
            self.deliveryman_cursor.execute("UPDATE PEDIDO SET ESTADO=2, ID_REPARTIDOR=? WHERE ID_PEDIDO=?",(self.id_repartidor,id_pedido,))
            self.deliveryman_cursor.execute("COMMIT")

            etiqueta_seleccion = Label(self.w_deliveryman,fg="blue",text="                     Pedido seleccionado correctamente.                       ")
            etiqueta_seleccion.grid(row=4,column=0,columnspan=2,padx=5,pady=5,sticky=NSEW)

        except self.deliveryman_conn.Error as error_execution:
            etiqueta_seleccion = Label(self.w_deliveryman,fg="red",text=format(error_execution))
            etiqueta_seleccion.grid(row=4,column=0,columnspan=2,padx=5,pady=5,sticky=NSEW)
            self.deliveryman_cursor.execute("ROLLBACK TO SELECCION_PEDIDO")

    def modificar_datos(self):
        # Limpiamos la ventana principal
        self.clean_w()

        # Redefinimos la ventana
        self.w_deliveryman.geometry('500x200')
        self.w_deliveryman.title('Modificar fecha de reparto')

        # Ajuste de filas
        Grid.rowconfigure(self.w_deliveryman, 0, weight = 2)
        Grid.rowconfigure(self.w_deliveryman, 1, weight = 2)
        Grid.rowconfigure(self.w_deliveryman, 2, weight = 2)
        Grid.rowconfigure(self.w_deliveryman, 3, weight = 2)

        # FILA 1 - Seleccion de pedido a modificar
        etiqueta_pedido = Label(self.w_deliveryman,text="Indique el ID de pedido a modificar  ")
        etiqueta_pedido.grid(row=0,column=0,padx=5,pady=5,sticky=NSEW)

        # Variable donde almacenaremos el id del pedido
        id_ped = StringVar()

        # Caja de entrada del pedido
        id_ped_entry = Entry(self.w_deliveryman,textvariable=id_ped)
        id_ped_entry.grid(row=0,column=1,padx=5,pady=5,sticky=NSEW)

        # FILA 2 - Introduccion de la fecha
        fecha = Label(self.w_deliveryman,text="Nueva fecha de entrega YYYY-MM-DD  ")
        fecha.grid(row=1,column=0,padx=5,pady=5,sticky=NSEW)

        # Ponemos la fecha de ahora por defecto
        now = datetime.now()
        string_fecha = StringVar(value=now.strftime('%Y-%m-%d'))

        #Ponemos la caja de introducion de la nueva fecha
        fecha_entry = Entry(self.w_deliveryman,textvariable=string_fecha)
        fecha_entry.grid(row=1,column=1,padx=5,pady=5,sticky=NSEW)

        # FILA 3 - Consulta de pedidos en una ventana auxiliar
        etiqueta_consulta = Label(self.w_deliveryman,text="Consulta tus pedidos  ")
        etiqueta_consulta.grid(row=2,column=0,padx=5,pady=5,sticky=NSEW)

        # Boton de la consulta de pedidos del Repartidor actual
        consulta_pedidos = Button(self.w_deliveryman,text="Consultar pedidos",command=self.ver_pedidos_id)
        consulta_pedidos.grid(row=2,column=1,padx=5,pady=5,sticky=NSEW)

        # FILA 4 - Modificar fecha y salir al menu repartidor
        boton_modificar = Button(self.w_deliveryman, text="Modificar pedido", command=lambda: self.modify_transaction(string_fecha.get(),id_ped.get()))
        boton_modificar.grid(row=3,column=0,padx=5,pady=5,sticky=NSEW)

        boton_salir = Button(self.w_deliveryman, text="Volver al menu", command=self.main_repartidor)
        boton_salir.grid(row=3,column=1,padx=5,pady=5,sticky=NSEW)

    # METODO AUXILIAR PARA MODIFICAR EL ENVIO SELECCIONADO POR STRING_FECHA
    def modify_transaction(self,fecha,id_pedido):
        print(fecha)
        print(id_pedido)
        try:
            self.deliveryman_cursor.execute("SAVEPOINT MODIFY")
            self.deliveryman_cursor.execute("UPDATE PEDIDO SET ESTADO=?, FECHA_ENTREGA_PROGRAMADA=?, ID_REPARTIDOR=NULL WHERE ID_PEDIDO=?", (1,fecha,id_pedido,))
            self.deliveryman_cursor.execute("COMMIT")

            l_modify_error = Label(self.w_deliveryman,fg="blue",text="                     Pedido modificado con exito                       ")
            l_modify_error.grid(row=5,column=0,columnspan=2,padx=5,pady=5)
        except self.deliveryman_conn.Error as error_execution:
            l_modify_error = Label(self.w_deliveryman,fg="red",text=format(error_execution))
            l_modify_error.grid(row=5,column=0,columnspan=2,padx=5,pady=5)
            self.deliveryman_cursor.execute("ROLLBACK TO MODIFY")

            # METER TRIGGER PARA COMPROBAR SI EL PEDIDO ES SUYO Y VER SI ESTA EL DE LA FECHA


    # FUNCIONALIDAD PARA PODER VISUALIZAR LOS PEDIDOS DENTRO DE SELECCION DE PEDIDO
    def ver_pedidos_id(self):
        self.deliveryman_cursor.execute("SELECT * FROM PEDIDO WHERE ID_REPARTIDOR=?", (self.id_repartidor,))

        column_headers = []
        size_columns = len(self.deliveryman_cursor.description)
        # Por cada una de las columnas de la tabla PEDIDOS, cogemos su cabecera y la guardamos en el array column_headers
        for i in range(size_columns):
            column_headers.append(self.deliveryman_cursor.description[i][0])

        # Creamos una ventana auxiliar donde visualizarlo
        w_aux_pedidos = Toplevel(self.w_deliveryman)
        w_aux_pedidos.title('Tus Pedidos')

        # Creamos el treeview para visualizar los elementos
        tabla = ttk.Treeview(w_aux_pedidos, columns=column_headers, height=10, show='headings', selectmode="none")
                  
        # Ajuste de anchura de las columnas
        for d in range(size_columns):
            tabla.column(column_headers[d],width=100,minwidth=100)

        # Ubicamos el texto en la ventana
        for i in range(size_columns):
            tabla.heading(column_headers[i], text=column_headers[i], anchor=CENTER)

        # Obtenemos los datos de la tabla
        datos_fila = []

        for pedidos in self.deliveryman_cursor:
            for i in range(len(pedidos)):
                datos_fila.append(pedidos[i])
            print(datos_fila)
            tabla.insert('', END, values=datos_fila) # Datos fila obviamente no esta obteniendo nada
            datos_fila.clear()

        # Creamos un scroll vertical a la derecha
        scrollbar = Scrollbar(w_aux_pedidos, orient='vertical', command=tabla.yview)

        # Configuramos la tabla para hacer scroll
        tabla.configure(yscrollcommand=scrollbar.set)

        # Configuramos la visualizacion
        w_aux_pedidos.geometry('1100x400')

        #Ajuste de Grid de las columnas y filas
        # Primera fila TreeView y scroll Col 0 y 1 respectivamente
        Grid.rowconfigure(w_aux_pedidos, 0, weight = 2)

        # Ajuste de columnas
        Grid.columnconfigure(w_aux_pedidos, 0, weight = 3)
        Grid.columnconfigure(w_aux_pedidos, 1, weight = 1)
        
        # Ajustamos para que se vean bien las columnas de los pedidos
        tabla.grid(row=0,column=0,padx=30,pady=30,sticky=NSEW)
        scrollbar.grid(row=0,column=1,padx=3,pady=3,sticky=NS)

        boton_salir = Button(w_aux_pedidos, text="Salir", command=w_aux_pedidos.destroy)
        boton_salir.grid(row=1,column=0,padx=5,pady=5,sticky=NS)
        
        
    def confirmar_pedido(self):
        print("Hola")

    def cancelar_pedido(self):
        print("Hola")