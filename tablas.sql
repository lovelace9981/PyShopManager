--Primero creamos las tablas no relacionadas, es decir aquellas que no tienen claves FK.
--Las tablas son:
--  EMPLEADO
--  CLIENTE
--  CIUDADES
--  STOCK
--  REPARTIDOR
--  PEDIDO
DROP TABLE IF EXISTS ALTA_CLIENTE; -- Relacion con CLIENTE y EMPLEADO por FK
DROP TABLE IF EXISTS BAJA_CLIENTE; -- Relacion con CLIENTE y EMPLEADO por FK
DROP TABLE IF EXISTS ESTADO_REPARTO; 
DROP TABLE IF EXISTS PEDIDO; -- Relacion con CLIENTE, EMPLEADO REPARTIDOR STOCK por FK
DROP TABLE IF EXISTS CLIENTE; -- Relacion con CIUDADES por codigo postal de FK y con EMPLEADO
DROP TABLE IF EXISTS MOD_STOCK; --Relacion con STOCK ya que lleva el conteo de las actualizaciones de este

-- TABLAS NO RELACIONADAS
DROP TABLE IF EXISTS EMPLEADO;
DROP TABLE IF EXISTS CIUDADES;
DROP TABLE IF EXISTS STOCK;
DROP TABLE IF EXISTS REPARTIDOR;


CREATE TABLE EMPLEADO (
    ID_EMPLEADO INT(4) UNSIGNED AUTO_INCREMENT PRIMARY KEY, 
    NOMBRE VARCHAR(10),
    APELLIDO VARCHAR(10),
    PASSWORD VARCHAR(30)
);


CREATE TABLE REPARTIDOR (
    ID_REPARTIDOR INT(4) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    NOMBRE VARCHAR(10),
    PASSWORD VARCHAR(30)
);


CREATE TABLE CIUDADES (
    COD_POSTAL INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    NOMBRE VARCHAR(20)
);


CREATE TABLE CLIENTE(
    ID_CLIENTE INT(4) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    NOMBRE VARCHAR(10),
    TELEFONO INT(10) UNSIGNED,
    DIRECCION VARCHAR(30),
    COD_POSTAL INT(6) UNSIGNED,
    PASSWORD VARCHAR(30),
    ID_EMPLEADO_ALTA INT(4) UNSIGNED, -- Esto debe hacerlo un trigger ?
    ID_EMPLEADO_BAJA INT(4) UNSIGNED, -- Esto debe hacerlo un trigger ?

    CONSTRAINT UN_TELEFONO UNIQUE(TELEFONO),
    CONSTRAINT COD_POSTAL_FK FOREIGN KEY (COD_POSTAL) REFERENCES CIUDADES(COD_POSTAL),
    CONSTRAINT ID_ALTA_FK FOREIGN KEY (ID_EMPLEADO_ALTA) REFERENCES EMPLEADO(ID_EMPLEADO),
    CONSTRAINT ID_BAJA_FK FOREIGN KEY (ID_EMPLEADO_BAJA) REFERENCES EMPLEADO(ID_EMPLEADO)
);

-- Tablas de log  del TRIGGER de INSERCION BEFORE CLIENTE
CREATE TABLE ALTA_CLIENTE (
    ID_CLIENTE INT(4) UNSIGNED,
    ID_EMPLEADO INT(4) UNSIGNED,
    FECHA_ALTA DATE,    -- Esto debe hacerlo un trigger ?

    CONSTRAINT ID_CLIENTE_ALTA_FK FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTE(ID_CLIENTE),
    CONSTRAINT ID_EMPLEADO_ALTA_FK FOREIGN KEY (ID_EMPLEADO) REFERENCES EMPLEADO(ID_EMPLEADO)
);

-- Tablas de log del TRIGGER de UPDATE BEFORE CLIENTE
CREATE TABLE BAJA_CLIENTE (
    ID_CLIENTE INT(4) UNSIGNED,
    ID_EMPLEADO INT(4) UNSIGNED,
    FECHA_BAJA DATE,    -- Esto debe hacerlo un trigger ?

    CONSTRAINT ID_CLIENTE_BAJA_FK FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTE(ID_CLIENTE),
    CONSTRAINT ID_EMPLEADO_BAJA_FK FOREIGN KEY (ID_EMPLEADO) REFERENCES EMPLEADO(ID_EMPLEADO)
);
-- Posible CONSTRAINT CANTIDAD_MAYOR_QUE_0 CHECK(CANTIDAD>0)

CREATE TABLE STOCK (
    ID_PRODUCTO INT(4) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    NOMBRE VARCHAR(30),
    CANTIDAD INT(4)
);

CREATE TABLE MOD_STOCK(
    ID_PRODUCTO INT(4) UNSIGNED,
    FECHA_MODIFICACION DATE,
    VIEJA_CANTIDAD INT(4) UNSIGNED,
    NUEVA_CANTIDAD INT(4) UNSIGNED,

    CONSTRAINT ID_PRODUCTO_MOD_FK FOREIGN KEY (ID_PRODUCTO) REFERENCES STOCK(ID_PRODUCTO)
);

CREATE TABLE PEDIDO (
    ID_PEDIDO INT(4) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    ID_CLIENTE INT(4) UNSIGNED,
    ID_PRODUCTO INT(4) UNSIGNED,
    ID_REPARTIDOR INT(4) UNSIGNED,
    FECHA_PEDIDO DATE,
    FECHA_ENTREGA_PROGRAMADA DATE,
    REPARTIDO INT(1) UNSIGNED,
    EN_REPARTO INT(1) UNSIGNED,

    CONSTRAINT ID_CLIENTE_PEDIDO_FK FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTE(ID_CLIENTE),
    CONSTRAINT ID_PRODUCTO_PEDIDO_FK FOREIGN KEY (ID_PRODUCTO) REFERENCES STOCK(ID_PRODUCTO),
    CONSTRAINT ID_REPARTIDOR_PEDIDO_FK FOREIGN KEY (ID_REPARTIDOR) REFERENCES REPARTIDOR(ID_REPARTIDOR)  
);

CREATE TABLE ESTADO_REPARTO (
    ID_PEDIDO INT(4) UNSIGNED,
    ID_REPARTIDOR INT(4) UNSIGNED,
    FECHA_REPARTO DATE,
    FECHA_ENTREGA DATE,

    CONSTRAINT ID_PEDIDO_FK FOREIGN KEY (ID_PEDIDO) REFERENCES PEDIDO(ID_PEDIDO), 
    CONSTRAINT ID_REPARTIDOR_FK FOREIGN KEY (ID_REPARTIDOR) REFERENCES REPARTIDOR(ID_REPARTIDOR)
);