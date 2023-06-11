class Server:
    
    __slots__ = ['instance']

    def __init__(self, client):
        self.instance = client

    def getInstance(self):
        return self.instance