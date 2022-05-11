from pydub import AudioSegment
from os import path, system, walk
import pygame
import time

pygame.mixer.init()

status = "Play"

def play(song_path):
	pygame.mixer.music.load(song_path)
	pygame.mixer.music.play()

def getPlayTime():
	return time.strftime("%M:%S", time.gmtime(pygame.mixer.music.get_pos() / 1000))

def pause():
	global status
	if status == "Play":
		status = "Pause"
		pygame.mixer.music.pause()
	else:
		status = "Play"
		pygame.mixer.music.unpause()
		

def findMp3File(search_path="/home/j03-dev/Music"):
	file_dict = {}
	for root, dir, files in walk(search_path):
		for file in files:
			if ".mp3" in file:
				file_dict[file[:-4]] = path.join(root, file)
	return file_dict
