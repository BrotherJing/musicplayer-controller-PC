import serial
from tkinter import *
from tkinter.ttk import *

ser = serial.Serial('COM8',115200,timeout=0.5)
root = Tk()
root.geometry("400x400")
root.title('Music Player Panel')
lb = Listbox(root,width=400,height=200)
play = Button(root,text='Play')
pause = Button(root,text='Pause')
    
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
    play.bind('<Button-1>',playMusic)
    pause.bind('<Button-1>',pauseMusic)
    play.grid(row=0,column=0,sticky=W)
    pause.grid(row=1,column=0,sticky=W)
    lb.grid(row=2,column=0,sticky=W)
    #play.pack(side=LEFT)
    #pause.pack(side=RIGHT)
    #lb.pack(side=TOP)
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
    putStr('play '+item.split(' ')[1]+'\n')
    print(item.split(' ')[1])
    raw_str = getStrBlocking()
    print(raw_str)

def playMusic(event):
    putStr('res\n')

def pauseMusic(event):
    putStr('pau\n')

main()
