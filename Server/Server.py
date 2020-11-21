import socket
from select import *

class Server():
    def __init__(self):
        self.appEncoding = 'UTF-8'
        self.isOnline = False
        self.pollFreq = 200
        self.socketList = []
    
    def getPort(self):
        return self.port
    
    def getPeers(self):
        peers = []
        for sock in self.socketList:
            if sock is not self.socket:
                peers.append(sock.getpeername())
        return peers
    
    #Returns isOnline
    def listen(self, _port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)
        self.port = int(_port)
        
        try:
            self.socket.bind(('0.0.0.0', self.port))
            self.socket.listen(1)
            self.isOnline = True
            self.socket.settimeout(0)
            self.socketList.append(self.socket)
        except socket.error:
            self.socket = None
            self.isOnline = False
        
        return self.isOnline
    
    def isListening(self):
        return self.isOnline
    
    def disconnectClients(self, clientId=None):
        if clientId is None:
            for sock in self.socketList:
                if sock is not self.socket:
                    sock.shutdown(1)
            self.socketList = [self.socket]
        else:
            sockC = self.getSocketFromClientId(clientId)
            sockC.shutdown(1)
            self.socketList.remove(sockC)
    
    def close(self):
        if self.isOnline == False:
            return

        self.disconnectClients()
        self.socket.close()
        self.socketList.remove(self.socket)
        self.isOnline = False
    
    #Returns data or false 
    def getData(self):
        readable, writable, error = select(self.socketList, [], [], 0)
        message = False
        
        for sock in readable:
            if sock is self.socket:
                (sockC, addr) = self.socket.accept()
                self.socketList.append(sockC)        

                message = "{} connected".format(sockC.getpeername())
            else:
                data = sock.recv(2048)
                peer = sock.getpeername()
                message = "{}: {}".format(peer, data.decode(self.appEncoding)) if data else "{} disconnected".format(peer)
                
                if not data:
                    sock.close()
                    self.socketList.remove(sock)
                        
        return message

    #Returns false on socket.error, true on msg sent
    def sendMessage(self, msg, toClient=None):
        didSend = False
        
        #Send to all if no socket was admitted
        if toClient == None:
            for sock in self.socketList:
                if sock is not self.socket:
                    sock.sendall(bytearray(msg, self.appEncoding))
                    didSend = True
        else:
            sockC = self.getSocketFromClientId(toClient)
            sockC.sendall(bytearray(msg, self.appEncoding))
            didSend = True
        
        return didSend

    def getSocketFromClientId(self, clientId):
        #get socket based on client index. +1 because client array does not contain
        #server socket like server.socketList does
        return self.socketList[clientId+1]
