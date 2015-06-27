from socket import *
from tkinter import *
from os.path import join, getsize
import os.path
import tkinter.filedialog as filedialog
import time

class TCPClient:
    HEAD = "CMD "
    END = " END"
    PORT = 80
    BUFSIZE = 1024
    def __init__(self):
        self.HOST = input("please import host ip:")
        self.ADDR = (self.HOST,self.PORT)
        self.client = socket(AF_INET,SOCK_STREAM)
        self.client.settimeout(5)
        self.client.connect(self.ADDR)

        self.file_opt = options = {}
        options['defaultextension']='.wav'
        options['filetypes']=[('wav files','.wav'),('all files,''.*')]

        self.root = Tk()
        self.cmd_text = StringVar()
        self.fpath_text = StringVar()
        Entry(self.root,textvariable=self.cmd_text).pack()
        Entry(self.root,textvariable=self.fpath_text).pack()
        Button(self.root,text='send command',command=self.sendcommand).pack()
        Button(self.root,text='open file',command=self.askopenfile).pack()
        Button(self.root,text='send file',command=self.sendfile).pack()
        self.root.mainloop()

    def str2cmd(self,str0):
        return self.HEAD+str0+self.END

    def askopenfile(self):
        self.filename = filedialog.askopenfilename(**self.file_opt)
        self.fpath_text.set(self.filename)

    def sendfile(self):
        filesize = getsize(self.filename)
        print(self.filename+', size is '+str(filesize))
        fp = open(self.filename,'rb')
        name = os.path.basename(self.filename)
        self.sendcmd('file '+str(filesize)+'/'+name,False)
        while True:
            filedata = fp.read(self.BUFSIZE)
            if not filedata:
                break
            self.client.send(filedata)
            time.sleep(0.05)
        print('finish')
        fp.close()

    def sendcmd(self,cmd,isReceive):
        print(cmd)
        self.client.send(self.str2cmd(cmd).encode('ascii'))
        if not isReceive:
            return
        try:
            data = self.client.recv(self.BUFSIZE)
        except:
            print('no return data')
        if data:
            print(data.decode('ascii'))

    def sendcommand(self):
        self.sendcmd(self.cmd_text.get(),False)

if __name__ == '__main__':
    client = TCPClient()
        
