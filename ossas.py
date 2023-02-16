from tkinter import PhotoImage, Listbox, StringVar, Scrollbar, Button
import PIL
import customtkinter
from lecteur import lecteur

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("Light")
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
        self.__album_image = customtkinter.CTkImage(
            PIL.Image.open("assets/music.png"), size=(150, 150)
        )

        self.__play_status: bool = False
        self.__theme: str = "white"
        self.__activate_now: int = 0
        self.__scrolloff: int = 8

        self.__position = 0

        self.__pathMp3Dict: dict = lecteur.findMp3File()
        self.__all_mp3_title: list[str] = [key for key in self.__pathMp3Dict]

        self.__container = customtkinter.CTkFrame(self)

        self.__left_frame = customtkinter.CTkFrame(self.__container)

        self.__search_frame = customtkinter.CTkFrame(self.__left_frame)
        self.__search_entry = customtkinter.CTkEntry(
            self.__search_frame, placeholder_text="search"
        )
        self.__search_entry.pack(fill="x", side="left", expand=1)
        self.__search_frame.pack(fill="x", pady=5)
        self.__scrollbar = Scrollbar(self.__left_frame)
        self.__scrollbar.pack(side="left", fill="y")
        self.__music_listbox = Listbox(
            self.__left_frame,
            bg="white",
            fg="gray",
            height=80,
            width=60,
            selectbackground="black",
            selectforeground="white",
            yscrollcommand=self.__scrollbar.set,
        )
        self.__music_listbox.pack(fill="x")
        self.__scrollbar.config(command=self.__music_listbox.yview)

        # insert all title on listbox
        for music_title in self.__all_mp3_title:
            self.__music_listbox.insert("end", music_title)

        self.__left_frame.pack(pady=20, side="left", fill="y", padx=5)

        self.__right_frame = customtkinter.CTkFrame(self.__container)
        self.__titre_text = StringVar()
        self.__titre = customtkinter.CTkLabel(
            self.__right_frame, textvariable=self.__titre_text
        ).pack(pady=50)
        self.__image_music = customtkinter.CTkLabel(
            self.__right_frame, text="", image=self.__album_image
        )
        self.__image_music.pack()

        self.__right_frame_bottom = customtkinter.CTkFrame(self.__right_frame)
        self.__prev_button = Button(
            self.__right_frame_bottom,
            text=None,
            relief="groove",
            borderwidth=0,
            command=self.prev,
            image=self.__prev_image,
        ).pack(side="left")
        self.__play_button = Button(
            self.__right_frame_bottom,
            text=None,
            relief="groove",
            borderwidth=0,
            command=self.play,
            image=self.__play_image,
        )
        self.__play_button.pack(padx=10, side="left")
        self.__next_button = Button(
            self.__right_frame_bottom,
            text=None,
            relief="groove",
            borderwidth=0,
            command=self.next,
            image=self.__text_image,
        ).pack(side="left")
        self.__right_frame_bottom.pack(pady=20, side="bottom")

        self.__status = customtkinter.CTkFrame(self.__right_frame)
        self.scale = customtkinter.CTkSlider(
            self.__status, command=lambda x: (self.changePositon(x))
        )
        self.scale.pack(side="left", fill="x", ipadx=150)
        self.__status.pack(fill="x", side="bottom", ipady=2, padx=4)

        self.__right_frame.pack(side="right", fill="y", expand=1, padx=5)

        self.__container.pack(fill="y", anchor="sw")

        self.__music_listbox.bind("<Double-Button-1>", self.selectItemInListbox)
        self.__search_entry.bind("<KeyRelease>", self.search)

        self.playTime()

    def music_now(self, index) -> str:
        key = self.__music_listbox.get(index)
        return self.__pathMp3Dict[key]

    def upateTitleAndImage(self, index) -> None:
        titre, _, artist, image = lecteur.get_tags(self.music_now(index))

        if image is not None:
            with open(".tmp.jpg", "wb") as file:
                file.write(image)
            image = customtkinter.CTkImage(PIL.Image.open(".tmp.jpg"), size=(250, 230))
        else:
            image = self.__album_image 

        self.__image_music.configure(image=image)
        self.__titre_text.set(f"{titre} {artist}")

    def changePositon(self, position: float):
        lecteur.scrool(position)
        self.__position = position

    def playTime(self) -> None:
        # update scale postion
        if self.__play_status:
            self.__position += 1
            _, time_left = lecteur.getPosition()
            self.scale.set(self.__position)
            if time_left == "59:59":
                self.next()
        self.after(1000, self.playTime)

    def play(self, index: int | str = "active") -> None:
        self.__play_status = True
        total_len_music = len(self.__music_listbox.get(0, "end"))
        if index == total_len_music:
            index = 0
        sond = self.music_now(index)
        self.scale._to = lecteur.play(sond)
        self.scale.set(0)
        self.__position = 0
        self.__play_button.config(image=self.__pause_image, command=self.pause)
        self.__music_listbox.selection_clear(0, "end")
        self.__music_listbox.activate(index)
        self.__music_listbox.selection_set(index, last=None)
        self.__activate_now: int = self.__music_listbox.curselection()[0]
        self.__music_listbox.yview(
            "moveto", (self.__activate_now - self.__scrolloff) / total_len_music,
        )  # update yview
        self.upateTitleAndImage(self.__activate_now)

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
        self.__music_listbox.delete(0, "end")
        for result in data:
            self.__music_listbox.insert("end", result)

    def search(self, e: str) -> None:
        search_output = self.__search_entry.get()
        data = [
            title
            for title in self.__all_mp3_title
            if search_output.lower() in title.lower()
        ]
        self.updateMusicListbox(data)


if __name__ == "__main__":
    app = MusicPlayer()
    app.mainloop()
