import pygame.mouse

from sprites import *
from config import *
import sys


class Game:
	def __init__(self):
		pygame.init()

		self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
		self.clock = pygame.time.Clock()
		self.running = True
		self.font = pygame.font.Font('arial.ttf', 32)
		self.camera = Camera(WORLD_WIDTH, WORLD_HEIGHT)

		self.character_spritesheet = Spritesheet("static/assets/img/character.png")
		self.terrain_spritesheet = Spritesheet("static/assets/img/terrain.png")
		self.enemy_spritesheet = Spritesheet("static/assets/img/enemy.png")
		self.attack_spritesheet = Spritesheet("static/assets/img/attack.png")
		self.intro_background = pygame.image.load("static/assets/img/introbackground.png")
		self.go_background = pygame.image.load("static/assets/img/gameover.png")


	def createTilemap(self):
		for i, row in enumerate(tilemap):
			for j, column in enumerate(row):
				# Add ground tiles to tilemap
				Ground(self, j + 50, i + 50)
				# Add blocks/walls to tilemap
				if column == "B":
					self.blocks.add(Block(self, j + 50, i + 50))
				# Add player to tilemap
				if column == "P":
					self.player = Player(self, j + 50, i + 50)
				# Add enemy to tilemap
				if column == "E":
					Enemy(self, j + 50, i + 50)

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

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					if self.player.facing == 'up':
						Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
					if self.player.facing == 'down':
						Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
					if self.player.facing == 'left':
						Attack(self, self.player.rect.x  - TILESIZE, self.player.rect.y)
					if self.player.facing == 'right':
						Attack(self, self.player.rect.x  + TILESIZE, self.player.rect.y)

			elif event.type == pygame.USEREVENT:
				self.player.turn_off_invincibility()

	def update(self):
		# game loop updates
		self.all_sprites.update()
		#self.player.update()
		self.camera.update(self.player)

	def draw(self):
		self.screen.fill(BLACK)
		for sprite in self.all_sprites:
			self.screen.blit(sprite.image, self.camera.apply(sprite))
		self.display_stats()
		self.clock.tick(FPS)
		pygame.display.update()

	def display_stats(self):
		# create surface for stat bar
		stats_surface = pygame.Surface((WIN_WIDTH, 50))
		stats_surface.fill((0,0,0))

		# render text
		text = self.font.render(f"Lvl {self.player.level}  Exp {self.player.exp}  HP {self.player.health} ${self.player.money}", True, WHITE)
		text_rect = text.get_rect(center=(WIN_WIDTH // 2, 25)) # centered horizontally, 25 px from top
		stats_surface.blit(text, text_rect)
		self.screen.blit(stats_surface, (0,0))

	def main(self):
		# game loop
		while self.playing:
			self.events()
			self.update()
			self.draw()

	def game_over(self):
		text = self.font.render("Game Over!", True, WHITE)
		text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))

		restart_button = Button(10, WIN_HEIGHT - 60, 120, 50, WHITE, BLACK, 'Restart', 32)

		for sprite in self.all_sprites:
			sprite.kill()

		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False

			mouse_pos = pygame.mouse.get_pos()
			mouse_pressed = pygame.mouse.get_pressed()

			if restart_button.is_pressed(mouse_pos, mouse_pressed):
				self.new()
				self.main()

			self.screen.blit(self.go_background, (0,0))
			self.screen.blit(text, text_rect)
			self.screen.blit(restart_button.image, restart_button.rect)
			self.clock.tick(FPS)
			pygame.display.update()

	def intro_screen(self):
		intro = True

		title = self.font.render("Alex and Hilda's awesome game!", True, BLACK)
		title_rect = title.get_rect(x=10, y=10)

		play_button = Button(10, 50, 100, 50, WHITE, BLACK, "Play", 32)

		while intro:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					intro = False
					self.running = False

			mouse_pos = pygame.mouse.get_pos()
			mouse_pressed = pygame.mouse.get_pressed()

			if play_button.is_pressed(mouse_pos, mouse_pressed):
				intro = False

			self.screen.blit(self.intro_background, (0,0))
			self.screen.blit(title, title_rect)
			self.screen.blit(play_button.image, play_button.rect)
			self.clock.tick(FPS)
			pygame.display.update()


class Camera:
	def __init__(self, width, height):
		self.camera = pygame.Rect(0, 0, width, height)
		self.width = width
		self.height = height

	def apply(self, entity):
		return entity.rect.move(self.camera.topleft)

	def update(self, target):
		x = -target.rect.centerx + int(WIN_WIDTH / 2)
		y = -target.rect.centery + int(WIN_HEIGHT / 2)

		# limit scrolling to map size
		x = min(0, x)  # left
		y = min(0, y)  # top
		x = max(-(self.width - WIN_WIDTH), x)  # right
		y = max(-(self.height - WIN_HEIGHT), y)  # bottom


		self.camera = pygame.Rect(x, y, self.width, self.height)

g = Game()
g.intro_screen()
g.new()
while g.running:
	g.main()
	g.game_over()

pygame.quit()
sys.exit()