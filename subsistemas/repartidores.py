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
        self.opciones = ['Ver pedidos pendientes de envio', 'Seleccionar pedido para repartir', 'Modificar datos de envio', 'Confirmar envio', 'Cancelar envio']
        self.opciones_b = ['Ver pedidos', 'Seleccionar', 'Modificar datos', 'Confirmar', 'Cancelar']
        self.comandos = [self.ver_pedidos, self.seleccionar_pedido, self.modificar_datos, self.confirmar_pedido, self.cancelar_pedido]       
        # Obtencion de credenciales del repartidor
        self.auth_id_repartidor = StringVar()
        self.passwd_repartidor = StringVar()
        # ID del repartidor al autenticar
        self.id_repartidor = -1

    # Limpeza de widgets en la ventana w_deliveryman
    def clean_w(self):
        for widget in self.w_deliveryman.winfo_children():
            widget.destroy()

    def ver_pedidos(self):
        self.deliveryman_cursor.execute("SELECT * FROM PEDIDOS WHERE EN_REPARTO=0")

        self.clean_w()

        column_headers = []
        size_columns = len(self.deliveryman_cursor.description)
        # Por cada una de las columnas de la tabla PEDIDOS, cogemos su cabecera y la guardamos en el array column_headers
        for i in range(size_columns):
            column_headers.append(self.deliveryman_cursor.description[i][0])

        # Creamos el treeview para visualizar los elementos
        tabla = ttk.Treeview(self.w_deliveryman, columns=column_headers, show='headings', selectmode="none")

        # Ubicamos el texto en la ventana
        for i in range(size_columns):
            tabla.heading(column_headers[i], text=column_headers[i], anchor=CENTER)

        # Obtenemos los datos de la tabla
        datos_fila = []

        for pedidos in self.deliveryman_cursor:
            for i in range(len(pedidos)):
                datos_fila.append(pedidos[i])
            tabla.insert('', END, values=datos_fila)
            datos_fila.clear()

        # Creamos un scroll vertical a la derecha
        scrollbar = Scrollbar(self.w_deliveryman, orient='vertical', command=tabla.yview)

        # Configuramos la tabla para hacer scroll
        tabla.configure(yscrollcommand=scrollbar.set)

        # Configuramos la visualizacion
        self.w_deliveryman.geometry('800x400')
        
        # Ajustamos para que se vean bien las columnas de los pedidos
        tabla.grid(row=0, column=0, sticky=NSEW)
        scrollbar.grid(row=0, column=1, sticky=NS)

        boton_salir = Button(self.w_deliveryman, text="Menu Repartidor", command=self.main_repartidor)
        boton_salir.grid(row=1,column=0,sticky=NS)

    def order_selection(self, id_pedido):
        try:
            self.deliveryman_cursor.execute("SAVEPOINT SELECCION_PEDIDO")
            self.deliveryman_cursor.execute("UPDATE PEDIDO SET EN_REPARTO=1 WHERE ID_PEDIDO=?",(id_pedido))
            self.deliveryman_cursor.execute("COMMIT")

            etiqueta_seleccion = Label(self.w_deliveryman,fg="blue",text="                     Pedido seleccionado correctamente.                       ")
            etiqueta_seleccion.grid(row=4,column=0,columnspan=2,sticky=NSEW)

        except self.deliveryman_conn.Error as error_execution:
            etiqueta_seleccion = Label(self.w_deliveryman,fg="red",text=format(error_execution))
            etiqueta_seleccion.grid(row=4,column=0,columnspan=2,sticky=NSEW)
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
        etiqueta.grid(row=0,column=0,sticky=NSEW)

        id_ped = StringVar()

        # Caja de introduccion de pedido
        intro_id_pedido = Entry(self.w_deliveryman,textvariable=id_ped)
        intro_id_pedido.grid(row=0,column=1,sticky=NSEW)

        # SEGUNDA FILA consulta de pedidos pendientes de envio
        etiqueta = Label(self.w_deliveryman,text="Consulta los pedidos pendientes")
        etiqueta.grid(row=1,column=0,sitcky=NSEW)

        boton_consulta = Button(self.w_deliveryman, text="Consultar pedidos", command=self.ver_pedidos)
        boton_consulta.grid(row=1,column=1,sticky=NSEW)

        # TERCERA FILA seleccionar pedido
        seleccion = Button(self.w_deliveryman, text="Seleccionar pedido", command=self.order_selection)
        seleccion.grid(row=2,column=0,sticky=NSEW)

        # CUARTA FILA salir al menu de repartidor
        boton_salir = Button(self.w_deliveryman, text="Salir", command=self.main_repartidor)
        boton_salir.grid(row=3,column=0,sticky=NSEW)

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

        Grid.columnconfigure(self.w_deliveryman, 0, weight = 3)
        Grid.columnconfigure(self.w_deliveryman, 1, weight = 1)

        etiquetas = range(len(self.opciones))
        for i in etiquetas:
            l = Label(self.w_deliveryman,text=self.opciones[i])
            l.grid(row=i,column=0,sticky=NSEW)
            b = Button(self.w_deliveryman, text=self.opciones_b[i], command=self.comandos[i])
            b.grid(row=i, column=1, sticky=NSEW)
