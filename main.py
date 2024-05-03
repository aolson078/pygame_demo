import pygame
from static.sprites.sprites import *
from config import *
import sys

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
		self.clock = pygame.time.Clock()
		self.font = pygame.font.Font('Arial', 32)
		self.running = True

	def new(self):
		# new game starts
		self.playing = True

		self.all_sprites = pygame.sprite.LayeredUpdates()
		self.blocks = pygame.sprite.LayeredUpdates()
		self.enemies = pygame.sprite.LayeredUpdates()
		self.attacks = pygame.sprite.LayeredUpdates()

		self.player = Player(self, 1, 2)

	def events(self):
		pass

	def update(self):
		pass

	def draw(self):
		pass

	def main(self):
		# game loop
		while self.playing:
			self.events()
			self.update()
			self.draw()
		self.running = False

	def game_over(self):
		pass

	def intro_screen(self):
		pass