from tkinter import PhotoImage, Listbox, StringVar, Button as Btn

import customtkinter
from PIL import Image

from lecteur import lecteur

config = lecteur.read_config(".config")

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode(config["mode"])
customtkinter.set_default_color_theme(config["theme"])


class MusicPlayer(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("osas player")
        self.geometry("1000x500")
        self.__titre_text = StringVar()
        self.__play_image = PhotoImage(file="assets/play-button.png")
        self.__pause_image = PhotoImage(file="assets/pause.png")
        self.__text_image = PhotoImage(file="assets/next.png")
        self.__prev_image = PhotoImage(file="assets/previous.png")

        self.__album_image = customtkinter.CTkImage(
            Image.open("assets/music.png"), size=(150, 150)
        )

        self.__play_status: bool = False
        self.__theme: str = "white"
        self.__activate_now: int = 0
        self.__scrolloff: int = 8

        self.__pathMp3Dict: dict = lecteur.find_audio_file(config["path"])
        self.__all_mp3_title: list[str] = [key for key in self.__pathMp3Dict]

        self.__container = customtkinter.CTkFrame(self)

        self.__left_frame = customtkinter.CTkFrame(self.__container)

        self.__search_frame = customtkinter.CTkFrame(self.__left_frame)
        self.__search_entry = customtkinter.CTkEntry(
            self.__search_frame, placeholder_text="search"
        )
        self.__search_entry.pack(fill="x", side="left", expand=1)
        self.__search_frame.pack(fill="x", pady=5)
        self.__scrollbar = customtkinter.CTkScrollbar(self.__left_frame)
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
        self.__scrollbar.configure(command=self.__music_listbox.yview)

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

        self.__frame_center_button = customtkinter.CTkFrame(
            self.__right_frame_bottom,
        )
        Btn(
            self.__frame_center_button,
            text=None,
            relief="groove",
            borderwidth=0,
            command=self.prev,
            image=self.__prev_image,
        ).pack(side="left")
        self.__play_button = Btn(
            self.__frame_center_button,
            text="",
            relief="groove",
            borderwidth=0,
            command=self.play,
            image=self.__play_image,
        )
        self.__play_button.pack(padx=10, side="left")
        Btn(
            self.__frame_center_button,
            text="",
            relief="groove",
            borderwidth=0,
            command=self.next,
            image=self.__text_image,
        ).pack(side="left")

        self.__frame_center_button.pack(anchor="center")

        self.__right_frame_bottom.pack(side="bottom", pady=10)

        self.scale = customtkinter.CTkSlider(
            self.__right_frame, command=lambda x: (self.change_position(x))
        )
        self.scale.pack(side="bottom", fill="x", ipadx=150, pady=10)

        self.__right_frame.pack(side="right", fill="y", expand=1, padx=5)

        self.__container.pack(fill="y", anchor="sw")

        self.__music_listbox.bind(
            "<Double-Button-1>", lambda x: self.select_item_in_listbox(x)
        )
        self.__search_entry.bind("<KeyRelease>", self.search)

        self.play_time()

    def music_now(self, index) -> str:
        key = self.__music_listbox.get(index)
        return self.__pathMp3Dict[key]

    def update_title_and_image(self, index) -> None:
        titre, _, artist, image = lecteur.get_tags(self.music_now(index))

        if image is not None:
            with open(".tmp.jpg", "wb") as file:
                file.write(image)
            image = customtkinter.CTkImage(
                Image.open(".tmp.jpg"),
                size=(250, 230),
            )
        else:
            image = self.__album_image

        self.__image_music.configure(image=image)
        self.__titre_text.set(f"{titre} {artist}")

    def change_position(self, position: float):
        lecteur.set_position(position)

    def play_time(self) -> None:
        # update scale postion
        if self.__play_status:
            position, time_left = lecteur.get_position()
            self.scale.set(position)
            if time_left == "59:59":
                self.next()
        self.after(1000, self.play_time)

    def play(self, index: int | str = "active") -> None:
        self.__play_status = True
        total_len_music = len(self.__music_listbox.get(0, "end"))
        if index == total_len_music:
            index = 0
        song = self.music_now(index)
        self.scale._to = lecteur.play(song)
        self.scale.set(0)
        self.__play_button.config(image=self.__pause_image, command=self.pause)
        self.__music_listbox.selection_clear(0, "end")
        self.__music_listbox.activate(index)
        self.__music_listbox.selection_set(index, last=None)
        self.__activate_now: int = self.__music_listbox.curselection()[0]
        self.__music_listbox.yview(
            "moveto",
            (self.__activate_now - self.__scrolloff) / total_len_music,
        )  # update yview
        self.update_title_and_image(self.__activate_now)

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

    def select_item_in_listbox(self, e: str) -> None:
        self.play()

    def update_music_listbox(self, data: list[str]) -> None:
        self.__music_listbox.delete(0, "end")
        for result in data:
            self.__music_listbox.insert("end", result)

    def search(self, e: str) -> None:
        search_output = self.__search_entry.get()
        search_result = [
            title
            for title in self.__all_mp3_title
            if search_output.lower() in title.lower()
        ]
        self.update_music_listbox(search_result)


if __name__ == "__main__":
    app = MusicPlayer()
    app.mainloop()
