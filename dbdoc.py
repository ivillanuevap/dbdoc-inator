# -*- coding: utf-8 -*-
import sqlalchemy, re, time
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, select, MetaData, Table, inspect
from classes.diccionario import Diccionario
#from classes.proyeccion import Proyeccion
from console_progressbar import ProgressBar

print("Connecting to database...")
engine = sqlalchemy.create_engine('mysql+mysqlconnector://user:password@localhost:3306/satabase', echo=False)

print("Retrieve information...")
database_metadata = sqlalchemy.MetaData()
database_metadata.reflect(bind=engine)

inspector = inspect(engine)
# print(inspector.get_table_names())

info_schema = {
    'schema': str(inspector.default_schema_name),
    'db_engine': None,
    'initial_size': 0,
    'proyection': {
        '1y': 0,
        '2y': 0
    },
    'tables': []
}

tables = engine.table_names()

i = 0
db_initial_size = 0
progress_table = ProgressBar(total=len(tables), prefix='', suffix='', decimals=2, length=50, fill='X', zfill='-')
for table in tables:
    #print("Retrive info from: " + table)
    progress_table.print_progress_bar(i+1)

    table_object = database_metadata.tables.get(table)
    # print(inspector.get_columns(table))
    # print(table_object.columns)
    query = table_object.count()
    # This will produce something like, where id is a primary key column in "table_name" automatically selected by sqlalchemy
    # 'SELECT count(table_name.id) AS tbl_row_count FROM table_name'

    count_result = engine.scalar(query)

    info_table = {
        'name': str(table),
        'rows_count': count_result,
        'size': {
            'row': 0,
            'index': 0,
            'table': 0,
            'total': 0
        },
        'row_size': float(0),
        'table_size': float(0),
        'table_index': float(0),
        'total_size': float(0 + 0),

        'proyection': {
            '1y': 0,
            '2y': 0
        },
        'total_size_bytes': 0,
        'rows': [],
        'pk': [],
        'fk': []
    }
    for column in table_object.columns:
        column = str(column).replace(table + '.', '')
        col = table_object.c[column]
        isFk = False
        fk_reference = ''

        if col.primary_key:
            info_table['pk'].append({
                'name': col.name,
                'type': col.type,
            })
        for fk in col.foreign_keys:
            isFk = True
            parts = str(fk).replace("ForeignKey(u'", '').split(".")
            fk_reference = parts[0].replace("ForeignKey('", "")
            fk_column = parts[1].replace("')", "")
            info_table['fk'].append({
                'name': col.name,
                'column': fk_column,
                'reference': fk_reference
            })

        length = ''
        type = str(col.type)

        typeArray = re.findall('[a-zA-Z]+', type)
        lengthArray = re.findall('\d+', type)
        # TODO - Poner elegante este pedo
        if len(typeArray) > 0:
            type = typeArray[0]
        if len(lengthArray) > 0:
            length = lengthArray[0]

        info_table['rows'].append({
            'name': col.name,
            'full_type': col.type,
            'type': type,
            'length': length,
            'null': col.nullable,
            'primary_key': col.primary_key,
            'foreign_key': isFk,
            'fk_reference': fk_reference,
            'default': col.default,
            'auto_increment': col.autoincrement
        })

    info_schema['tables'].append(info_table)
    i += 1

# print(info_schema)
dts = datetime.now()
Diccionario(info_schema)
dte = datetime.now()
diff = dte-dts
diff_in_seconds = diff.days*24*60*60 + diff.seconds
print("Finish dictionary in: " + str(diff_in_seconds) + "s")