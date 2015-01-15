from .proxy import MonnitProxy



class Network(object):
    def __init__(self, proxy, name, networkid=None):
        self.proxy = proxy
        self.networkid = networkid
        self.name = name


    def create(self, name):
        response = self.proxy.execute("CreateNetwork2", name=self.name)

    def save(self):
        if self.networkid is None:
            #create new entry
            response = self.proxy.execute("CreateNetwork2", name=self.name)