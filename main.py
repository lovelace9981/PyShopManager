import mariadb
import sys
from tkinter import *
from tkinter import ttk

from subsistemas.clientes import Cliente
from subsistemas.repartidores import Repartidor

#Importacion de menus de terminal prefabricados

#user = Usuario que tiene permisos de creacion de tablas sobre la base de datos
#password = contrasenia en texto plano
#host = IP o dominio del servidor de SQL MariaDB
#port = puerto del listener de MariaDB
#database = base de datos por defecto que se quiere usar en esta conexion

try:
    conn = mariadb.connect(
        user="tiendabd",
        password="password",
        host="localhost",
        database="tiendabd",
        port=3306
    )
except mariadb.Error as err:
        print(err, file=sys.stderr)
        sys.exit(1)

# Inicializacion de la interfaz
root = Tk()

# Nombre y tamaño inicial de la ventana
root.title('Sistema Gestor de Tienda')
root.geometry('400x200')

Grid.rowconfigure(root, 0, weight = 2)
Grid.rowconfigure(root, 1, weight = 2)
Grid.rowconfigure(root, 2, weight = 2)
Grid.rowconfigure(root, 3, weight = 2)

Grid.columnconfigure(root, 0, weight = 3)
Grid.columnconfigure(root, 1, weight = 1)

# Funciones para cada uno de los botones
# Ventana de cliente
def client_area():
    w_client = Toplevel(root)
    instanciate_client = Cliente(conn, w_client)
    instanciate_client.auth_client()

# Ventana de empleado
def employee_area():
    employee_win = Toplevel(root)
    employee_win.geometry('400x400')
    employee_win.title('Area Empleado')

# Ventana de repartidor
def delivery_area():
    delivery_win = Toplevel(root)
    instanciate_deliveryman = Repartidor(conn, delivery_win)
    # instanciate_deliveryman.


# Arrays de etiquetas y botones
opciones_l = ['Area Clientes','Area Empleados','Area Repartidores','Salir']
opciones_b = ['Clientes','Empleados','Repartidores','Salir']
commands = [client_area,employee_area,delivery_area,root.destroy]

labels = range(4)
for i in range(4):
    l = Label(root,text=opciones_l[i])
    l.grid(row=i,column=0,sticky=NSEW, padx=5, pady=5)
    b = Button(root, text=opciones_b[i], command=commands[i])
    b.grid(row=i,column=1,sticky=NSEW,padx=5, pady=5)

root.mainloop()

conn.close()