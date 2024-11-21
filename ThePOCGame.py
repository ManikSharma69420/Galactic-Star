import pygame
import random

def play():

    score = 0

    x = 200
    y = 400 
    z = 1
    a = 5

    pygame.display.set_caption('ThePOCGame')
    game_window = pygame.display.set_mode((480, 640))

    Player_rect = pygame.draw.rect(game_window, (255,0,0), pygame.Rect(30,320,45,60))
    pygame.display.flip()

    pipe_rect = pygame.draw.rect(game_window, (255,255,0), pygame.Rect(30,320,45,70))
    pygame.display.flip()

    clock = pygame.time.Clock()
    fps = 60  # Set FPS to a reasonable value (e.g., 60 FPS)
    dt = clock.tick(fps) / 1000
    Player_velocity = 0  # This is the bird's falling speed (velocity)
    gravity = 0.75  # The gravity force that accelerates the bird's fall
    jump_strength = -12  # The strength of the bird's jump when a key is pressed
    Player_rect.y = 320  # Start position of the bird (optional to reset position)

    def show_score():

        score_font = pygame.font.SysFont("Consolas", 20)

        score_surface = score_font.render('Score : ' + str(score), True, (255,255,255))

        score_rect = score_surface.get_rect()
            
        # displaying text
        game_window.blit(score_surface, score_rect)

    while True:
        # handling key events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Press space to make the bird "jump"
                    Player_velocity = jump_strength

        # Apply gravity: increase the velocity over time
        Player_velocity += gravity

        # Update the bird's position based on its velocity
        Player_rect.y += Player_velocity

        # Prevent the bird from falling out of bounds
        if Player_rect.y > 640:  # Off the bottom
            Player_rect.y = 0  # Wrap to the top

        if Player_rect.y < 0:  # Off the top
            Player_rect.y = 640  # Wrap to the bottom

        if Player_rect.x > 480:
            Player_rect.x = -50 

        # Clear the screen and redraw the bird
        if score > 0 and score <=10:  # round 1
            a = 5

        if score > 10 and score <= 20:  # round 1
            a = 10

        elif score > 20 and score <= 30:  # round 2
            a = 15

        elif score > 30 and score <= 40:  # round 3
            a = 20

        elif score > 40 and score <= 50:  # round 4
            a = 25

        elif score > 50 and score <= 60:  # round 5
            a = 30

        elif score > 60:  # round BONUS!
            a = 35

        pipe_rect.x -= a
            
        # If the pipe goes off the left side of the screen, reset it to the right
        if pipe_rect.x < -70:  # Pipe width is 70
            pipe_rect.x = 480
            pipe_rect.y = random.randint(0, 570)  # Randomize pipe's vertical position
            score += 1
            print(str(score))

            Player_rect.x += 10 * dt
        # Clear the screen and redraw everything
        game_window.fill((0, 0, 0))  # Black background
        pygame.draw.rect(game_window, (255, 0, 0), Player_rect)  # Redraw the bird
        pygame.draw.rect(game_window, (255, 255, 0), pipe_rect)  # Redraw the pipe

        if Player_rect.colliderect(pipe_rect):
            score = 0

        show_score()

        pygame.display.flip()
        clock.tick(fps)

pygame.init()

pygame.display.set_caption('ThePOCMenu')
menu_window= pygame.display.set_mode((480, 640))

menu_font = pygame.font.SysFont("Consolas",85)

menu_font2 = pygame.font.SysFont("Consolas",20)

menu_surface = menu_font.render("ThePOCGame", True, (255,255,255))

menu_surface2 = menu_font2.render("Press Enter to Play", True, (255,255,255))

menu_rect = menu_surface.get_rect()
        
# displaying text
menu_window.blit(menu_surface, menu_rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER): 
                play()
            
    menu_window.blit(menu_surface,(0,0))
    menu_window.blit(menu_surface2,(135,600))

    pygame.display.flip()
