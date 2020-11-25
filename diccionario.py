# -*- coding: utf-8 -*-
from documento import Documento

class Diccionario:

    src_template = 'template/diccionario.docx'
    output = 'output/{schema}_diccionario_v1.0.docx'

    def chispaAll(self, search, replace, string):
        while(string.find(search) > 0):
            string = string.replace(search, replace)
        return string;

    def __init__(self, json):
        documento = Documento(self.src_template)

        t = 1  # Because thead is 0
        for json_table in json['tables']:
            documento.createHeading("1." + str(t) + ". " + json_table['name'])

            json_table_table = {
                'rows': 4 + len(json_table['rows']),
                'cols': 11,
                'thead': {  # Headers by rows
                    0: {
                        'style': 'normal',
                        'text': {
                            0: 'Nombre de la Tabla o Vista:',
                            4: str(json_table['name']),
                        }
                    },
                    1: {
                        'style': 'normal',
                        'text': {
                            0: 'Descripcion:',
                            4: 'Contiene registros de ' + str(json_table['name']),
                        }
                    },
                    2: {
                        'style': 'bold',
                        'text': {
                            0: 'Columnas de la tabla o vista:'
                        }
                    },
                    3: {
                        'style': 'bold',
                        'text': {
                            0: 'No.',
                            1: 'Nombre',
                            2: 'Tipo de dato',
                            3: 'Tamanio',
                            4: 'Nulo (Nullable)',
                            5: 'Llave Primaria(PK)',
                            6: 'Llave Foranea(FK)',
                            7: 'Valor por Default',
                            8: 'Autoincremental',
                            9: 'Unicidad(unique)',
                            10: 'Descripcion'
                        }
                    },
                },
                'tbody': {},
                'merge': [
                    {'a': [0, 0], 'b': [0, 2]},
                    {'a': [0, 3], 'b': [0, 10]},

                    {'a': [1, 0], 'b': [1, 2]},
                    {'a': [1, 3], 'b': [1, 10]},

                    {'a': [2, 0], 'b': [2, 10]},
                ]
            }

            r = 4
            index_table_field = ''
            index_table_type = ''
            for row in json_table['rows']:
                description = self.chispaAll('_', ' ', row['name']).capitalize()
                if row['primary_key'] == 'PK':
                    description = 'Indice'
                    index_table_field = str(row['name'])
                    index_table_type = str(row['type'])
                elif row['foreign_key'] == 'FK':
                    description = 'Relacion con ' + self.chispaAll('_', ' ', row['name']).replace('id', '').capitalize()

                json_table_table['tbody'][r] = {
                    'style': 'normal',
                    'text': {
                        0: str(r-3),
                        1: str(row['name']),
                        2: str(row['type']),
                        3: str(row['size']),
                        4: str(row['null']),
                        5: str(row['primary_key']),
                        6: str(row['foreign_key']),
                        7: str(row['default']),
                        8: str(row['auto_increment']),
                        9: '',
                        10: description
                    }
                }
                # TODO - Get index properly
                json_index_table = {
                    'rows': 3,
                    'cols': 4,
                    'thead': {
                        0: {
                            'style': 'bold',
                            'text': {
                                0: 'Indices',
                            }
                        },
                        1: {
                            'style': 'bold',
                            'text': {
                                0: 'No.',
                                1: 'Nombre',
                                2: 'Tipo',
                                3: 'Columnas'
                            }
                        },
                    },
                    'tbody': {
                        2: {
                            'style': 'normal',
                            'text': {
                                0: '1',
                                1: index_table_field,
                                2: index_table_type,
                                3: ''
                            }
                        }
                    },
                    'merge': [
                        {'a': [0, 0], 'b': [0, 3]},
                    ]
                }
                json_fk_table = {
                    'rows': 3,
                    'cols': 4,
                    'thead': {
                        0: {
                            'style': 'bold',
                            'text': {
                                0: 'Llaves de Referencia',
                            }
                        },
                        1: {
                            'style': 'bold',
                            'text': {
                                0: 'No.',
                                1: 'Nombre',
                                2: 'Columna',
                                3: 'Referenciado con'
                            }
                        },
                    },
                    'tbody': {},
                    'merge': [
                        {'a': [0, 0], 'b': [0, 3]},
                    ]
                }
                i_td = 2
                for td in json_table['fk']:
                    json_fk_table['tbody'][i_td] = {
                        'style': 'normal',
                        'text': {
                            0: str(td['no']),
                            1: str(td['column_name']),
                            2: str(td['reference_column']),
                            3: str(td['reference_table']),
                        }
                    }
                    i_td += 1

                r += 1


            documento.createTable(json_table_table)
            documento.createParagraph('')
            documento.createTable(json_index_table)
            documento.createParagraph('')
            documento.createTable(json_fk_table)
            documento.createParagraph('')
            # TODO - ADD index table
            # TODO - ADD FK table

        documento.save(self.output.replace('{schema}', json['schema']))