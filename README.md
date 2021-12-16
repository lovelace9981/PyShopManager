El sistema de información la GUI utiliza Tkinter python como frontend.

El connector es de Mariadb.

Prerequisitos con el Binario:

Instalar MariaDB como SGBD

En sistemas Debian-like:

```bash
apt-get install mariadb-server mariadb-client libmariadb3
```

En sistemas RedHat-like:

```bash
dnf install mariadb mariadb-server mariadb-connector-c
```

El Binario empaquetado se encuenta en dist/sistema_informacion_tienda

Librería de desarrollo

Necesitamos librerías de Tkinter y Mariadb-connector-python

En sistemas Debian-like:

```bash
apt-get install libmariadb-dev python3-tk
pip3 install mariadb
```

En sistemas RedHat-like:

```bash
dnf install python3-tkinter 
pip3 install mariadb
```
