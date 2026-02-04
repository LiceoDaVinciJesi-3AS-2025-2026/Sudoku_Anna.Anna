import pygame

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Aggiungere forme geometriche") 

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    screen.fill("white")

    # linea VERDE dal punto... al punto ... di spessore ...
    # l è il "rettangolo" che contiene la linea disegnata 
    orizz = pygame.draw.line(screen, "black", (50, 100), (950, 100), 5)
    vert = pygame.draw.line(screen, "black", (50, 100), (50, 950), 5)
    
    pygame.display.flip()

pygame.quit()