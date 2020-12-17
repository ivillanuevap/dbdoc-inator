# DBDoc-inator(Database documentation generator)

## Supported Databases(tested)
* MySQL
* Oracle
* MSSQL

## Supported Databases(NO tested)
_SQLAlchemy supported databases_
* SQLite
* Postgresql 
* Firebird
* Sybase
* Others, most of which support multiple DBAPIs

## Generated documents
_This project generates docx files_
* Data Dictionary
* Database growth projection

_TODO_
* ERM Diagram
* Schema build script

## Requirements
_It is required to have Python3 installed as well as the packages:_
* setuptools
* wheel
* python-docx

_Make sure you have the PIP package manager installed_
```
apt install python-pip
```
_Required packages_
```
pip install -U setuptools
pip install -U wheel
pip install mysql-connector-python-rf
pip install python-docx
apt install python-pip
pip install python-docx
pip install cx_Oracle
pip install SQLAlchemy
pip install console-progressbar
pip install pymssql
```

## How to generate documentation?
_To generate the documentation in a terminal execute_
```
python dbdoc.py
```
### Parameters
_Modify the dbdoc.py file to connect to your database_


## How to customize the templates?
_Go to the **./template/** folder and edit the files_
* diccionario.docx
* proyeccion.docx

_The generator will take the format and add the corresponding information. The generated files will be stored in **./output**_

_**Do not take the generated files as the deliverables, make sure you:**_
* Change the texts and what has to be changed
* Check spelling
* Complement or modify the generated texts