import mariadb
import sys
import time
from tkinter import *
from tkinter import ttk

class Repartidor:
    # Constructor
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

    # Limpeza de widgets en la ventana w_deliveryman
    def clean_w(self):
        for widget in self.w_deliveryman.winfo_children():
            widget.destroy()

    def modificar_datos(self):
        print("Hola")
        
    def confirmar_pedido(self):
        print("Hola")

    def cancelar_pedido(self):
        print("Hola")

    def ver_pedidos(self):
        self.deliveryman_cursor.execute("SELECT * FROM PEDIDO WHERE EN_REPARTO=0")

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

    def order_selection(self, id_pedido):
        print(id_pedido)

        try:
            self.deliveryman_cursor.execute("SAVEPOINT SELECCION_PEDIDO")
            self.deliveryman_cursor.execute("UPDATE PEDIDO SET EN_REPARTO=1, ID_REPARTIDOR=? WHERE ID_PEDIDO=?",(self.id_repartidor,id_pedido,))
            self.deliveryman_cursor.execute("COMMIT")

            etiqueta_seleccion = Label(self.w_deliveryman,fg="blue",text="                     Pedido seleccionado correctamente.                       ")
            etiqueta_seleccion.grid(row=4,column=0,columnspan=2,padx=5,pady=5,sticky=NSEW)

        except self.deliveryman_conn.Error as error_execution:
            etiqueta_seleccion = Label(self.w_deliveryman,fg="red",text=format(error_execution))
            etiqueta_seleccion.grid(row=4,column=0,columnspan=2,padx=5,pady=5,sticky=NSEW)
            self.deliveryman_cursor.execute("ROLLBACK TO SELECCION_PEDIDO")

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

        boton_consulta = Button(self.w_deliveryman, text="Consultar pedidos", command=self.ver_pedidos)
        boton_consulta.grid(row=1,column=1,padx=5,pady=5,sticky=NSEW)

        # TERCERA FILA seleccionar pedido
        seleccion = Button(self.w_deliveryman, text="Seleccionar pedido", command=lambda: self.order_selection(id_ped.get()))
        seleccion.grid(row=2,column=0,padx=5,pady=5,sticky=NSEW)

        # CUARTA FILA salir al menu de repartidor
        boton_salir = Button(self.w_deliveryman, text="Salir", command=self.main_repartidor)
        boton_salir.grid(row=2,column=1,padx=5,pady=5,sticky=NSEW)

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