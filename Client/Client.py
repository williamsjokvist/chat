import socket

class Client():
    def __init__(self):
        self.isSockConnected = False
        self.disconnect()
        self.pollFreq = 200
        self.appEncoding = 'UTF-8'  
    
    #Returns isSockConnected
    def connect(self, ipPort):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)
        
        try:
            self.socket.connect(ipPort)
            self.isSockConnected = True
            self.socket.settimeout(0)
        except socket.error:
            self.socket = None
            self.isSockConnected = False
        
        return self.isSockConnected
    
    def isConnected(self):
        return self.isSockConnected
    
    def disconnect(self):
        #Close socket if connected
        if self.isSockConnected:
            self.socket.close()
        
        self.isSockConnected = False
    
    #Returns data or false on socket.error
    def pollMessages(self):
        #Return if the socket is not connected
        if not self.isSockConnected:
            return
        
        try:
            msg = self.socket.recv(2048)
            return msg.decode(self.appEncoding)
        except socket.error as err:
            return False
    
    #Returns false on socket.error, true on msg sent
    def sendMessage(self, msg):
        #Return if the socket is not connected
        if not self.isSockConnected:
            return
        
        try:
            self.socket.sendall(bytearray(msg, self.appEncoding))
            return True
        except socket.error as err:
            print(err)
            #disconnect on socket.error
            self.disconnect()
            return False
