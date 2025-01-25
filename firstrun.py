import pygame
from sys import exit
from random import randint, choice

# Constants
SCALE_FACTOR_PLAYER = 0.3
SCALE_FACTOR_ENEMY = 0.3
scale = 0.1
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load and scale images
        player_walk_1 = pygame.image.load(r"C:\Users\shivn\OneDrive\Pictures\for game\character_idle_0.png").convert_alpha()
        player_walk_2 = pygame.image.load(r"C:\Users\shivn\OneDrive\Pictures\for game\character_run_0.png").convert_alpha()
        player_walk_1 = pygame.transform.scale(player_walk_1, (int(player_walk_1.get_width() * SCALE_FACTOR_PLAYER), int(player_walk_1.get_height() * SCALE_FACTOR_PLAYER)))
        player_walk_2 = pygame.transform.scale(player_walk_2, (int(player_walk_2.get_width() * SCALE_FACTOR_PLAYER), int(player_walk_2.get_height() * SCALE_FACTOR_PLAYER)))
        self.player_walk = [player_walk_1, player_walk_2]

        self.player_jump = pygame.image.load(r"C:\Users\shivn\OneDrive\Pictures\for game\character_jump_0.png").convert_alpha()
        self.player_jump = pygame.transform.scale(self.player_jump, (int(self.player_jump.get_width() * SCALE_FACTOR_PLAYER), int(self.player_jump.get_height() * SCALE_FACTOR_PLAYER)))

        self.player_index = 0
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 330))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 330:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 330:
            self.rect.bottom = 330

    def animation_state(self):
        if self.rect.bottom < 330:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        # Load and scale images
        if type == 'fly':
            fly_1 = pygame.image.load(r"C:\Users\shivn\OneDrive\Pictures\for game\fly1.png").convert_alpha()
            fly_2 = pygame.image.load(r"C:\Users\shivn\OneDrive\Pictures\for game\fly2.png").convert_alpha()
            fly_1 = pygame.transform.scale(fly_1, (int(fly_1.get_width() * scale), int(fly_1.get_height() * scale)))
            fly_2 = pygame.transform.scale(fly_2, (int(fly_2.get_width() * scale), int(fly_2.get_height() * scale)))
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load(r"C:\Users\shivn\OneDrive\Pictures\for game\w_034.png").convert_alpha()
            snail_2 = pygame.image.load(r"C:\Users\shivn\OneDrive\Pictures\for game\w_055.png").convert_alpha()
            snail_1 = pygame.transform.scale(snail_1, (int(snail_1.get_width() * SCALE_FACTOR_ENEMY), int(snail_1.get_height() * SCALE_FACTOR_ENEMY)))
            snail_2 = pygame.transform.scale(snail_2, (int(snail_2.get_width() * SCALE_FACTOR_ENEMY), int(snail_2.get_height() * SCALE_FACTOR_ENEMY)))
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def collision_sprite():
    # Check if player collides with any obstacle using pixel-perfect detection
    for obstacle in obstacle_group:
        if player.sprite.rect.colliderect(obstacle.rect):
            # Get the pixels of the player and obstacle
            player_mask = pygame.mask.from_surface(player.sprite.image)
            obstacle_mask = pygame.mask.from_surface(obstacle.image)

            # Get the offset of the player relative to the obstacle
            offset = (obstacle.rect.x - player.sprite.rect.x, obstacle.rect.y - player.sprite.rect.y)

            # Check if there is any overlap
            if player_mask.overlap(obstacle_mask, offset):
                return True
    return False


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font(r"C:\Users\shivn\OneDrive\Pictures\for game\Pixeltype.ttf", 50)
game_active = False
start_time = 0
score = 0

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# Load and scale backgrounds
sky_surface = pygame.image.load(r"C:\Users\shivn\OneDrive\Pictures\for game\sky.png").convert()
sky_surface = pygame.transform.scale(sky_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
ground_surface = pygame.image.load(r"C:\Users\shivn\OneDrive\Pictures\for game\ground.png").convert()
ground_surface = pygame.transform.scale(ground_surface, (SCREEN_WIDTH, SCREEN_HEIGHT // 2))

# Intro screen
player_stand = pygame.image.load(r"C:\Users\shivn\OneDrive\Pictures\for game\character_idle_0.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 0.5)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = test_font.render('FIRST RUN', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render('PRESS SPACE TO RUN', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 330))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # Check for collision
        if collision_sprite():
            game_active = False
            score = display_score()

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)

        score_message = test_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
