from discord import Message

class Message:

    DEBUG = False

    def __init__(self, message: Message, clsName: str = "Unknown"):
        self.data = message
        self.initClsName = clsName
        self.run()
    
    def run(self):
        self.on_message()

    def toggleDebug(self):
        Message.Debug != Message.Debug

    def isDebug(self):
        return Message.DEBUG
    
    def on_message(self):
        if(Message.DEBUG): print('New message found, triggered by {}'.format(self.initClsName))

    def getData(self):
        return self.data