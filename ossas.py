from tkinter import Tk
from tkinter import (
    Entry,
    PhotoImage, 
    StringVar, Listbox, 
    Scrollbar
)
import customtkinter
from lecteur.lecteur import play, pause, getPlayTime, findMp3File
import os

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")

class MusicPlayer(customtkinter.CTk):
    def __init__(self):
        super().__init__()
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

        self.__activate_now = 0
        
        self.__pathMp3Dict = findMp3File()
        self.__all_mp3_title = [key for key in self.__pathMp3Dict]
        
        self.__container = customtkinter.CTkFrame(self)

        self.__left_frame = customtkinter.CTkFrame(self.__container)
        
        self.__search_Frame = customtkinter.CTkFrame(self.__left_frame)
        self.__search_Entry = customtkinter.CTkEntry(self.__search_Frame, placeholder_text="search")
        self.__search_Entry.pack(fill='x', side='left', expand=1)
        self.__search_Frame.pack(fill='x')
        self.__scrollbar = Scrollbar(self.__left_frame)
        self.__scrollbar.pack(side='left', fill='y')
        self.__music_listbox = Listbox(self.__left_frame, bg='white', fg='gray', height=80, width=60, selectbackground='black', selectforeground='white', yscrollcommand=self.__scrollbar.set)
        self.__music_listbox.pack(fill='x')
        self.__scrollbar.config(command=self.__music_listbox.yview)
        
        #insert all title on listbox
        for music_title in self.__all_mp3_title:
            self.__music_listbox.insert('end', music_title)
        
        self.__left_frame.pack(pady= 20, side="left",fill="y", padx=5)

        self.__right_frame = customtkinter.CTkFrame(self.__container)
        self.__titre_text = StringVar()
        self.__titre = customtkinter.CTkLabel(self.__right_frame, textvariable=self.__titre_text).pack(pady=50)
        self.__image_music = customtkinter.CTkLabel(self.__right_frame, image=self.__album_image, width=500).pack()

        self.__right_frame_bottom = customtkinter.CTkFrame(self.__right_frame)
        self.__prev_button = customtkinter.CTkButton(
                self.__right_frame_bottom,
                text=None ,
                relief='groove',
                borderwidth=0,
                fg_color=("gray70", "gray50"),
                command=self.__prev,
                image=self.__prev_image
        )\
        .pack(side='left')
        self.__play_button = customtkinter.CTkButton(
                self.__right_frame_bottom,
                text=None,
                relief='groove',
                borderwidth=0,
                fg_color=("gray70", "gray50"),
                command=self.__play, 
                image=self.__play_image
        )
        self.__play_button.pack(padx=10, side='left')
        self.__next_button = customtkinter.CTkButton(
                self.__right_frame_bottom,
                text=None,
                relief='groove',
                borderwidth=0,
                command=self.__next, 
                fg_color=("gray70", "gray50"),
                image=self.__text_image
        )\
        .pack(side='left')
        self.__right_frame_bottom.pack(pady=20 ,side='bottom')

        self.__status = customtkinter.CTkFrame(self.__right_frame)
        self.scale = customtkinter.CTkSlider(self.__status)
        self.scale.pack(side='left', fill='x', ipadx=150)
        self.__status.pack(fill='x', side='bottom', ipady=2, padx=4)

        self.__right_frame.pack(side="right", fill="y", expand=1, padx=5)
        
        self.__container.pack(fill='y', anchor="sw")

        self.__music_listbox.bind('<Double-Button-1>', self.__selectItemInListbox)
        self.__search_Entry.bind('<KeyRelease>', self.__search)

    def __loadMusic(self, start=0):
        self.__playlist = self.__music_listbox.get(start, 'end')
        self.__new_playlist = [self.__pathMp3Dict[key] for key in self.__pathMp3Dict if key in self.__playlist]
        return self.__new_playlist

    def __playTime(self):
        time_left = getPlayTime()
        self.after(1000, self.__playTime)
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
            sond = self.__pathMp3Dict[self.__music_listbox.get(index)]
        except:
            index = 0
            sond = self.__pathMp3Dict[self.__music_listbox.get(index)]
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
