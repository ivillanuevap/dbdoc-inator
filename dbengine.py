import mysql.connector
class Dbengine:
    connector = None
    db_engine = 'mysql'
    schema = None

    def __init__(self, db_engine, host, user, password, database):
        self.db_engine = db_engine
        self.schema = database
        if db_engine == 'mysql':
            self.connector = self.mysqlconnection(host, user, password, database)

    def mysqlconnection(self, host, user, password, database):
        return mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
    def getTables(self):
        mycursor = self.connector.cursor()
        mycursor.execute("SHOW TABLES")
        return mycursor.fetchall()
    def getFk(self, schema, table):
        mycursor = self.connector.cursor()
        sql = "SELECT TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE CONSTRAINT_SCHEMA = '" + schema + "' AND TABLE_NAME = '" + table + "' AND REFERENCED_COLUMN_NAME IS NOT NULL"
        mycursor.execute(sql)
        return mycursor.fetchall()
    def getSizeTable(self, table):
        cursor =  self.connector.cursor()
        sql = "SELECT ROUND(DATA_LENGTH + INDEX_LENGTH) AS Size, TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA = '" + self.schema + "' AND TABLE_NAME = '" + table + "' ORDER BY (DATA_LENGTH + INDEX_LENGTH)"
        cursor.execute(sql)
        result = cursor.fetchone()
        return result[0]

    def getTotalRows(self, table):
        cursor = self.connector.cursor()
        sql = "SELECT COUNT(*)  FROM " + table
        cursor.execute(sql)
        result = cursor.fetchone()
        return result[0]
    def getDescripcionTable(self, table):
        var_return = {
            'size': 0,
            'columns': {}
        }
        cursor = self.connector.cursor()
        cursor.execute("DESCRIBE " + table)
        describe = cursor.fetchall()
        for d in describe:
            #0,1,3 se usa para proy
            field = d[0]
            type = d[1]
            full_type = d[1]
            size = ''
            null = d[2]
            key = d[3]
            default = str(d[4])
            auto_increment = d[5]
            primary_key, foreign_key = '', ''
            if null == 'YES':
                null = 'SI'
            if default == 'None':
                default = ''
            if auto_increment == 'auto_increment':
                auto_increment = 'SI'
            type_indexof = type.find('(')
            if type_indexof > 0:
                type_indexof_end = type.find(')')
                size = type[type_indexof + 1:type_indexof_end]
                type = type[0:type_indexof]
            if key == 'PRI':
                primary_key = 'PK'
                index_table_field = field
                index_table_type = type
            elif key == 'MUL':
                foreign_key = 'FK'

            var_return['columns'][str(field)] = {
                'full_type': full_type,
                'type': type,
                'full_size': self.getTableDimension(table, field),
                'size': size,
                'null': null,
                'primary_key': primary_key,
                'foreign_key': foreign_key,
                'default': default,
                'auto_increment': auto_increment
            }
            if key != '':
                var_return['size'] += 16
        return var_return

    def getTableDimension(self, table, column,):
        # TODO - revisar esta mamada
        cursor = self.connector.cursor()
        cursor.execute("SELECT sum(char_length(" + column + ")) FROM " + table + "")
        result = cursor.fetchone()
        return result[0]