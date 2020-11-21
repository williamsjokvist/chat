import tkinter as tk
import tkinter.messagebox as tkmsgbox
import tkinter.scrolledtext as tksctxt

class View(tk.Frame):
    def __init__(self, _controller, master):
        self.controller = _controller
        super().__init__(master)
        
        master.title('BTD - Better Than Discord')
        # if attempt to close the window, handle it in the on-closing method
        master.protocol("WM_DELETE_WINDOW", self.controller.onClosing)
        self.pack()
        self.make_widgets()
    
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
        self.ipPortLbl = tk.Label(self.groupCon, text='IP:port', padx=10)
        self.ipPortLbl.pack(side="left")
        #
        self.ipPort = tk.Entry(self.groupCon, width=20)
        self.ipPort.insert(tk.END, 'localhost:60003')
        # if the focus is on this text field and you hit 'Enter',
        # it should (try to) connect
        self.ipPort.bind('<Return>', self.controller.connectHandler)
        self.ipPort.pack(side="left")
        #
        padder = tk.Label(self.groupCon, padx=5)
        padder.pack(side="left")
        #
        self.connectButton = tk.Button(self.groupCon, text='Connect',
            command = self.controller.connectButtonClick, width=10)
        self.connectButton.pack(side="left")
        #
        padder = tk.Label(self.groupCon, padx=1)
        padder.pack(side="left")
        #
        self.clearButton = tk.Button(self.groupCon, text='clr msg',
            command = self.clearMessages)
        self.clearButton.pack(side="left")

        
        #-------------------------------------------------------------------
        # row 2: the message field (chat messages + status messages)
        #-------------------------------------------------------------------
        self.msgText = tksctxt.ScrolledText(height=15, width=42,
            state=tk.DISABLED)
        self.msgText.pack(side="top")

    
        #-------------------------------------------------------------------
        # row 3: sending messages
        #-------------------------------------------------------------------
        self.groupSend = tk.LabelFrame(bd=0)
        self.groupSend.pack(side="top")
        #
        self.textInLbl = tk.Label(self.groupSend, text='message', padx=10)
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
        self.sendButton = tk.Button(self.groupSend, text = 'send',
            command = self.controller.sendButtonClick)
        self.sendButton.pack(side="left")
        
        
        # set the focus on the IP and Port text field
        self.ipPort.focus_set()
