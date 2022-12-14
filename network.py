import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.hostname=socket.gethostname()   
        self.server = "192.168.43.164"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.player = self.connect() # player 1 or 2

    def getPlayer(self):
        return self.player

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            rcv = self.client.recv(2048*5)
            return pickle.loads(rcv)
        except socket.error as e:
            print(e)

    def recv(self):
        try:
            data=self.client.recv(2048*5)
            return pickle.loads(data)
        except socket.error as e:
            print(e)