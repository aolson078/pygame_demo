import pygame
import sys
import random
from sprites import *
from config import *

class Game:
	def __init__(self):
		self.player = None
		pygame.init()
		self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
		self.clock = pygame.time.Clock()
		self.running = True
		self.font = pygame.font.Font(None, 32)  # Use default font
		self.camera = Camera(WORLD_WIDTH, WORLD_HEIGHT)
		self.load_assets()
		self.tilemap = self.generate_tilemap(MAP_HEIGHT, MAP_WIDTH)
		self.enemy_timers = {}

		self.is_paused = False
		self.is_playing = False

	def run(self):
		self.is_playing = True
		while self.is_playing:
			self.events()
			if not self.is_paused:
				self.update()
			self.draw()
			self.clock.tick(FPS)  # Limit the frame rate

	def load_assets(self):
		self.character_spritesheet = Spritesheet("static/assets/img/character.png")
		self.terrain_spritesheet = Spritesheet("static/assets/img/terrain.png")
		self.enemy_spritesheet = Spritesheet("static/assets/img/enemy.png")
		self.attack_spritesheet = Spritesheet("static/assets/img/attack.png")
		self.intro_background = pygame.image.load("static/assets/img/introbackground.png")
		self.go_background = pygame.image.load("static/assets/img/gameover.png")

	def generate_tilemap(self, height, width):
		tilemap = [['.' for _ in range(width)] for _ in range(height)]
		for i in range(width):
			tilemap[0][i] = 'B'
			tilemap[height - 1][i] = 'B'
		for i in range(height):
			tilemap[i][0] = 'B'
			tilemap[i][width - 1] = 'B'
		for _ in range(NUM_EXTRA_BLOCKS):
			while True:
				x, y = random.randint(1, width - 2), random.randint(1, height - 2)
				if tilemap[y][x] == '.':
					tilemap[y][x] = 'B'
					break

		num_remaining_enemies = NUM_INITIAL_ENEMIES
		while num_remaining_enemies > 0:
			x, y = random.randint(1, width - 2), random.randint(1, height - 2)
			if tilemap[y][x] == '.':
				tilemap[y][x] = 'E'
				num_remaining_enemies -= 1

		while True:
			x, y = random.randint(1, width - 2), random.randint(1, height - 2)
			if tilemap[y][x] == '.':
				tilemap[y][x] = 'P'
				break

		print("Generated tilemap:")
		for row in tilemap:
			print(" ".join(row))
		return tilemap

	def create_tilemap(self):
		for i, row in enumerate(self.tilemap):
			for j, column in enumerate(row):
				Ground(self, j * TILESIZE, i * TILESIZE)
				if column == "B":
					Block(self, j * TILESIZE, i * TILESIZE)
				if column == "P":
					self.player = Player(self, j * TILESIZE, i * TILESIZE)
				if column == "E":
					Enemy(self, j * TILESIZE, i * TILESIZE)

	def new(self):
		self.is_playing = True
		self.all_sprites = pygame.sprite.LayeredUpdates()
		self.blocks = pygame.sprite.LayeredUpdates()
		self.enemies = pygame.sprite.LayeredUpdates()
		self.attacks = pygame.sprite.LayeredUpdates()
		self.ground = pygame.sprite.LayeredUpdates()  # Initialize ground sprite group
		self.create_tilemap()
		self.camera.update(self.player)  # Center the camera on the player

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.is_playing = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					self.is_paused = not self.is_paused
				elif event.key == pygame.K_ESCAPE:
					self.is_playing = False
				if event.key == pygame.K_SPACE:
					if self.player:
						if self.player.facing == 'up':
							Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
						if self.player.facing == 'down':
							Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
						if self.player.facing == 'left':
							Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y)
						if self.player.facing == 'right':
							Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y)

			if event.type >= pygame.USEREVENT and event.type in self.enemy_timers:
				self.enemy_timers[event.type].turn_off_invincibility()
			elif event.type >= pygame.USEREVENT:
				if self.player:
					self.player.turn_off_invincibility()

	def update(self):
		if not self.is_paused:
			self.all_sprites.update()
			if self.player:
				self.camera.update(self.player)

	def draw(self):
		self.screen.fill(BLACK)
		for sprite in self.ground:
			if self.camera.apply(sprite).colliderect(self.screen.get_rect()):
				self.screen.blit(sprite.image, self.camera.apply(sprite))
		for sprite in self.all_sprites:
			if self.camera.apply(sprite).colliderect(self.screen.get_rect()):
				self.screen.blit(sprite.image, self.camera.apply(sprite))
		self.display_stats()  # Draw the status bar
		if self.is_paused:
			self.draw_text("Paused", 50, WHITE, self.screen.get_width() // 2, self.screen.get_height() // 2)
		pygame.display.flip()

	def draw_text(self, text, size, color, x, y):
		font = pygame.font.Font(pygame.font.match_font('arial'), size)
		text_surface = font.render(text, True, color)
		text_rect = text_surface.get_rect()
		text_rect.midtop = (x, y)
		self.screen.blit(text_surface, text_rect)

	def display_stats(self):
		stats_surface = pygame.Surface((WIN_WIDTH, 40), pygame.SRCALPHA)  # create surface for stat bar
		stats_surface.fill((0, 0, 0 ,128))
		text = self.font.render(
			f"Lvl {self.player.level}  Exp {self.player.exp}  HP {self.player.health} ${self.player.money}", True,
			WHITE)
		text_rect = text.get_rect(center=(WIN_WIDTH // 2, 25))  # centered horizontally, 25 px from top
		stats_surface.blit(text, text_rect)
		self.screen.blit(stats_surface, (0, 0))

	def main(self):
		while self.is_playing:
			self.events()
			self.update()
			self.draw()

	def game_over(self):
		text = self.font.render("Game Over!", True, WHITE)
		text_rect = text.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))
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
			self.screen.blit(self.go_background, (0, 0))
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

			self.screen.blit(self.intro_background, (0, 0))
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
        y = -target.rect.centery + int((WIN_HEIGHT - 50) / 2)  # Adjust for the status bar

        # limit scrolling to map size
        x = min(0, x)  # ensure camera does not go past the left edge
        y = min(0, y)  # ensure camera does not go past the top edge
        x = max((self.width - WIN_WIDTH), x)  # ensure camera does not go past the right edge
        y = max((self.height - (WIN_HEIGHT - 80)), y)  # ensure camera does not go past the bottom edge

        self.camera = pygame.Rect(x, y, self.width, self.height)

g = Game()
g.intro_screen()
g.new()
while g.running:
	g.main()
	g.game_over()

pygame.quit()
sys.exit()
