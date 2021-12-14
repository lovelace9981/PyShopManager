DROP VIEW IF EXISTS VENTAS;
CREATE VIEW VENTAS AS
SELECT P.ID_CLIENTE, P.ID_PRODUCTO, S.NOMBRE, P.CANTIDAD
FROM PEDIDO AS P
INNER JOIN STOCK AS S 
ON P.ID_PRODUCTO = S.ID_PRODUCTO;