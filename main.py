import serial
from tkinter import *
from tkinter.ttk import *

ser = serial.Serial('COM8',115200,timeout=0.5)
root = Tk()
root.geometry("400x400")
root.title('Music Player Panel')
lb = Listbox(root,width=300,height=200)
    
def main():
    raw_str = ''
    song_list = []
    if not ser.isOpen():
        ser.open()
        
    #first, get the content of root directory.
    putStr('ls\n');
    raw_str = getStrBlocking()
    print(raw_str)

    #generate a list of directory entries
    song_list = raw_str.split('\r\n')
    for song in song_list:
        lb.insert(END,song)
    lb.bind('<Double-Button-1>',onListItemDoubleClick)
    lb.pack()
    root.mainloop()

def getStrBlocking():
    raw_str = ''
    started = False
    ended = False
    while not ended:
        data = ser.read()
        if data != b'':
            if not started:
                started = True
            #decode the raw bytes to string
            raw_str = raw_str + data.decode()
        else:
            if started:
                ended = True
    return raw_str

def putStr(raw_str):
    ser.write(raw_str.encode('ascii'))

def onListItemDoubleClick(event):
    item = lb.get(lb.curselection())
    if item[1] == 'F':
        switchSong(item)

def switchSong(item):
    putStr("play "+item.split(' ')[1]+"\n")
    print(item.split(' ')[1])
    raw_str = getStrBlocking()
    print(raw_str)

main()
