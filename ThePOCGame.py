import pygame
import random

is_game_paused = False

def play():

    score = 0

    global is_game_paused

    x = "Wave 1!"
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

    def wave_check():
        wave_font = pygame.font.SysFont("Consolas", 30)
        wave_surface = wave_font.render(x, True, (255,255,255))
        wave_rect = wave_surface.get_rect()
        # Displaying WAVE counter!
        game_window.blit(wave_surface, (135,600))

    def show_score():
        score_font = pygame.font.SysFont("Consolas", 20)
        score_surface = score_font.render('Score : ' + str(score), True, (255,255,255))
        score_rect = score_surface.get_rect()
        # displaying text
        game_window.blit(score_surface, score_rect)

    def pause_menu():
        global is_game_paused  # Declare it global at the start of the function
        menu_font = pygame.font.SysFont("Consolas", 85)
        menu_font2 = pygame.font.SysFont("Consolas", 20)

        menu_surface = menu_font.render("ThePOCGame", True, (255, 255, 255))
        menu_surface2 = menu_font2.render("Press Escape or P to Continue", True, (255, 255, 255))

        menu_window = pygame.display.set_mode((480, 640))
        menu_rect = menu_surface.get_rect()

        menu_window.blit(menu_surface, menu_rect)
        pygame.display.flip()

        while is_game_paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_p, pygame.K_ESCAPE): 
                        pygame.display.set_caption('ThePOCGame')
                        is_game_paused = False  # Unpause the game

            menu_window.fill((0, 0, 0))  # Clear the screen
            menu_window.blit(menu_surface, (0, 0))
            menu_window.blit(menu_surface2, (75, 600))
            pygame.display.flip()

    while True:
        # handling key events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:  # Press space to make the bird "jump"
                    Player_velocity = jump_strength

                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    if not is_game_paused:
                        is_game_paused = True
                        pygame.display.set_caption('ThePOCPause')
                        pause_menu()  # Call the pause menu while the game is paused

        if not is_game_paused:
            # Apply gravity: increase the velocity over time
            Player_velocity += gravity

            if Player_velocity > 50:
                Player_velocity = 50

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
            pipe_rect.x -= a

            # If the pipe goes off the left side of the screen, reset it to the right
            if pipe_rect.x < -70:  # Pipe width is 70
                pipe_rect.x = 480
                pipe_rect.y = random.randint(0, 570)  # Randomize pipe's vertical position
                score += 1

                Player_rect.x += 10 * dt

            # Clear the screen and redraw everything
            game_window.fill((0, 0, 0))  # Black background
            pygame.draw.rect(game_window, (255, 0, 0), Player_rect)  # Redraw the bird
            pygame.draw.rect(game_window, (255, 255, 0), pipe_rect)  # Redraw the pipe

            if Player_rect.colliderect(pipe_rect):
                score = 0

            show_score()

            if score > 0 and score <= 10:  # round 1
                a = 5
                x = "Wave 1"
                wave_check()

            if score > 10 and score <= 20:  # round 2
                a = 10
                x = "Wave 2"
                wave_check()

            elif score > 20 and score <= 30:  # round 3
                a = 15
                x = "Wave 3"
                wave_check()

            elif score > 30 and score <= 40:  # round 4
                a = 20
                x = "Wave 4"
                wave_check()

            elif score > 40 and score <= 50:  # round 5
                a = 25
                x = "Wave 5"
                wave_check()

            elif score > 50 and score <= 60:  # round 6
                a = 30
                x = "Wave 6"
                wave_check()

            elif score > 60:  # round BONUS!
                a = 35
                x = "Wave BONUS! (Final!)"
                wave_check()

            elif score > 100:
                x = "YOU WIN!"
                wave_check()

            pygame.display.flip()
            clock.tick(fps)

pygame.init()

pygame.display.set_caption('ThePOCMenu')
menu_window = pygame.display.set_mode((480, 640))

menu_font = pygame.font.SysFont("Consolas", 85)
menu_font2 = pygame.font.SysFont("Consolas", 20)

menu_surface = menu_font.render("ThePOCGame", True, (255, 255, 255))
menu_surface2 = menu_font2.render("Press Enter to Play", True, (255, 255, 255))

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

    menu_window.blit(menu_surface, (0, 0))
    menu_window.blit(menu_surface2, (135, 600))

    pygame.display.flip()
