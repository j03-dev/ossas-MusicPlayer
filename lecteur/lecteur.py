from os import path, walk
from mutagen.mp3 import MP3
import pygame
import eyed3
import time

pygame.mixer.init()

PLAY: bool = True


def get_tags(song_path: str) -> tuple:
    audio_file = eyed3.load(song_path)
    img = None
    if audio_file is not None:
        titre = audio_file.tag.title or "unknow"
        album_name = audio_file.tag.album or "unknow"
        artist_name = audio_file.tag.artist or "unknow"
        album_image = audio_file.tag.images
        for image in album_image:
            img = image.image_data
    else:
        titre = song_path.split("/")[-1].split(".")[0]
        album_name = "unknow"
        artist_name = "unknow"

    return (titre, album_name, artist_name, img)


def play(song_path: str) -> float:
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()
    audio = MP3(song_path)
    return audio.info.length


def scrool(postion: float) -> None:
    pygame.mixer.music.set_pos(postion)


def getPosition() -> tuple[float, str]:
    postion: float = pygame.mixer.music.get_pos() / 1000
    postion_as_time_format: str = time.strftime("%M:%S", time.gmtime(postion))
    return postion, postion_as_time_format


def pause() -> bool:
    global PLAY
    if PLAY:
        PLAY = False
        pygame.mixer.music.pause()
    else:
        PLAY = True
        pygame.mixer.music.unpause()
    return PLAY


def findMp3File(search_path: str = "/mnt/d/Music") -> dict:
    file_dict: dict = {}
    for root, dir, files in walk(search_path):
        for file in files:
            if ".mp3" in file:
                audio_file = path.join(root, file)
                titre, album, artist, _ = get_tags(audio_file)
                file_dict[f"{titre}, {album}, {artist}"] = audio_file
    return file_dict
