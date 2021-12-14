#!/bin/bash

echo Regenerando tablas
mysql --user=tiendabd --password=password --database=tiendabd < scripts_sql/tablas.sql

echo Regenerando triggers
mysql --user=tiendabd --password=password --database=tiendabd < scripts_sql/triggers.sql

echo Regenerando vistas
mysql --user=tiendabd --password=password --database=tiendabd < scripts_sql/view.sql

echo Regenerando dml
mysql --user=tiendabd --password=password --database=tiendabd < scripts_sql/dml.sql