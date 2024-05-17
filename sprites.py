import pygame
from config import *
import math
import random

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.initialize_attributes(x, y)
        self.load_sprites()

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def initialize_attributes(self, x, y):
        self.health = 5
        self.exp = 0
        self.level = 1
        self.invincible = False
        self.money = 0

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

    def load_sprites(self):
        image_to_load = pygame.image.load('static/assets/img/single.png')
        self.image = image_to_load
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(image_to_load, (self.width, self.height))

        self.down_animations = [self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height)]
        self.up_animations = [self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
                              self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
                              self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height)]
        self.left_animations = [self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height)]
        self.right_animations = [self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
                                 self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
                                 self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height)]

    def update(self):
        self.level_up()
        self.handle_movement()
        self.handle_animation()
        self.collide_with_enemies()

        self.rect.x += self.x_change
        self.collide_with_blocks("x")
        self.rect.y += self.y_change
        self.collide_with_blocks("y")

        self.x_change = 0
        self.y_change = 0

    def level_up(self):
        if self.exp >= 5:
            self.level += 1
            self.exp = 0

    def handle_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y_change += PLAYER_SPEED
            self.facing = 'down'

        # normalize diagonal speed
        if self.x_change != 0 and self.y_change != 0:  # if moving on both x and y-axis
            self.x_change *= 0.7071   # reduce x speed by 1/sqrt(2)
            self.y_change *= 0.7071   # reduce y speed by 1/sqrt(2)

    def collide_with_enemies(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits and not self.invincible:
            if self.health > 1:
                self.health -= 1
                self.invincible = True
                pygame.time.set_timer(pygame.USEREVENT, 1000)
            else:
                self.kill()
                self.game.playing = False

    def turn_off_invincibility(self):
        self.invincible = False

    def collide_with_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def handle_animation(self):
        animations = {
            'down': self.down_animations,
            'up': self.up_animations,
            'left': self.left_animations,
            'right': self.right_animations
        }

        if self.facing in animations:
            if (self.facing in ['left', 'right'] and self.x_change == 0) or (
                    self.facing in ['up', 'down'] and self.y_change == 0):
                self.image = animations[self.facing][0]
            else:
                self.image = animations[self.facing][math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= len(animations[self.facing]):
                    self.animation_loop = 0

class Enemy(pygame.sprite.Sprite):
    id_counter = 0

    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.health = 2
        self.invincible = False
        self.id = Enemy.id_counter
        Enemy.id_counter += 1

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(["left", "right"])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(7, 30)

        self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


        self.down_animations = [self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height)]
        self.up_animations = [self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height),
                              self.game.enemy_spritesheet.get_sprite(35, 34, self.width, self.height),
                              self.game.enemy_spritesheet.get_sprite(68, 34, self.width, self.height)]
        self.left_animations = [self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height),
                                self.game.enemy_spritesheet.get_sprite(35, 98, self.width, self.height),
                                self.game.enemy_spritesheet.get_sprite(68, 98, self.width, self.height)]
        self.right_animations = [self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height),
                                 self.game.enemy_spritesheet.get_sprite(35, 66, self.width, self.height),
                                 self.game.enemy_spritesheet.get_sprite(68, 66, self.width, self.height)]

    def turn_off_invincibility(self):
        self.invincible = False

    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.collide_blocks("x")
        self.rect.y += self.y_change
        self.collide_blocks("y")

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        if self.facing == "left":
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = "right"

        if self.facing == "right":
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = "left"

    def animate(self):
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

    def spawn(self, x, y):
        while self.game.tilemap[x][y] != '.':
            x = random.choice(range(len(self.game.tilemap) - 1))
            y = random.choice(range(len(self.game.tilemap) - 1))

        new_row = list(self.game.tilemap[x])
        new_row[y] = 'E'
        self.game.tilemap[x] = "".join(new_row)

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(960, 448, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.ground
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(64, 352, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('arial.ttf', fontsize)
        self.content = content
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width / 2, self.height / 2))

        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False

class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.animation_loop = 0
        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                                 self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
                                 self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                                 self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
                                 self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]
        self.down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]
        self.left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]
        self.up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                              self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
                              self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                              self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
                              self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        for hit in hits:
            if not hit.invincible:
                if hit.health > 1:
                    hit.health -= 1
                    hit.invincible = True
                    enemy_hit = pygame.USEREVENT + hit.id  # use unique id of enemy
                    self.game.enemy_timers[enemy_hit] = hit  # map event to enemy
                    pygame.time.set_timer(enemy_hit, 500)
                else:
                    hit.kill()
                    self.game.player.exp += 1
                    self.game.player.money += 1

    def animate(self):
        direction = self.game.player.facing

        if direction == "up":
            self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == "down":
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == "left":
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == "right":
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()