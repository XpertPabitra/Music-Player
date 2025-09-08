from tkinter import *
from PIL import Image, ImageTk
import os
import time
import tkinter.messagebox
from tkinter import filedialog
from pygame import mixer
from mutagen.mp3 import MP3

mixer.init()

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title('Music Player')
        self.root.geometry('700x400')
        self.root.resizable(0, 0)
        self.root.configure(background='white')

        self.paused = False
        self.filename = None

        # ----------------- Menu -----------------
        def open_file():
            self.filename = filedialog.askopenfilename()
            if self.filename:
                self.filelabel['text'] = "Selected: " + os.path.basename(self.filename)

        def about():
            tkinter.messagebox.showinfo('About Us', 'Music Player Created By Dradcoder')

        self.menubar = Menu(self.root)
        self.root.configure(menu=self.menubar)

        file_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Open', command=open_file)
        file_menu.add_command(label='Exit', command=self.root.destroy)

        help_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Help', menu=help_menu)
        help_menu.add_command(label='About', command=about)

        # ----------------- Labels -----------------
        self.filelabel = Label(text='Select And Play', bg='black', fg='white', font=22)
        self.filelabel.place(x=5, y=30)

        self.label1 = Label(self.root, text='Let’s Play It.', bg='black', fg='white', font=20)
        self.label1.pack(side=BOTTOM, fill=X)

        self.lengthbar = Label(self.root, text='Total_Length:-00:00', font=20, bg='black', fg='white')
        self.lengthbar.place(x=5, y=270)

        # ----------------- Functions -----------------
        def playmusic():
            if not self.filename:
                tkinter.messagebox.showerror('Error', 'Please select a file first.')
                return

            if self.paused:
                mixer.music.unpause()
                self.paused = False
                self.label1['text'] = "Music Playing..."
            else:
                mixer.music.load(self.filename)
                mixer.music.play()
                self.label1['text'] = "Music Playing..."
                length_bar()

        def pausemusic():
            self.paused = True
            mixer.music.pause()
            self.label1['text'] = "Music Paused"

        def stopmusic():
            mixer.music.stop()
            self.label1['text'] = "Music Stopped"

        def length_bar():
            current_time = mixer.music.get_pos() / 1000
            convert_current_time = time.strftime('%M:%S', time.gmtime(current_time))
            song_mut = MP3(self.filename)
            song_length = song_mut.info.length
            convert_song_length = time.strftime('%M:%S', time.gmtime(song_length))
            self.lengthbar.config(text=f'Play: {convert_current_time} / {convert_song_length}')
            self.lengthbar.after(1000, length_bar)

        def volume_(vol):
            volume = int(vol) / 100
            mixer.music.set_volume(volume)

        # ----------------- Buttons -----------------
        Button(self.root, text="Play", command=playmusic).place(x=5, y=300)
        Button(self.root, text="Pause", command=pausemusic).place(x=85, y=300)
        Button(self.root, text="Stop", command=stopmusic).place(x=165, y=300)

        self.scale = Scale(self.root, from_=0, to=100, bg='cyan',
                           orient=HORIZONTAL, length=120, command=volume_)
        self.scale.set(30)
        self.scale.place(x=330, y=290)


root = Tk()
obj = MusicPlayer(root)
root.mainloop()
