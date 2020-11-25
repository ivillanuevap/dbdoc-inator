# Generador de documentación de base de datos(MySQL)

_Este proyecto genera archivos docx_
* Diccionario
* Proyección

##Requerimientos

_Se requiere tener Python instalado asi como los paquetes:_
* setuptools
* wheel
* mysql-connector-python-rf
* python-docx

_Asegurate de tener instalado el administrador de paquetes PIP_
```
apt install python-pip
```
_Asegurate de tener instalados los paquetes necesarios_
```
pip install -U setuptools
pip install -U wheel
pip install mysql-connector-python-rf
pip install python-docx
```

##¿Como generar documentacion?
_Para generar la documentación en una terminal ejecuta_
```
python documentator.py --host 127.0.0.1 --user root --database schema_name
```
###Parametros
_Incorpora estos parametros para realizar la coneccion a MySQL_
* --host
* --user
* --password
* --database

_Incorpora este parametro con valor true para indicar que capturaras los numeros de registro por año de cada tabla_
* --input

_**Para la proyección de base de datos asegurate de que tomes un schema con informacion inicial, como si fuera el sistema en el dia 1(recien liberado a producción)**_

##¿Como cambiar las plantillas?
_Dirigete a la carpeta **./template/** y edita los archivos_
* diccionario.docx
* proyeccion.dox

_El generador tomara el formato y agregara la informacion correspondiente. Los archivos generados se almacenaran en **./output**_
_**No tomes los archivos generados como los entregables, asegurate bien de:**_
* Cambiar los textos y lo que se tenga que cambiar
* Revisar ortografica
* Complementar o modificar los textos generados

