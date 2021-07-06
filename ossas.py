from tkinter import Tk
from tkinter import Label, Entry, Button, Frame, PhotoImage, StringVar, Listbox, Scale, Scrollbar
from lecteur.lecteur import play, pause, getPlayTime
import os


class MusicPlayer(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("ossas Music player")
        self.geometry("1000x500")
        self.__titre_text = StringVar()
        self.__directory = None
        self.__play_image = PhotoImage(file="assets/play-button.png")
        self.__pause_image = PhotoImage(file="assets/pause.png")
        self.__text_image = PhotoImage(file="assets/next.png")
        self.__prev_image = PhotoImage(file="assets/previous.png")
        self.__album_image = PhotoImage(file="assets/music.png")
        self.__play_status = True
        self.__theme = "white"

        self.__font = ('Comic Sans MS', 11, 'bold')
        self.__activate_now = 0
        
        self.__dictionary = {}
        self.__directory = "/d/Music"
        self.__mp3_path = [music[:-1] for music in os.popen(f'find {self.__directory} | grep mp3').readlines()]
        self.__all_mp3_title = [title.split('/')[-1] for title in self.__mp3_path]
        for i in range(len(self.__all_mp3_title)):
            self.__dictionary[self.__all_mp3_title[i]] = self.__mp3_path[i]
        
        self.__container = Frame(self, bg=self.__theme)

        self.__left_frame = Frame(self.__container, bg=self.__theme)
        
        self.__search_Frame = Frame(self.__left_frame, bg=self.__theme)
        self.__search_Entry = Entry(self.__search_Frame, width=70)
        self.__search_Entry.pack(fill='x', side='left')
        self.__search_Frame.pack(fill='x')
        self.__scrollbar = Scrollbar(self.__left_frame)
        self.__scrollbar.pack(side='left', fill='y')
        self.__music_listbox = Listbox(self.__left_frame, bg='white', fg='gray', font=self.__font, height=80, width=60, selectbackground='black', selectforeground='white', yscrollcommand=self.__scrollbar.set)
        self.__music_listbox.pack(fill='x')
        self.__scrollbar.config(command=self.__music_listbox.yview)
        
        #insert all title on listbox
        for music_title in self.__all_mp3_title:
            self.__music_listbox.insert('end', music_title)
        
        self.__left_frame.pack(pady= 20, side="left",fill="y", expand=1, padx=5)

        self.__right_frame = Frame(self.__container, bg=self.__theme)
        
        self.__right_frame_top = Frame(self.__right_frame, bg=self.__theme)
        self.__titre_text = StringVar()
        self.__titre = Label(self.__right_frame_top, bg=self.__theme, font=self.__font, textvariable=self.__titre_text).pack(pady=50)
        self.__image_music = Label(self.__right_frame_top, bg=self.__theme, image=self.__album_image, width=500).pack()
        self.__right_frame_top.pack(fill='x', side='top')


        self.__right_frame_bottom = Frame(self.__right_frame, bg=self.__theme)
        self.__prev_button = Button(self.__right_frame_bottom, relief='groove', borderwidth=0, bg=self.__theme,command=self.__prev, image=self.__prev_image).pack(side='left')
        self.__play_button = Button(self.__right_frame_bottom, relief='groove', borderwidth=0, bg=self.__theme, command=self.__play, image=self.__play_image)
        self.__play_button.pack(padx=10, side='left')
        self.__next_button = Button(self.__right_frame_bottom, relief='groove', borderwidth=0, bg=self.__theme, command=self.__next, image=self.__text_image).pack(side='left')
        self.__right_frame_bottom.pack(pady=20 ,side='bottom')

        self.__status = Frame(self.__right_frame, bg=self.__theme)
        # self.scale = Scale(self.__right_frame, from_=0, to=100, orient='horizontal', length=360)
        # self.scale.pack(side='left')
        self.__show_music_time = Label(self.__right_frame, bg=self.__theme, font=self.__font, text='', bd=1, relief=None, anchor='e')
        self.__show_music_time.pack(side='right')
        self.__status.pack(fill='x', side='bottom', ipady=2)

        self.__right_frame.pack(side="right", fill="y", expand=1, padx=5)
        
        self.__container.pack(fill='x')

        self.__music_listbox.bind('<Double-Button-1>', self.__selectItemInListbox)
        self.__search_Entry.bind('<KeyRelease>', self.__search)

    def __loadMusic(self, start=0):
        self.__playlist = self.__music_listbox.get(start, 'end')
        self.__new_playlist = [self.__dictionary[key] for key in self.__dictionary if key in self.__playlist]
        return self.__new_playlist

    def __playTime(self):
        time_left = getPlayTime()
        self.__show_music_time.config(text=time_left)
        self.__show_music_time.after(1000, self.__playTime)
        if time_left == "59:59":
            self.__next()

    def __next(self):
        self.__activate_now = self.__activate_now + 1
        self.__play(self.__activate_now)
    
    def __prev(self):    
        self.__activate_now = self.__activate_now - 1
        self.__play(self.__activate_now)

    def __play(self, index='active'):
        try:
            sond = self.__dictionary[self.__music_listbox.get(index)]
        except:
            index = 0
            sond = self.__dictionary[self.__music_listbox.get(index)]
        play(sond)      
        self.__play_button.config(command=self.__pause, image=self.__pause_image)      
        self.__music_listbox.selection_clear(0, 'end')
        self.__music_listbox.activate(index)
        self.__music_listbox.selection_set(index, last=None)
        self.__activate_now = self.__music_listbox.curselection()[0]
        self.__playTime()
        self.__setTitle()

    def __setTitle(self):
        self.__titre_text.set(self.__music_listbox.get('active'))

    def __pause(self):
        if self.__play_status:
            self.__play_status = False
            self.__play_button.config(image=self.__play_image)
        else:
            self.__play_status = True
            self.__play_button.config(image=self.__pause_image)
        pause()

    def __search(self, e):
        __input = self.__search_Entry.get()
        data = [title for title in self.__all_mp3_title if __input.lower() in title.lower()]
        self.__updateMusicListbox(data)

    def __updateMusicListbox(self, data):
        self.__music_listbox.delete(0, 'end')
        for result in data:
            self.__music_listbox.insert('end', result)

    def __selectItemInListbox(self, e):
        self.__play()

    
app = MusicPlayer()
app.mainloop()
