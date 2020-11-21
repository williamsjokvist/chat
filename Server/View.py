import tkinter as tk
import tkinter.messagebox as tkmsgbox
import tkinter.scrolledtext as tksctxt

class View(tk.Frame):
    def __init__(self, _controller, master):
        self.controller = _controller
        super().__init__(master)
        
        master.title('BTD - Better Than Discord Server')
        # if attempt to close the window, handle it in the on-closing method
        master.protocol("WM_DELETE_WINDOW", self.controller.onClosing)
        self.pack()
        self.make_widgets()
            
    def updateClientList(self, clientList):
        #delete all of it
        self.clientBox.configure(state=tk.NORMAL)

        self.clientBox.delete(0, tk.END)
        print(clientList)

        for client in clientList:
            self.clientBox.insert(tk.END, client)
        
        self.clientBox.see(tk.END)
    
    def deleteSelectedClient(self):
        self.controller.disconnectClientBtnClicked(int(self.clientBox.curselection()[0]))
        self.clientBox.delete(tk.ANCHOR)
    
    def sendMessageToSelectedClient(self):
        #Do try catch IndexError in case no selection
        self.controller.sendBtnClicked(int(self.clientBox.curselection()[0]))
    
    def clearMessages(self):
        self.msgText.configure(state=tk.NORMAL)
        self.msgText.delete(1.0, tk.END)
        self.msgText.see(tk.END)
        self.msgText.configure(state=tk.DISABLED)
    
    def clearMessageInput(self):
        self.textIn.delete(0, tk.END)
    
    def printToMessages(self, message):
        self.msgText.configure(state=tk.NORMAL)
        self.msgText.insert(tk.END, message + '\n')
        # scroll to the end, so the new message is visible at the bottom
        self.msgText.see(tk.END)
        self.msgText.configure(state=tk.DISABLED)
    
    def showAskWindow(self, title, msg):
        return tkmsgbox.askokcancel(title, msg)
    
    def make_widgets(self):
        
        #-------------------------------------------------------------------
        # row 1: connection stuff (and a clear-messages button)
        #-------------------------------------------------------------------
        self.groupCon = tk.LabelFrame(bd=0)
        self.groupCon.pack(side="top")
        #
        self.ipPortLbl = tk.Label(self.groupCon, text='Port', padx=10)
        self.ipPortLbl.pack(side="left")
        #
        self.port = tk.Entry(self.groupCon, width=20)
        self.port.insert(tk.END, '60003')
        # if the focus is on this text field and you hit 'Enter',
        # it should (try to) connect
        self.port.bind('<Return>', self.controller.listenHandler)
        self.port.pack(side="left")
        #
        padder = tk.Label(self.groupCon, padx=5)
        padder.pack(side="left")
        #
        self.listenBtn = tk.Button(self.groupCon, text='Listen',
            command = self.controller.listenBtnClicked, width=10)
        self.listenBtn.pack(side="left")
        #
        padder = tk.Label(self.groupCon, padx=1)
        padder.pack(side="left")
        #
        self.clsBtn = tk.Button(self.groupCon, text='Clear Activity Monitor',
            command = self.clearMessages)
        self.clsBtn.pack(side="left")

        
        #-------------------------------------------------------------------
        # row 2: the message field (chat messages + status messages)
        #-------------------------------------------------------------------
        tk.Label(text='Activity Monitor', padx=10).pack(side="top")

        self.msgText = tksctxt.ScrolledText(height=15, width=75,
            state=tk.DISABLED)
        self.msgText.pack(side="top")


        
        #-------------------------------------------------------------------
        # row 3: dcing clients
        #-------------------------------------------------------------------
        self.groupdc = tk.LabelFrame(bd=0)
        self.groupdc.pack(side="top")
        
        tk.Label(self.groupdc, text='Connected Clients', padx=10).pack(side="top")
        
        self.clientBox = tk.Listbox(self.groupdc, height=5, width=75)
        self.clientBox.pack(side="top")
        
        self.dcBtn = tk.Button(self.groupdc, text='Disconnect Selected Client',
            command = self.deleteSelectedClient)
        self.dcBtn.pack(side="right")
        
        self.dcAllBtn = tk.Button(self.groupdc, text='Disconnect All',
            command = self.controller.disconnectClientHandler)
        self.dcAllBtn.pack(side="right")
        
        #-------------------------------------------------------------------
        # row 4: sending messages
        #-------------------------------------------------------------------
        self.groupSend = tk.LabelFrame(bd=0)
        self.groupSend.pack(side="top")
        #
        self.textInLbl = tk.Label(self.groupSend, text='Message', padx=10)
        self.textInLbl.pack(side="left")
        #
        self.textIn = tk.Entry(self.groupSend, width=38)
        # if the focus is on this text field and you hit 'Enter',
        # it should (try to) send
        self.textIn.bind('<Return>', self.controller.sendMessage)
        self.textIn.pack(side="left")
        #
        padder = tk.Label(self.groupSend, padx=5)
        padder.pack(side="left")
        #
        
        self.sendBtn = tk.Button(self.groupSend, text = 'Send To Selected',
            command = self.sendMessageToSelectedClient)
        self.sendBtn.pack(side="right")
        
        self.sendAllBtn = tk.Button(self.groupSend, text = 'Send To All',
            command = self.controller.sendToAllBtnClicked)
        self.sendAllBtn.pack(side="right")
        
        # set the focus on the IP and Port text field
        self.port.focus_set()
