from os import path, system, walk
from mutagen.mp3 import MP3
import pygame
import time

pygame.mixer.init()

PLAY: bool = True


def play(song_path: str) -> float:
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()
    audio = MP3(song_path)
    return audio.info.length


def scrool(song_path: str, postion: float) -> None:
    play(song_path)
    postion *= 1000
    print("postion", postion)
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
        for title in files:
            if ".mp3" in title:
                file_dict[title[:-4]] = path.join(root, title)
    return file_dict
