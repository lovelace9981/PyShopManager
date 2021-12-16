# Sistema de informacion de Gestión de Tienda

***Programa escrito en Python utilizando la librería Mariadb-connector para la conexión a base de datos y para la GUI utilizamos Tkinter como librería.***

Se ofrecen dos alternativas:
- Binario ejecutable directo, sin utilizar librerías de desarrollo.
- Código fuente del Sistema de Información que permita expandir el código con licencia GPLv3.0

# Prerrequisitos con el Binario

Instalar MariaDB como SGBD

- En sistemas Debian-like:

```bash
apt-get install mariadb-server mariadb-client libmariadb3
```

- En sistemas RedHat-like:

```bash
dnf install mariadb mariadb-server mariadb-connector-c
```

El Binario empaquetado se encuenta en dist/sistema_informacion_tienda

# Librerías de desarrollo

Necesitamos librerías de Tkinter y Mariadb-connector-python

- En sistemas Debian-like:

```bash
apt-get install build-essential
apt-get install libmariadb-dev python3-tk python3-dev
pip3 install mariadb
```

- En sistemas RedHat-like:

```bash
dnf groupinstall "Development Tools"
dnf install mariadb-devel python3-tkinter python3-devel
pip3 install mariadb
```

Para información más detallada sobre la instalación, visite [este link](https://mariadb.com/docs/clients/mariadb-connectors/connector-c/install/).
