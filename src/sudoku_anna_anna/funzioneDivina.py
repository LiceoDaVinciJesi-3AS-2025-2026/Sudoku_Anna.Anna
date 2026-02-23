# Funzione in grado di verificare il contenuto della casella
# La potete utilizzare finchè Anna smette di ridere

import random

from sudoku9 import SudokuGenerator

generator = SudokuGenerator(difficulty="hard")
puzzle = generator.get_puzzle()

for row in puzzle:
    print(" ".join(row))

import pygame

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000

quadretto = 100

lettere = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]

# ciclo che crea ogni casella su ogni riga
# variabili utili per il ciclo for
lista_pulsanti = []
lista_nomipulsanti = []

y = 0

# righe
for z in range(9):
    # caselle su ogni riga
    for x in range(1,10):
        variabile = f"buttonRect_{z+1}_{x}"
        lista_nomipulsanti.append(variabile)
        
        oggetto_pulsante = pygame.Rect(50 + (x * 100), (50 + y), quadretto, quadretto)
        lista_pulsanti.append(oggetto_pulsante)
    y += 100

def prendi_valore_da_casella(riga, colonna):
    row = puzzle[riga-1]
    valore = row[colonna-1]
    
    return valore

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
        # quando clicchi sopra il pulsante
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(lista_pulsanti)):
                if lista_pulsanti[i].collidepoint(mPos):
                # trova il nome della casella che hai cliccato dalla lista_pulsanti
                    nome = lista_nomipulsanti[i]
                    print("Il nome della casella è:", nome)
                    
                    valori = nome.replace("buttonRect_", "").split("_")
                    
                    riga = int(valori[0])
                    colonna = int(valori[1])
                    
                    print(riga, colonna)
                    
                    valore_dal_puzzle = prendi_valore_da_casella(riga, colonna)
                    
                    print(f"Il valore che hai selezionato è {valore_dal_puzzle}")
    
    screen.fill("white")
    
    buttonColor = "red"
    if buttonRect.collidepoint(mPos):
        buttonColor = "blue"
    button = pygame.draw.rect(screen,buttonColor,buttonRect)
    
    screen.blit(textRect , (1000 + 45, 925))
    
    for x in range(9):
        linee_orizzontali = pygame.draw.line(screen, "black", (150, 150 + (100 * x)), (1050, 150 + (100 * x)), 5)
        linee_verticali = pygame.draw.line(screen, "black", (250 + (100 * x), 50), (250 + (100 * x), 1000), 5)
    
    for y in range(4):
        spesse_orizzontali = pygame.draw.line(screen, "black", (150, 50 + (300 * y)), (1050, 50 + (300 * y)), 10)
        spesse_verticali = pygame.draw.line(screen, "black", (150 + (300 * y), 50), (150 + (300 * y), 1000), 10)

    for rect in lista_pulsanti:
        posizione = rect.topleft
        altezza = rect.height
        larghezza = rect.width
        
        c = random.randint(0, 255)
        
        colore = (c, c, c, 10)
        
        # pygame.draw.rect(screen, colore, rect)

    pygame.display.flip()
