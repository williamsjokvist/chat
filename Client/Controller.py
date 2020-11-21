from View import *
from Client import *

class Controller():
    def __init__(self, _root):
        self.client = Client()
        self.root = _root
        
        # reschedule the next polling event
        self.jobId = self.root.after(self.client.pollFreq, self.pollMessages)
        
        self.view = View(self, self.root)
        
    def connectButtonClick(self):
        self.connectHandler()
    
    def sendButtonClick(self):
        self.sendMessage()

    def connectHandler(self, event=None):
        connected = False
        if self.client.isConnected():
            self.client.disconnect()
            connected = False
        else:
            ipPort = self.getStringAddressTuple(self.view.ipPort.get())            
            connected = self.client.connect(ipPort)
            if not connected:
                self.view.printToMessages('Could not connect to server')
        
        #Change btn text
        self.view.connectButton['text'] = 'Disconnect' if connected else 'Connect'
            
    def sendMessage(self, event=None):
        if not self.client.isConnected():
            self.view.printToMessages('Not connected to a server')
            return
        
        didSendMsg = self.client.sendMessage(self.view.textIn.get())
        
        #Clear textinput if succesful
        if didSendMsg:
            self.view.clearMessageInput()
        else:
            self.view.printToMessages('Message could not be sent')

    # if attempt to close the window, it is handled here
    def onClosing(self):
        if self.client.isConnected():
            if self.view.showAskWindow("Quit",
                "You are still connected. If you quit you will be"
                + " disconnected."):
                self.quit()
        else:
            self.quit()

    # when quitting, do it the nice way    
    def quit(self):
        self.client.disconnect()
        #destroy job
        self.root.after_cancel(self.jobId)
        #destroy gui
        self.root.destroy()

    # utility address formatting
    def formatAddressToString(self,addr):
        return '{}:{}'.format(addr[0], addr[1])    

    #Converts ip:port string to (ip,port) tuple
    def getStringAddressTuple(self,addr):
        arr = addr.split(':')
        return (arr[0], int(arr[1]))

    def pollMessages(self):
        # reschedule the next polling event
        self.jobId = self.root.after(self.client.pollFreq, self.pollMessages)
        
        #print message
        message = self.client.pollMessages()
        if message:
            self.view.printToMessages(message)
