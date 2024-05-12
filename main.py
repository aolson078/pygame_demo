from sprites import *
from config import *
import sys

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
		self.clock = pygame.time.Clock()
		self.running = True

		self.character_spritesheet = Spritesheet('static/assets/img/character.png')
		self.terrain_spritesheet = Spritesheet('static/assets/img/terrain.png')
		self.enemy_spritesheet = Spritesheet('static/assets/img/enemy.png')

	def createTilemap(self):
		for i, row in enumerate(tilemap):
			for j, column in enumerate(row):
				# Add ground tiles to tilemap
				Ground(self, j, i)
				# Add blocks/walls to tilemap
				if column == "B":
					self.blocks.add(Block(self, j, i))
				# Add player to tilemap
				if column == "P":
					Player(self, j, i)
				# Add enemy to tilemap
				if column == "E":
					Enemy(self, j, i)


	def new(self):
		# new game starts
		self.playing = True

		self.all_sprites = pygame.sprite.LayeredUpdates()
		self.blocks = pygame.sprite.LayeredUpdates()
		self.enemies = pygame.sprite.LayeredUpdates()
		self.attacks = pygame.sprite.LayeredUpdates()

		self.createTilemap()


	def events(self):
		# game loop events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.playing = False
				self.running = False

	def update(self):
		# game loop updates
		self.all_sprites.update()

	def draw(self):
		self.screen.fill(BLACK)
		self.all_sprites.draw(self.screen)
		self.clock.tick(FPS)
		pygame.display.update()

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


g = Game()
g.intro_screen()
g.new()
while g.running:
	g.main()
	g.game_over()

pygame.quit()
sys.exit()