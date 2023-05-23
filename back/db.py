from datetime import timedelta

from couchdb.client import Server

class Database:

    def __init__(self, host, username, password, name):
        self.host = host
        self.username = username
        self.password = password
        self.name = name

        self.inst = None
        self.db = None

    def connect(self):
        self.inst = Server(f'http://{self.username}:{self.password}@{self.host}:5984/')
        if self.inst[self.name]:
            self.db = self.inst[self.name]
        else:
            self.db = self.inst.create(self.name)

    def write(self, json):
        self.db.save(json)

    def read(self):
        return self.db.view('_all_docs', include_docs=True)
