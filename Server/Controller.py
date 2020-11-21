from View import *
from Server import *

class Controller():
    def __init__(self, _root):
        self.server = Server()
        self.root = _root
        self.view = View(self, self.root)
        self.jobId = None
        
    def listenBtnClicked(self):
        self.listenHandler()
    
    def sendBtnClicked(self, indexOfClient):
        self.sendMessage(toClient=indexOfClient)

    def sendToAllBtnClicked(self):
        self.sendMessage()
    
    def disconnectClientBtnClicked(self, indexOfClient):
        self.disconnectClientHandler(client=indexOfClient)
    
    def disconnectClientHandler(self, client=None):
        self.server.disconnectClients(clientId=client if client is not None else None)
        
        if self.server.isListening:
            self.view.printToMessages('All clients have been disconnected' if client is None else 'Client has been disconnected')
        
        self.updateClientListView()
        
    def updateClientListView(self):
        self.view.updateClientList(self.server.getPeers())

    def listenHandler(self, event=None):
        listening = False
        printMessage = ''
        if self.server.isListening():
            self.server.close()
            listening = False
            printMessage = 'Stopped listening on port {}'.format(self.server.getPort())
        else:
            port = self.view.port.get()
            listening = self.server.listen(int(port))            
            printMessage = 'Listening on port {}'.format(port) if listening else 'Port is already in use' 
        
        #Change btn text
        self.view.listenBtn['text'] = 'Close' if listening else 'Listen'
        self.view.printToMessages(printMessage)
        
        if listening:
            # reschedule the next polling event
            self.jobId = self.root.after(self.server.pollFreq, self.pollMessages)
            
    def sendMessage(self, event=None, toClient=None):
        if not self.server.isListening():
            self.view.printToMessages('The server is not listening for connections')
            return
        
        didSendMsg = self.server.sendMessage('(Server): '+self.view.textIn.get(), toClient=toClient)
        
        #Clear textinput if succesful
        if didSendMsg:
            self.view.clearMessageInput()
        else:
            self.view.printToMessages('Message could not be sent')

    # if attempt to close the window, it is handled here
    def onClosing(self):
        if self.server.isListening():
            if self.view.showAskWindow("Quit",
                "The server is still online, if you quit it will be disconnected"):
                self.quit()
        else:
            self.quit()

    def quit(self):
        self.server.close()
        #destroy job
        if self.jobId is not None:
            self.root.after_cancel(self.jobId)
        #destroy gui
        self.root.destroy()

    def pollMessages(self):
        if not self.server.isListening():
            return
        
        # reschedule the next polling event
        self.jobId = self.root.after(self.server.pollFreq, self.pollMessages)
        #print message
        message = self.server.getData()
        if message:
            self.view.printToMessages(message)
            self.server.sendMessage(message)
            self.updateClientListView()
            
# utility address formatting
def formatAddressToString(addr):
    return '{}:{}'.format(addr[0], addr[1])    

#Converts ip:port string to (ip,port) tuple
def getStringAddressTuple(addr):
    arr = addr.split(':')
    return (arr[0], int(arr[1]))
