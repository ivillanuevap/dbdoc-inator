# -*- coding: utf-8 -*-
from documento import Documento

class Proyeccion:

    src_template = "template/proyeccion.docx"
    output = "output/{schema}proyeccion.docx"

    def __init__(self, json, input_enable):
        documento = Documento(self.src_template)
        json_gral_table = {
            "rows": 4,
            "cols": 6,
            "thead": { # Headers by rows
                0: {
                    "style": "bold",
                    "text": {
                        0: "Proyeccion de Crecimiento de Base de Datos"
                    }
                },
                1: {
                    "style": "bold",
                    "text": {
                        0: "Nombre",
                        1: "Motor de Base de Datos",
                        2: "Tamanio inicial",
                        3: "Modelo de crecimiento",
                        4: "Proyeccion",
                    }
                },
                2: {
                    "style": "bold",
                    "text": {
                        4: "1 anio",
                        5: "2 anios",
                    }
                },
            },
            "tbody": {
                3: {
                    "style": "normal",
                    "text": {
                        0: str(json["schema"]),
                        1: str(json["db_engine"]),
                        2: documento.bytesToMb(json["initial_size"]),
                        3: "FORMULA",
                        4: documento.bytesToMb(json["proyection"]["1y"]),
                        5: documento.bytesToMb(json["proyection"]["2y"])
                    }
                },
            },
            "merge": [
                {"a": [0, 0], "b": [0, 5]},

                {"a": [1, 0], "b": [2, 0]},
                {"a": [1, 1], "b": [2, 1]},
                {"a": [1, 2], "b": [2, 2]},
                {"a": [1, 3], "b": [2, 3]},

                {"a": [1, 4], "b": [1, 5]},
            ]
        }

        documento.createHeading("\n\t1.1 General\n")
        documento.createTable(json_gral_table)
        documento.createHeading("\n\t1.2 Espesificacion\n")

        json_espesification_table = {
            "rows": len(json["tables"])+1,
            "cols": 8,
            "thead": {  # Headers by rows
                0: {
                    "style": "bold",
                    "text": {
                        0: "Nombre Tabla",
                        1: "Numero Registros",
                        2: "Tamanio Registro",
                        3: "Tamanio Tabla",
                        4: "Tamanio indices",
                        5: "Tamanio total",
                        6: "Proyeccion a 1 ano",
                        7: "Proyeccion a 2 anos"
                    }
                }
            },
            "tbody": {}
        }
        t = 1 # Because thead is 0
        for json_table in json["tables"]:
            json_espesification_table["tbody"][t] = {
                "style": "normal",
                "text": {
                    0: str(json_table["name"]),
                    1: str(json_table["rows_count"]),
                    2: documento.bytesToMb(json_table["row_size"]),
                    3: documento.bytesToMb(json_table["table_size"]),
                    4: documento.bytesToMb(json_table["table_index"]),
                    5: documento.bytesToMb(json_table["total_size"]),
                    6: documento.bytesToMb(json_table["proyection"]["1y"]),
                    7: documento.bytesToMb(json_table["proyection"]["2y"])
                }
            }
            t += 1

        documento.createTable(json_espesification_table)
        # TODO - add parapraph
        documento.createHeading("\n2. Anexos: Estimar el tamanio de una base de datos\n")
        for json_table in json["tables"]:
            json_table_table = {
                "rows": 2 + len(json_table["rows"]) + 1,
                "cols": 3,
                "thead": {  # Headers by rows
                    0: {
                        "style": "center",
                        "text": {
                            0: str(json_table["name"])
                        }
                    },
                    1: {
                        "style": "bold",
                        "text": {
                            0: "Columna",
                            1: "Tipo",
                            2: "Tamanio en bytes"
                        }
                    }
                },
                "tbody": {},
                "merge": [
                    {"a": [0, 0], "b": [0, 2]},
                ]
            }
            r = 2
            for row in json_table["rows"]:
                json_table_table["tbody"][r] = {
                    "style": "normal",
                    "text": {
                        0: row["name"],
                        1: row["type"],
                        2: documento.bytesToMb(row["full_size"], True)
                    }
                }
                r += 1
            json_table_table["merge"].append({"a": [r, 0], "b": [r, 1]})
            json_table_table["tbody"][r] = {
                "style": "normal",
                "text": {
                    0: "Tamanio total en bytes:",
                    2: documento.bytesToMb(json_table["total_size_bytes"], True)
                }
            }

            string_dimen = "(  No Registros al anio) * " + str(json_table["total_size_bytes"]) + " = Dimensionamiento de crecimiento de Tabla"
            if input_enable == 1:
                year_rows = input("\tNumero de registros al año:")
                bytes_dimen = year_rows * json_table["total_size_bytes"]
                string_dimen = str(year_rows) + " * " + str(json_table["total_size_bytes"]) + " = " + bytesToMb(bytes_dimen, bytes_dimen, True, 1) + " = " + bytesToMb(bytes_dimen, True, 2)

            documento.createTable(json_table_table)
            documento.createParagraph("\n" + string_dimen + "\n")
        documento.save(self.output.replace("{schema}", json["schema"]))