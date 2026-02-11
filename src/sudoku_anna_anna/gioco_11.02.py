import pygame

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Aggiungere forme geometriche") 



running = True

font = pygame.font.SysFont('Georgia',30) 
textRect = font.render('Esci' , True , "white") 
buttonRect = pygame.Rect(1000, 925, 140, 30)
    
while running:
    
    # posizione del mouse
    mPos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

        # quando clicchi SOPRA il pulsante... FAI QUALCOSA!!!
        if event.type == pygame.MOUSEBUTTONDOWN: 
            if buttonRect.collidepoint(mPos):
                running = False
                
    screen.fill("white")

    # ANIMAZIONE DEL PULSANTE (cambia colore quando ci passi sopra)
    buttonColor = "red"
    if buttonRect.collidepoint(mPos):
        buttonColor = "blue"
    button = pygame.draw.rect(screen,buttonColor,buttonRect)
    
    screen.blit(textRect , (1000 + 45, 925))
    
    
    for x in range(9):
        linee_orizzontali = pygame.draw.line(screen, "black", (50, 50 + (100 * x)), (950, 50 + (100 * x)), 5)
        linee_verticali = pygame.draw.line(screen, "black", (150 + (100 * x), 50), (150 + (100 * x), 950), 5)
    
    for y in range(4):
        spesse_orizzontali = pygame.draw.line(screen, "black", (50, 50 + (300 * y)), (950, 50 + (300 * y)), 10)
        spesse_verticali = pygame.draw.line(screen, "black", (50 + (300 * y), 50), (50 + (300 * y), 950), 10)
    pygame.display.flip() 

pygame.quit()