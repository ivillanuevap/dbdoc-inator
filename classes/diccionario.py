# -*- coding: utf-8 -*-
from classes.documento import Documento
from console_progressbar import ProgressBar

class Diccionario:
    src_template = "template/diccionario.docx"
    output = "output/{schema}_diccionario.docx"

    def chispaAll(self, search, replace, string):
        while (string.find(search) > 0):
            string = string.replace(search, replace)
        return string;

    def __init__(self, json):
        documento = Documento(self.src_template)
        progress_table = ProgressBar(total=len(json["tables"]), prefix='', suffix='', decimals=2, length=50, fill='X', zfill='-')
        print("Building dictionary...")

        t = 1  # Because thead is 0
        for json_table in json["tables"]:
            json_table_table = {
                "rows": 4 + len(json_table["rows"]),
                "cols": 11,
                "thead": {  # Headers by rows
                    0: {
                        "style": "normal",
                        "text": {
                            0: "Nombre de la Tabla o Vista:",
                            4: str(json_table["name"]),
                        }
                    },
                    1: {
                        "style": "normal",
                        "text": {
                            0: "Descripcion:",
                            4: "Contiene registros de " + str(json_table["name"]),
                        }
                    },
                    2: {
                        "style": "bold",
                        "text": {
                            0: "Columnas de la tabla o vista:"
                        }
                    },
                    3: {
                        "style": "bold",
                        "text": {
                            0: "No.",
                            1: "Nombre",
                            2: "Tipo de dato",
                            3: "Tamanio",
                            4: "Nulo (Nullable)",
                            5: "Llave Primaria(PK)",
                            6: "Llave Foranea(FK)",
                            7: "Valor por Default",
                            8: "Autoincremental",
                            9: "Unicidad(unique)",
                            10: "Descripcion"
                        }
                    },
                },
                "tbody": {},
                "merge": [
                    {"a": [0, 0], "b": [0, 2]},
                    {"a": [0, 3], "b": [0, 10]},

                    {"a": [1, 0], "b": [1, 2]},
                    {"a": [1, 3], "b": [1, 10]},

                    {"a": [2, 0], "b": [2, 10]},
                ]
            }
            # Columns
            r = 4
            for row in json_table["rows"]:
                description = self.chispaAll("_", " ", row["name"]).capitalize()
                if row["primary_key"]:
                    description = "Indice"
                elif row["foreign_key"]:
                    description = "Relacion con " + self.chispaAll("_", " ", row["fk_reference"]).capitalize()

                json_table_table["tbody"][r] = {
                    "style": "normal",
                    "text": {
                        0: str(r - 3),
                        1: str(row["name"]),
                        2: str(row["type"]),
                        3: str(row["length"]),
                        4: str(row["null"]),
                        5: str(row["primary_key"]),
                        6: str(row["foreign_key"]),
                        7: str(row["default"]),
                        8: str(row["auto_increment"]),
                        9: "",
                        10: description
                    }
                }
                r += 1
            # PK
            json_index_table = {
                "rows": 2,
                "cols": 4,
                "thead": {
                    0: {
                        "style": "bold",
                        "text": {
                            0: "Indices",
                        }
                    },
                    1: {
                        "style": "bold",
                        "text": {
                            0: "No.",
                            1: "Nombre",
                            2: "Tipo",
                            3: "Columnas"
                        }
                    },
                },
                "tbody": {},
                "merge": [
                    {"a": [0, 0], "b": [0, 3]},
                ]
            }
            p = 1
            for pk in json_table["pk"]:
                json_index_table["tbody"][r - 1] = {
                    "style": "normal",
                    "text": {
                        0: str(p),
                        1: str(pk["name"]),
                        2: str(pk["type"])
                    }
                }
                p += 1
            # FK
            json_fk_table = {
                "rows": 3,
                "cols": 4,
                "thead": {
                    0: {
                        "style": "bold",
                        "text": {
                            0: "Llaves de Referencia",
                        }
                    },
                    1: {
                        "style": "bold",
                        "text": {
                            0: "No.",
                            1: "Nombre",
                            2: "Columna",
                            3: "Referenciado con"
                        }
                    },
                },
                "tbody": {},
                "merge": [
                    {"a": [0, 0], "b": [0, 3]},
                ]
            }
            f = 2
            if len(json_table["fk"]) > 0:
                for fk in json_table["fk"]:
                    json_fk_table["tbody"][f] = {
                        "style": "normal",
                        "text": {
                            0: str(f),
                            1: str(fk["name"]),
                            2: str(fk["column"]),
                            3: str(fk['reference']),
                        }
                    }
                    f += 1
            else:
                json_fk_table["tbody"][f] = {
                    "style": "normal",
                    "text": {
                        0: str(1),
                        1: "N/A",
                        2: "N/A",
                        3: "N/A",
                    }
                }
            progress_table.print_progress_bar(t)

            documento.createHeading("1." + str(t) + ". " + json_table["name"])
            documento.createTable(json_table_table)
            documento.createParagraph('')
            documento.createTable(json_index_table)
            documento.createParagraph('')
            documento.createTable(json_fk_table)
            documento.createParagraph('')
            t += 1

        documento.save(self.output.replace('{schema}', json['schema']))