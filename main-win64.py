##### IMPORTS #####
import pygame
from pygame.locals import *
#import subprocess as sub
#import random
import os
import winsound



##### Initializing the Pygame Libraries #####
pygame.init()
pygame.font.init() # Font Library
#pygame.mixer.init() # Music/Sound Effects Library


##### CONSTANTS #####
WINDOWSIZE = WIDTH, HEIGHT = 1100, 700
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 65, 55
BULLET_WIDTH, BULLET_HEIGHT = 10, 5
BORDER_WIDTH = 10
BORDER = pygame.Rect((WIDTH//2)-(BORDER_WIDTH//2), 0, BORDER_WIDTH, HEIGHT)

VEL = 5 # Velocity of the Spaceships # Default: 5, 7
BULLET_VEL = 7 # Velocity of the bullets # Default: 7, 5
MAX_BULLETS = 5 # Maximum number of bullets # Default: 5, 10

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_HEALTH = 12 # Default: 12, 20
RED_HEALTH = 12 # Default: 12, 20

SEC_DELAY = 5

#BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/attack_sound.wav')
#BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/laser.wav')


# COLORS (RGB)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

##### WINDOW #####
window = pygame.display.set_mode((WINDOWSIZE))
window_title = "Space-Wars"
pygame.display.set_caption(window_title)


##### IMAGES #####
YELLOW_SPACSHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
SPACE_IMAGE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

# Spaceships
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(
        YELLOW_SPACSHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(
        RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)


##### FPS #####
FPS = 60


##### FONTS #####
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
FPS_FONT = pygame.font.SysFont('comicsans', 35)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
SEC_FONT = pygame.font.SysFont('comicsans', 70)


##### Other Functions #####

def update_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health):
    window.blit(SPACE_IMAGE, (0,0))
    pygame.draw.rect(window, BLACK, BORDER)

    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    fps_text = FPS_FONT.render("FPS: " + str(FPS), 1, WHITE)
    window.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    window.blit(yellow_health_text, (10, 10))
    window.blit(fps_text, (WIDTH/2 - (fps_text.get_width()/2), 10))

    window.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    window.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(window, YELLOW, bullet)
    for bullet in red_bullets:
        pygame.draw.rect(window, RED, bullet)

    pygame.display.update()


def handle_yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # Left
            yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + yellow.width + VEL < BORDER.x: # Right
            yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # Up
            yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + yellow.height + VEL < HEIGHT - 10: # Down (slight issues; hardcoded)
            yellow.y += VEL


def handle_red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + 5 + BORDER.width: # Left (slight issues; hardcoded)
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + red.width + VEL < WIDTH + 8: # Right (slight issues; hardcoded)
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # Up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + red.height + VEL < HEIGHT - 10: # Down (slight issues; hardcoded)
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text, sec):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    window.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - (draw_text.get_height()/2 + 30)))
    sec_text = SEC_FONT.render(sec, 1, WHITE)
    window.blit(sec_text, (WIDTH/2 - sec_text.get_width()/2, HEIGHT/2 + 30))
    pygame.display.update()
    pygame.time.delay(SEC_DELAY * 1000)
    #for i in range(1,5):
        #delay -= 1
        #text()
        #pygame.time.delay(1000)


def sound_effect():
    winsound.PlaySound("Assets/attack.wav", winsound.SND_ASYNC) # For Windows



##### MAIN FUNC #####
def main():
    yellow = pygame.Rect(100, 100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(750, 400, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    yellow_bullets = []
    red_bullets = []

    yellow_health = YELLOW_HEALTH
    red_health = RED_HEALTH

    sec_delay = SEC_DELAY

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - BULLET_HEIGHT//2, BULLET_WIDTH, BULLET_HEIGHT)
                    yellow_bullets.append(bullet)
                    sound_effect()

                if event.key == pygame.K_SLASH and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - BULLET_HEIGHT//2, BULLET_WIDTH, BULLET_HEIGHT)
                    red_bullets.append(bullet)
                    sound_effect()
            

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                sound_effect()

            if event.type == RED_HIT:
                red_health -= 1
                sound_effect()

        winner_text = ""
        sec_text = f"Restarting in: {sec_delay} Seconds..."
        if yellow_health <= 0:
            winner_text = "Red (Right) Wins!"
        if red_health <= 0:
            winner_text = "Yellow (Left) Wins!"
        if winner_text != "":
            draw_winner(winner_text, sec_text)
            break

        
        keys_pressed = pygame.key.get_pressed()
        handle_yellow_movement(keys_pressed, yellow)
        handle_red_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets,
            yellow, red)

        update_window(yellow, red,
            yellow_bullets, red_bullets,
                yellow_health, red_health)
    
    main()


##### STARTING THE GAME #####
if __name__ == "__main__":
    main()
