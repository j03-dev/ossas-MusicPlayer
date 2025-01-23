import eyed3
from os import path, walk


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


def find_audio_file(search_path: str) -> dict:
    file_dict: dict = {}
    for root, _, files in walk(search_path):
        for file in files:
            if ".mp3" in file:
                audio_file = path.join(root, file)
                titre, album, artist, _ = get_tags(audio_file)
                file_dict[f"{titre} {album} {artist}"] = audio_file
    return file_dict
