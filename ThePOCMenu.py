import pygame
import ThePOCGame

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
                ThePOCGame.play()
            
    menu_window.blit(menu_surface,(0,0))
    menu_window.blit(menu_surface2,(135,600))

    pygame.display.flip()