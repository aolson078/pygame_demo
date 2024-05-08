import pygame
from pygame_demo.config import *
import math
import random

class Spritesheet:
	def __init__(self, file):
		self.sheet = pygame.image.load(file).convert()

	def get_sprite(self, x, y, width, height):
		sprite = pygame.Surface([width, height])
		sprite.blit(self.sheet, (0,0), (x, y, width, height))
		sprite.set_colorkey(BLACK)
		return sprite

class Player(pygame.sprite.Sprite):
	def __init__(self, game, x, y):

		self.game = game
		self._layer = PLAYER_LAYER
		self.groups = self.game.all_sprites
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.x = x * TILESIZE
		self.y = y * TILESIZE
		self.width = TILESIZE
		self.height = TILESIZE

		self.x_change = 0
		self.y_change = 0

		self.facing = 'down'

		# image_to_load = pygame.image.load('static/assets/images/alien.png')
		# self.image = image_to_load
		# self.image = pygame.transform.scale(image_to_load, (self.width, self.height))
		# self.image.set_colorkey(BLACK)


		self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)

		image_to_load = pygame.image.load('static/assets/img/single.png')
		self.image = image_to_load
		self.image.set_colorkey(BLACK)
		self.image.blit(image_to_load, (0,0))
		self.image = pygame.transform.scale(image_to_load, (self.width, self.height))


		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

	def update(self):
		self.movement()

		self.rect.x += self.x_change
		self.rect.y += self.y_change

		self.x_change = 0
		self.y_change = 0

	def movement(self):
		# get list of every key pressed
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			self.x_change -= PLAYER_SPEED
			self.facing = 'left'
		if keys[pygame.K_RIGHT]:
			self.x_change += PLAYER_SPEED
			self.facing = 'right'
		if keys[pygame.K_UP]:
			self.y_change -= PLAYER_SPEED
			self.facing = 'up'
		if keys[pygame.K_DOWN]:
			self.y_change += PLAYER_SPEED
			self.facing = 'down'


class Block(pygame.sprite.Sprite):
	def __init__(self, game, x, y):
		self.game = game
		self._layer = BLOCK_LAYER
		self.groups = self.game.all_sprites
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.x = x * TILESIZE
		self.y = y * TILESIZE
		self.width = TILESIZE
		self.height = TILESIZE

		# EVERY SPRITE NEEDS A RECT (hitbox) AND AN IMAGE -------------------------------------------------------

		self.image = self.game.terrain_spritesheet.get_sprite(960, 448, self.width, self.height)

		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y


class Ground(pygame.sprite.Sprite):
	def __init__(self, game, x, y):
		self.game = game
		self._layer = GROUND_LAYER
		self.groups = self.game.all_sprites
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.x = x * TILESIZE
		self.y = y * TILESIZE
		self.width = TILESIZE
		self.height = TILESIZE

		self.image = self.game.terrain_spritesheet.get_sprite(64, 352, self.width, self.height)

		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y