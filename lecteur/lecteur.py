import time
from os import path, walk
from osas.osas import Player

import eyed3
from mutagen.mp3 import MP3

player = Player()


def read_config(conf: str = "../.config") -> dict:
    config = {}
    with open(conf, "r") as config_file:
        for c in config_file.readlines():
            key, value = c.strip("\n").split("=")
            config[key.strip(" ")] = value.strip(" ")
    return config


def get_tags(song_path: str) -> tuple:
    audio_file = eyed3.load(song_path)
    img = None
    try:
        titre = audio_file.tag.title or "unknown"
        album_name = audio_file.tag.album or "unknown"
        artist_name = audio_file.tag.artist or "unknown"
        album_image = audio_file.tag.images
        for image in album_image:
            img = image.image_data
    except Exception:
        titre = song_path.split("/")[-1].split(".")[0]
        album_name = "unknown"
        artist_name = "unknown"

    return titre, album_name, artist_name, img


def play(song_path: str) -> float:
    player.stop()
    player.play(song_path)
    audio = MP3(song_path)
    return audio.info.length


def set_position(position: float) -> None:
    player.seek(int(position * 1000))


def get_position() -> tuple[float, str]:
    position: float = player.get_pos() / 1000
    position_as_time_format: str = time.strftime(
        "%M:%S",
        time.gmtime(position),
    )
    return position, position_as_time_format


def pause() -> bool:
    player.pause()
    return player.is_paused()


def find_audio_file(search_path: str) -> dict:
    file_dict: dict = {}
    for root, _, files in walk(search_path):
        for file in files:
            if ".mp3" in file:
                audio_file = path.join(root, file)
                titre, album, artist, _ = get_tags(audio_file)
                file_dict[f"{titre} {album} {artist}"] = audio_file
    return file_dict
