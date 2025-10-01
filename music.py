from tkinter import *
from PIL import Image, ImageTk
import os
import time
import tkinter.messagebox
from tkinter import filedialog
from pygame import mixer
from mutagen.mp3 import MP3  # for song length

mixer.init()

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        
        # Title
        self.root.title('Music_Player')
        
        # Width and Height
        self.root.geometry('700x400')
        
        # resizable window off
        self.root.resizable(0, 0)

        # Background color
        self.root.configure(background='white')

        # -------- Menu --------
        def Openfile():
            global filename
            filename = filedialog.askopenfilename()

        self.menubar = Menu(self.root)
        self.root.configure(menu=self.menubar)

        self.submenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='File', menu=self.submenu)
        self.submenu.add_command(label='Open', command=Openfile)
        self.submenu.add_command(label='Exit', command=self.root.destroy)

        def About():
            tkinter.messagebox.showinfo('About Us', 'Music Player Created By Dradcoder')

        self.submenu2 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Help', menu=self.submenu2)
        self.submenu2.add_command(label='About', command=About)

        # -------- File Label --------
        self.filelabel = Label(text='Select And Play', bg='black', fg='white', font=22)
        self.filelabel.place(x=5, y=30)

        def songinf():
            self.filelabel['text'] = 'Current Music :- ' + os.path.basename(filename)

        # -------- Images --------
        self.L_photo = ImageTk.PhotoImage(file='leftsideimage.jpg')
        Label(self.root, image=self.L_photo).place(x=260, y=80, width=500, height=250)

        self.photo = ImageTk.PhotoImage(file='mainimg.png')
        Label(self.root, image=self.photo, bg='white').place(x=5, y=60)

        # -------- Bottom Label --------
        self.label1 = Label(self.root, text='Lets Play It.', bg='black', fg='white', font=20)
        self.label1.pack(side=BOTTOM, fill=X)

        # -------- Functions --------
        def playmusic():
            try:
                paused
            except NameError:
                try:
                    mixer.music.load(filename)
                    mixer.music.play()
                    self.label1['text'] = 'Music Playing..'
                    songinf()
                    length_bar()

                    self.im1 = ImageTk.PhotoImage(file='10.jpeg')
                    self.im2 = ImageTk.PhotoImage(file='11.jpeg')
                    self.im3 = ImageTk.PhotoImage(file='12.jpeg')
                    self.im4 = ImageTk.PhotoImage(file='13.jpeg')

                    self.imglabel = Label(self.root, bg='white')
                    self.imglabel.place(x=5, y=60)

                    animation()

                except:
                    tkinter.messagebox.showerror('Error', 'File Could Not Be Found, Please Try Again...')
            else:
                mixer.music.unpause()
                self.label1['text'] = 'Music Playing..'
                animation()

        def length_bar():
            current_time = mixer.music.get_pos() / 1000
            convert_current_time = time.strftime('%M:%S', time.gmtime(current_time))

            song_mut = MP3(filename)
            song_mut_length = song_mut.info.length
            convert_song_mut_length = time.strftime('%M:%S', time.gmtime(song_mut_length))

            self.lengthbar.config(text=f'Total_Length: {convert_current_time}/{convert_song_mut_length}')
            self.lengthbar.after(1000, length_bar)

        # -------- Length Label --------
        self.lengthbar = Label(self.root, text='Total_Length: 00:00/00:00', font=20, bg='black', fg='white')
        self.lengthbar.place(x=5, y=270)

        # -------- Buttons --------
        self.photo_B1 = ImageTk.PhotoImage(file='3.jpeg')
        Button(self.root, image=self.photo_B1, bd=0, bg='white', command=playmusic).place(x=5, y=300)

        def pausemusic():
            global paused
            paused = True
            mixer.music.pause()
            self.label1['text'] = 'Music Paused'
            self.photo = ImageTk.PhotoImage(file='mainimg.png')
            Label(self.root, image=self.photo, bg='white').place(x=5, y=60)

        self.photo_B2 = ImageTk.PhotoImage(file='4.jpeg')
        Button(self.root, image=self.photo_B2, bd=0, bg='white', command=pausemusic).place(x=85, y=300)

        def stopmusic():
            mixer.music.stop()
            self.label1['text'] = 'Music Stopped'
            self.photo = ImageTk.PhotoImage(file='mainimg.png')
            Label(self.root, image=self.photo, bg='white').place(x=5, y=60)

        self.photo_B3 = ImageTk.PhotoImage(file='5.jpeg')
        Button(self.root, image=self.photo_B3, bd=0, bg='white', command=stopmusic).place(x=165, y=300)

        # -------- Animation --------
        def animation():
            self.im1, self.im2, self.im3, self.im4 = self.im2, self.im3, self.im4, self.im1
            self.imglabel.config(image=self.im1)
            self.imglabel.after(3000, animation)

        # -------- Volume --------
        def mute():
            self.scale.set(0)
            self.mute = ImageTk.PhotoImage(file='mute.jpeg')
            Button(self.root, image=self.mute, command=unmute, bg='white', bd=0).place(x=280, y=290)
            self.label1['text'] = 'Music Muted'

        def unmute():
            self.scale.set(30)
            self.volimg = ImageTk.PhotoImage(file='6.jpeg')
            Button(self.root, image=self.volimg, command=mute, bg='white', bd=0).place(x=280, y=290)
            self.label1['text'] = 'Music Playing'

        self.volimg = ImageTk.PhotoImage(file='6.jpeg')
        Button(self.root, image=self.volimg, command=mute, bg='white', bd=0).place(x=280, y=290)

        def volume_(vol):
            volume = int(vol) / 100
            mixer.music.set_volume(volume)

        self.scale = Scale(self.root, from_=0, to=100, bg='cyan',
                           orient=HORIZONTAL, length=120, command=volume_)
        self.scale.set(30)
        self.scale.place(x=330, y=290)


# -------- Main --------
root = Tk()
obj = MusicPlayer(root)
root.mainloop()
