from tkinter import (
    PhotoImage,
    Listbox,
    StringVar,
    Scrollbar,
    Button
)
import customtkinter
from lecteur import lecteur
import os

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")

class MusicPlayer(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("ossas Music player")
        self.geometry("1000x500")
        self.__titre_text = StringVar()
        self.__play_image = PhotoImage(file="assets/play-button.png")
        self.__pause_image = PhotoImage(file="assets/pause.png")
        self.__text_image = PhotoImage(file="assets/next.png")
        self.__prev_image = PhotoImage(file="assets/previous.png")
        self.__album_image = PhotoImage(file="assets/music.png")

        self.__play_status: bool = True
        self.__theme: str = "white"
        self.__duration: int = 0
        self.__activate_now: int = 0
        self.__scrolloff: int = 8

        self.__pathMp3Dict: dict = lecteur.findMp3File()
        self.__all_mp3_title: list[str] = [key for key in self.__pathMp3Dict]

        self.__container = customtkinter.CTkFrame(self)

        self.__left_frame = customtkinter.CTkFrame(self.__container)

        self.__search_Frame = customtkinter.CTkFrame(self.__left_frame)
        self.__search_Entry = customtkinter.CTkEntry(
            self.__search_Frame,
            placeholder_text="search"
        )
        self.__search_Entry.pack(fill='x', side='left', expand=1)
        self.__search_Frame.pack(fill='x')
        self.__scrollbar = Scrollbar(self.__left_frame)
        self.__scrollbar.pack(side='left', fill='y')
        self.__music_listbox = Listbox(
            self.__left_frame,
            bg='white',
            fg='gray',
            height=80,
            width=60,
            selectbackground='black',
            selectforeground='white',
            yscrollcommand=self.__scrollbar.set
        )
        self.__music_listbox.pack(fill='x')
        self.__scrollbar.config(command=self.__music_listbox.yview)

        # insert all title on listbox
        for music_title in self.__all_mp3_title:
            self.__music_listbox.insert('end', music_title)

        self.__left_frame.pack(pady= 20, side="left",fill="y", padx=5)

        self.__right_frame = customtkinter.CTkFrame(self.__container)
        self.__titre_text = StringVar()
        self.__titre = customtkinter.CTkLabel(self.__right_frame, textvariable=self.__titre_text).pack(pady=50)
        self.__image_music = customtkinter.CTkLabel(self.__right_frame, image=self.__album_image, width=500).pack()

        self.__right_frame_bottom = customtkinter.CTkFrame(self.__right_frame)
        self.__prev_button = Button(
                self.__right_frame_bottom,
                text=None ,
                relief='groove',
                borderwidth=0,
                command=self.prev,
                image=self.__prev_image
        )\
        .pack(side='left')
        self.__play_button = Button(
                self.__right_frame_bottom,
                text=None,
                relief='groove',
                borderwidth=0,
                command=self.play,
                image=self.__play_image
        )
        self.__play_button.pack(padx=10, side='left')
        self.__next_button = Button(
                self.__right_frame_bottom,
                text=None,
                relief='groove',
                borderwidth=0,
                command=self.next,
                image=self.__text_image
        )\
        .pack(side='left')
        self.__right_frame_bottom.pack(pady=20 ,side='bottom')

        self.__status = customtkinter.CTkFrame(self.__right_frame)
        self.scale = customtkinter.CTkSlider(self.__status, from_=0, to=1)
        self.scale.pack(side='left', fill='x', ipadx=150)
        self.__status.pack(fill='x', side='bottom', ipady=2, padx=4)

        self.__right_frame.pack(side="right", fill="y", expand=1, padx=5)

        self.__container.pack(fill='y', anchor="sw")

        self.__music_listbox.bind('<Double-Button-1>', self.selectItemInListbox)
        self.__search_Entry.bind('<KeyRelease>', self.search)

    def setTitle(self) -> None:
        self.__titre_text.set(self.__music_listbox.get('active'))

    def playTime(self) -> None:
        postion, time_left = lecteur.getPosition()
        tmp = self.scale.get()
        self.scale.set(postion)
        diff = abs(tmp - postion)
        if diff <= 3:
            self.after(1000, self.playTime)
            if time_left == "59:59":
                self.next()
        else:
            sond = self.__pathMp3Dict[self.__music_listbox.get(self.__activate_now)]
            lecteur.scrool(sond, self.scale.get())
            self.after(1000, self.playTime)

    def play(self, index: int|str ='active') -> None:
        try:
            sond = self.__pathMp3Dict[self.__music_listbox.get(index)]
        except:
            index = 0
            sond = self.__pathMp3Dict[self.__music_listbox.get(index)]
        self.__duration: float = lecteur.play(sond)
        self.scale.set(0)
        self.scale.to: float = self.__duration
        self.__play_button.config(image=self.__pause_image, command=self.pause)
        self.__music_listbox.selection_clear(0, 'end')
        self.__music_listbox.activate(index)
        self.__music_listbox.selection_set(index, last=None)
        self.__activate_now: int = self.__music_listbox.curselection()[0]
        self.__music_listbox.yview("moveto", (self.__activate_now - self.__scrolloff) / len(self.__music_listbox.get(0, 'end'))) # update yview 
        self.playTime()
        self.setTitle()

    def pause(self) -> None:
        if self.__play_status:
            self.__play_button.config(image=self.__play_image)
        else:
            self.__play_button.config(image=self.__pause_image)
        self.__play_status: bool = lecteur.pause()

    def next(self) -> None:
        self.__activate_now += 1
        self.play(self.__activate_now)

    def prev(self) -> None:
        self.__activate_now -= 1
        self.play(self.__activate_now)

    def selectItemInListbox(self, e: str) -> None:
        self.play()

    def updateMusicListbox(self, data: str) -> None:
        self.__music_listbox.delete(0, 'end')
        for result in data:
            self.__music_listbox.insert('end', result)

    def search(self, e: str) -> None:
        search_output = self.__search_Entry.get()
        data = [title for title in self.__all_mp3_title if search_output.lower() in title.lower()]
        self.updateMusicListbox(data)


if __name__ == "__main__":
    app = MusicPlayer()
    app.mainloop()
