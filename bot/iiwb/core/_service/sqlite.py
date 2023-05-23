import sqlite3
import json
from iiwb.core import utils

class SqliteService:
    
    __slots__ = [
        'name',
        'instance',
        'dbpath',
        'dbfullpath',
        'env'
    ]

    def __init__(self, dbname = None, dbpath = None):
        """Initialize SQLITE service

        Args:
            dbname (str, optional): Database name. Defaults to None.
            dbpath (str, optional): Database path. Defaults to None.
        """
        self.env = self.getEnvSqlite()
        self.name = self.env['dbname']
        if(dbname is not None):
            self.name = dbname
        self.dbpath = self.env['dbpath']
        self.dbfullpath = '{}{}'.format(self.dbpath, self.name)
        self.instance = sqlite3.connect(self.dbfullpath)

    def _execute(self, operation: str, parameters = []):
        cursor = self.instance.execute(operation, parameters)
        return cursor

    def _commit(self):
        self.instance.commit()
    
    @staticmethod
    def _fetchAll(cursor):
        records = cursor.fetchall()
        return records

    @staticmethod
    def tableToList(cursor) -> list:
        record = SqliteService._fetchAll(cursor)
        return [item for t in record for item in t]

    def createTable(self, tableName: str, configuration: str):
        """Create sqlite Table if it doesn't already exists

        Args:
            tableName (str): Table name
            configuration (str): Columns and the type of data
        """
        sql = "CREATE TABLE IF NOT EXISTS {} ({})".format(tableName, configuration)
        self._execute(sql)

    def listTable(self):
        sql = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        cursor = self._execute(sql)
        return cursor

    def isTableExist(self, name: str):
        record = self._fetchAll(self.listTable())
        if(name in record):
            return True
        return False
    
    def _escape(self, string: str) -> str:
        return json.dumps(string)
    
    def _joinList(self, col: list) -> list:
        for i, v in enumerate(col):
            col[i] = json.dumps(v)
        return col


    def insertion(self, table: str, columns: list, insertValues: list, ignore: bool = True):
        if(ignore):
            sql_pre = "INSERT OR IGNORE INTO"
        else:
            sql_pre = "INSERT INTO"
        _columns = ", ".join(self._joinList(columns))
        _values = ", ".join(self._joinList(insertValues))
        sql = "{} {} ({}) VALUES ({})".format(sql_pre, table, _columns, _values)
        print(sql + _columns + _values)
        cursor = self._execute(sql)
        self._commit()
        return cursor

    def getEnvSqlite(self):
        return utils.load_backend()['sqlite']

    def getDBName(self):
        return self.name
    
    def getInstance(self):
        return self.instance

    def getDBFullpath(self):
        return self.dbfullpath
    
    def getDBPath(self):
        return self.dbpath

#CODE EXAMPLE
""" 	self.db = SqliteService("Roleplay.db")
	self.c = self.db.instance.execute('''CREATE TABLE IF NOT EXISTS quests 
			(id INTEGER PRIMARY KEY, name TEXT, description TEXT, reward INTEGER)''')
	self.db.instance.commit() """