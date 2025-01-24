import tkinter as tk
import customtkinter as ctk

from mutagen.mp3 import MP3
from osas import osas
from enum import Enum
from PIL import Image

import utils

config = utils.read_config(".config")

# Modes: "System" (standard), "Dark", "Light"
ctk.set_appearance_mode(config["mode"])
ctk.set_default_color_theme(config["theme"])


class State(Enum):
    Stop = 0
    Play = 1
    Pause = 2


class Application(ctk.CTk):
    w = 1000
    h = 500
    status = State.Stop
    theme: str = "white"
    current_music_index: int = 0
    scrolloff: int = 8

    player = osas.Player()

    def __init__(self) -> None:
        super().__init__()
        self.title("ossas Music player")
        self.geometry(f"{self.w}x{self.h}")
        self.music_title_var = tk.StringVar()

        self.music_library = utils.find_audio_file(config["path"])
        self.titles: list[str] = [key for key in self.music_library]

        self.play_img = tk.PhotoImage(file="assets/play-button.png")
        self.pause_img = tk.PhotoImage(file="assets/pause.png")
        self.next_img = tk.PhotoImage(file="assets/next.png")
        self.prev_img = tk.PhotoImage(file="assets/previous.png")
        self.default_cover_img = ctk.CTkImage(
            Image.open("assets/music.png"),
            size=(150, 150),
        )

        self.container = ctk.CTkFrame(self)

        self.left = ctk.CTkFrame(self.container)

        self.search_container = ctk.CTkFrame(self.left)
        self.search_entry = ctk.CTkEntry(
            self.search_container, placeholder_text="search"
        )
        self.search_entry.pack(fill="x", side="left", expand=1)
        self.search_container.pack(fill="x", pady=5)

        self.scrollbar = ctk.CTkScrollbar(self.left)
        self.scrollbar.pack(side="left", fill="y")

        self.playlist = tk.Listbox(
            self.left,
            bg="white",
            fg="gray",
            height=80,
            width=60,
            selectbackground="black",
            selectforeground="white",
            yscrollcommand=self.scrollbar.set,
        )
        self.playlist.pack(fill="x")

        self.scrollbar.configure(command=self.playlist.yview)

        # insert all title on listbox
        for music_title in self.titles:
            self.playlist.insert("end", music_title)

        self.left.pack(pady=20, side="left", fill="y", padx=5)

        self.rigth = ctk.CTkFrame(self.container)
        ctk.CTkLabel(
            self.rigth,
            textvariable=self.music_title_var,
        ).pack(pady=50)

        self.cover = ctk.CTkLabel(
            self.rigth,
            text="",
            image=self.default_cover_img,
        )
        self.cover.pack()

        self.right_bottom = ctk.CTkFrame(self.rigth)

        self.center_right_bottom = ctk.CTkFrame(self.right_bottom)

        tk.Button(
            self.center_right_bottom,
            text=None,
            relief="groove",
            borderwidth=0,
            command=self.prev,
            image=self.prev_img,
        ).pack(side="left")

        self.play_btn = tk.Button(
            self.center_right_bottom,
            text="",
            relief="groove",
            borderwidth=0,
            command=self.play,
            image=self.play_img,
        )
        self.play_btn.pack(padx=10, side="left")

        tk.Button(
            self.center_right_bottom,
            text="",
            relief="groove",
            borderwidth=0,
            command=self.next,
            image=self.next_img,
        ).pack(side="left")

        self.center_right_bottom.pack(anchor="center")

        self.right_bottom.pack(side="bottom", pady=10)

        self.scale = ctk.CTkSlider(
            self.rigth, command=lambda x: (self.change_position(x))
        )
        self.scale.pack(side="bottom", fill="x", ipadx=150, pady=10)

        self.rigth.pack(side="right", fill="y", expand=1, padx=5)

        self.container.pack(fill="y", anchor="sw")

        self.playlist.bind("<Double-Button-1>", self.select_playlist)
        self.search_entry.bind("<KeyRelease>", self.search)

        self.play_time()

    def get_current_music_path(self, index) -> str:
        key = self.playlist.get(index)
        return self.music_library[key]

    def update_title_and_cover(self, index) -> None:
        titre, _, artist, image = utils.get_tags(
            self.get_current_music_path(index),
        )

        if image is not None:
            with open(".tmp.jpg", "wb") as file:
                file.write(image)
            image = ctk.CTkImage(
                Image.open(".tmp.jpg"),
                size=(250, 230),
            )
        else:
            image = self.default_cover_img

        self.cover.configure(image=image)
        self.music_title_var.set(f"{titre} {artist}")

    def change_position(self, position: float):
        self.player.seek(int(position * 1000))

    def play_time(self) -> None:
        if self.status is State.Play:
            position = self.player.get_pos() / 1000
            self.scale.set(position)
            if round(position) >= round(self.scale._to):
                self.next()
        self.after(1000, self.play_time)

    def play(self, index: int | str = "active") -> None:
        self.status = State.Play
        playlist_length = len(self.playlist.get(0, "end"))

        if isinstance(index, int):
            index %= playlist_length

        music_path = self.get_current_music_path(index)

        self.player.stop()
        self.player.play(music_path)

        self.scale._to = MP3(music_path).info.length
        self.scale.set(0)

        self.play_btn.config(image=self.pause_img, command=self.pause)

        self.playlist.selection_clear(0, "end")
        self.playlist.activate(index)
        self.playlist.selection_set(index, last=None)

        self.current_music_index: int = self.playlist.curselection()[0]
        yview = (self.current_music_index - self.scrolloff) / playlist_length
        self.playlist.yview("moveto", yview)

        self.update_title_and_cover(self.current_music_index)

    def pause(self) -> None:
        if self.status is State.Play:
            self.play_btn.config(image=self.play_img)
        elif self.status is State.Pause:
            self.play_btn.config(image=self.pause_img)
        self.player.pause()
        self.status = State.Pause if self.player.is_paused() else State.Play

    def next(self) -> None:
        self.current_music_index += 1
        self.play(self.current_music_index)

    def prev(self) -> None:
        self.current_music_index -= 1
        self.play(self.current_music_index)

    def select_playlist(self, _x) -> None:
        self.play()

    def update_music_listbox(self, data: list[str]) -> None:
        self.playlist.delete(0, "end")
        for result in data:
            self.playlist.insert("end", result)

    def search(self, e: str) -> None:
        output = self.search_entry.get()
        search_result = [
            title for title in self.titles if output.lower() in title.lower()
        ]
        self.update_music_listbox(search_result)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
