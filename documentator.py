#!/usr/bin/python
import sys, getopt
from dbengine import Dbengine
from proyeccion import Proyeccion
from diccionario import Diccionario

def main(argv):
    #print("Inicia generacion de documentacion de base de datos MySQL")
    db_engine = 'mysql'
    host = '127.0.0.1'
    user = 'root'
    password = ''
    database = ''
    input_enable = 0
    try:
        opts, args = getopt.getopt(argv, "hi:o:", [
            "h=", "u=", "p=", "d=", "i=",
            "host=", "user=", "password=", "database=", "input="
        ])
    except getopt.GetoptError:
        print('ERROR')
        print(getopt.GetoptError.msg)
        print('Revisa el archivo README.md o reporta el problema')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-help':
            print('Revisa el archivo README.md o reporta el problema')
            sys.exit()
        elif opt in ("-h", "--host"):
            host = arg
        elif opt in ("-u", "--user"):
            user = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-d", "--database"):
            database = arg
        elif opt in ("-i", "--input"):
            if arg == 'true':
                input_enable = 1


    dbEngine = Dbengine(db_engine, host, user, password, database)

    json = {
        'schema': dbEngine.schema,
        'db_engine': dbEngine.db_engine,
        'initial_size': 0,
        'proyection': {
            '1y': 0,
            '2y': 0
        },
        'tables': []
    }
    tables = dbEngine.getTables()
    db_initial_size = 0
    for t in tables:
        table = t[0]
        print("Retrive info from: " + table)

        table_size = dbEngine.getSizeTable(table)  # TODO - check this value
        rows_count = dbEngine.getTotalRows(table)
        row_size = 0
        if (rows_count > 0):
            row_size = table_size / rows_count
        description_table = dbEngine.getDescripcionTable(table)
        index_size = description_table['size']
        total_size = table_size + index_size
        proy_1_year = float(total_size) * 1.3
        proy_2_year = float(proy_1_year) * 1.3

        db_initial_size += total_size

        table_json = {
            'name': str(table),
            'rows_count': rows_count,
            'row_size': float(row_size),
            'table_size': float(table_size),
            'table_index': float(index_size),
            'total_size': float(table_size + index_size),
            'proyection': {
                '1y': proy_1_year,
                '2y': proy_2_year
            },
            'total_size_bytes': total_size,
            'rows': [],
            #'index': [],
            'fk': []
        }

        index_i = 1
        for i in dbEngine.getFk(dbEngine.schema, table):
            table_name = i[0]
            column_name = i[1]
            referenced_table_name = i[2]
            referenced_column_name = i[3]
            table_json['fk'].append({
                'no': index_i,
                'column_name': column_name,
                'reference_column': referenced_column_name,
                'reference_table': referenced_table_name,
            })
            index_i += 1
        if index_i == 1:
            table_json['fk'].append({
                'no': index_i,
                'column_name': 'N/A',
                'reference_column': 'N/A',
                'reference_table': 'N/A',
            })

        table_columns_size = 0
        index_esp = 1
        for key in description_table['columns']:
            try:
                table_columns_size += int(description_table['columns'][key]['size'])
            except:
                table_columns_size  # TODO - check this fucking shit
            table_json['rows'].append({
                'name': key,
                'full_size': str(description_table['columns'][key]['full_size']),
                'full_type': str(description_table['columns'][key]['full_type']),
                'type': str(description_table['columns'][key]['type']),
                'size': str(description_table['columns'][key]['size']),
                'null': str(description_table['columns'][key]['null']),
                'primary_key': str(description_table['columns'][key]['primary_key']),
                'foreign_key': str(description_table['columns'][key]['foreign_key']),
                'default': str(description_table['columns'][key]['default']),
                'auto_increment': str(description_table['columns'][key]['auto_increment'])
            })
            index_esp += 1
        index_esp += 1
        table_json['total_size_bytes'] = table_columns_size

        json['initial_size'] = db_initial_size;
        json['proyection']['1y'] = float(db_initial_size) * 1.3;
        json['proyection']['2y'] = float(json['proyection']['1y']) * 1.3;

        json['tables'].append(table_json)
    Diccionario(json)
    Proyeccion(json, input_enable)
if __name__ == "__main__":
    main(sys.argv[1:])