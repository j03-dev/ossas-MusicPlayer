from pydub import AudioSegment
from os import path, system
import pygame
import time
#from mutagen.mp3 import MP3

pygame.mixer.init()

cache_file = 'lecteur/.cache/song_tmp.wav'
status = "Play"

def play(song_path):
	'''
	1- verifier si le fichier exist et le supprimer
	2- convertire le fichier mp3 en wav
	3- metre sur play
	'''
	# mp3 = AudioSegment.from_mp3(song_path)
	# if path.exists(cache_file):
	# 	system(f'rm {cache_file}')
	# mp3.export(cache_file, format='wav')
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
		
