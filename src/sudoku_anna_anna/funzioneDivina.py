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

# font per le lettere e numeri da mettere ai lati della tabella e all'interno delle caselle
font_sudoku = pygame.font.SysFont('Arial', 45, bold=True)
font_coordinate = pygame.font.SysFont('Georgia', 30, italic=True)

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
    
    # linee orizzontali e verticali di tutta la griglia
    for x in range(9):
        linee_orizzontali = pygame.draw.line(screen, "black", (150, 150 + (100 * x)), (1050, 150 + (100 * x)), 5)
        linee_verticali = pygame.draw.line(screen, "black", (250 + (100 * x), 50), (250 + (100 * x), 1000), 5)
    
    # linee più spesse che creano la griglia tipica del sudoku
    for y in range(4):
        spesse_orizzontali = pygame.draw.line(screen, "black", (150, 50 + (300 * y)), (1050, 50 + (300 * y)), 10)
        spesse_verticali = pygame.draw.line(screen, "black", (150 + (300 * y), 50), (150 + (300 * y), 1000), 10)
    
    # stabilisce delle variabili (posizione, altezza e larghezza) per ogni quadretto della griglia 
    for rect in lista_pulsanti:
        posizione = rect.topleft
        altezza = rect.height
        larghezza = rect.width
        
        c = random.randint(0, 255)
        
        colore = (c, c, c, 10)
        
        # pygame.draw.rect(screen, colore, rect)
    
    # NUMERI E LETTERE FUORI DAL SUDOKU
    for i in range(9):
        # Lettere A-I sopra le colonne
        testo_colonna = font_coordinate.render(lettere[i], True, "blue")
        
        # Utilizza la variabile 'quadretto' per distanziarle: 150 (margine) + i * 100 + metà quadretto
        x_lettera = 150 + (i * quadretto) + (quadretto // 2) - 15
        # scrive la lettera
        screen.blit(testo_colonna, (x_lettera, 10))
        
        # Numeri 1-9 a sinistra delle righe
        testo_riga = font_coordinate.render(str(i + 1), True, "blue")
        # Usa 'quadretto' per l'altezza: 50 (margine) + i * 100 + metà quadretto
        y_riga = 50 + (i * quadretto) + (quadretto // 2) - 15
        # scrive il numero
        screen.blit(testo_riga, (110, y_riga))

    # NUMERI NELLE CASELLE
    for i in range(len(lista_pulsanti)):
        rettangolo_corrente = lista_pulsanti[i]
        
        # Trova riga e colonna (1-9) per la funzione prendi_valore_da_casella (per stabilire successivamente la variabile contenente entrambe le coordinate)
        riga = (i // 9) + 1
        colonna = (i % 9) + 1
        
        # variabili trovate attraverso la funzione iniziale
        valore_da_disegnare = prendi_valore_da_casella(riga, colonna)
        
        # Se la casella contiene un numero (diverso da 0 o vuoto)
        if str(valore_da_disegnare) != "0" and str(valore_da_disegnare) != "":
            
            testo_num = font_sudoku.render(str(valore_da_disegnare), True, "black")
            
            # Usiamo le proprietà del rettangolo (altezza e larghezza) per centrare
            # 'get_rect(center=...)' calcola tutto da solo usando i dati del pulsante
            pos_centro = testo_num.get_rect(center=rettangolo_corrente.center)
            screen.blit(testo_num, pos_centro)
    
    pygame.display.flip()
