# Funzione in grado di verificare il contenuto della casella
# La potete utilizzare finchè Anna smette di ridere

import random
import time 

from sudoku9 import SudokuGenerator

puzzle: list | None = None
user_puzzle: list | None = None

import pygame

pygame.init()

# gli stati sono "menu" e "playing"
STATE = "menu"

SCREEN_WIDTH = 1400
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

running = True

font = pygame.font.SysFont('Georgia',30) 
textRect = font.render('Esci' , True , "white") 
buttonRect = pygame.Rect(1200, 925, 140, 30)

# all'inizio nessuna casella è selezionata
casella_selezionata = None

# per le tre difficoltà del sudoku (facile, medio, difficile)
easy_difficulty_button_text = font.render("FACILE", True, "white")
easy_difficulty_button_rect = easy_difficulty_button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))

medium_difficulty_button_text = font.render("MEDIO", True, "white")
medium_difficulty_button_rect = medium_difficulty_button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 75))

hard_difficulty_button_text = font.render("DIFFICILE", True, "white")
hard_difficulty_button_rect = hard_difficulty_button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 150))

# funzione che verifica se il numero inserito è già presente nella stessa riga o colonna
def mossa_valida(griglia, r, c, val):
    # se la casella è vuota, non c'è errore
    if val == ".": return True
    # controlla riga e colonna
    # tranne quella appena selezionata perchè se no
    # dovrebbe controllare se il numero da controllare c'è nella casella dove c'è il numero stesso
    # e c'è sicuramente e renderebbe la casella selezionata rossa ogni volta
    for i in range(9):
        if (griglia[r][i] == val and i != c) or (griglia[i][c] == val and i != r):
            return False
    # controlla il quadratino 3x3
    start_r, start_c = 3 * (r // 3), 3 * (c // 3)
    for i in range(start_r, start_r + 3):
        for j in range(start_c, start_c + 3):
            if griglia[i][j] == val and (i != r or j != c):
                return False
    # ritorna True se  possibile scrivere quel numero in quella casella (e non ci sono doppioni)
    return True

def genera_puzzle(opzione: str):
    # in pratica global evita di creare una variabile DENTRO la funzione e quindi si riferisce a "puzzle" che si trova fuori dalla funzione
    global puzzle, user_puzzle

    generator = SudokuGenerator(difficulty=opzione)
    puzzle = generator.get_puzzle()

    user_puzzle = [list(row) for row in puzzle] # type: ignore

    print("Puzzle Generato:")

    for row in puzzle: # type: ignore
        print(" ".join(row))

def inizia_gioco(opzione: str):
    # global = permette di interagire e utilizzare le variabili già esistenti fuori dalla funzione, dentro la funzione
    global STATE, puzzle

    print(f"Inizio il gioco con difficoltà {opzione}")

    genera_puzzle(opzione)

    STATE = "playing"

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
                
        # quando clicchi sopra il pulsante
        if event.type == pygame.MOUSEBUTTONDOWN:
            if STATE == "playing":
                for i in range(len(lista_pulsanti)):
                    if lista_pulsanti[i].collidepoint(mPos):
                        # Memorizzo l'indice della casella
                        casella_selezionata = i
                    
                        # trova il nome della casella che hai cliccato dalla lista_pulsanti
                        nome = lista_nomipulsanti[i]
                        print("Il nome della casella è:", nome)
                        
                        valori = nome.replace("buttonRect_", "").split("_")
                        
                        riga = int(valori[0])
                        colonna = int(valori[1])
                        
                        lettera_colonna = lettere[colonna-1]
                        
                        print(riga, lettera_colonna)
                        
                        valore_dal_puzzle = prendi_valore_da_casella(riga, colonna)
                        
                        print(f"Il valore che hai selezionato è {valore_dal_puzzle}")
        
            elif STATE == "menu":
                if easy_difficulty_button_rect.collidepoint(mPos):
                    inizia_gioco("easy")
                elif medium_difficulty_button_rect.collidepoint(mPos):
                    inizia_gioco("medium")
                elif hard_difficulty_button_rect.collidepoint(mPos):
                    inizia_gioco("hard")
        
    # se clicchi e se sul punto in cui hai cliccato c'è una casella
    if event.type == pygame.KEYDOWN and casella_selezionata is not None and STATE == "playing" and puzzle != None and user_puzzle != None:
        # trova il nome della casella e le coordinate
        nome = lista_nomipulsanti[casella_selezionata]
        valori = nome.replace("buttonRect_", "").split("_")
        r_idx = int(valori[0]) - 1
        c_idx = int(valori[1]) - 1

        # ti fa scrivere solo se la casella originale (quella iniziale del puzzle che hai inserito nella griglia) era vuota (".")
        if puzzle[r_idx][c_idx] == ".":
            # filtra solo numeri da 1 a 9 (tastiera standard e tastierino)
            if pygame.K_1 <= event.key <= pygame.K_9:
                user_puzzle[r_idx][c_idx] = str(event.key - pygame.K_0)
            elif pygame.K_KP1 <= event.key <= pygame.K_KP9:
                user_puzzle[r_idx][c_idx] = str(event.key - pygame.K_KP1 + 1)
            # permette di cancellare con Backspace o Canc
            elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                user_puzzle[r_idx][c_idx] = "."
         
    screen.fill("white")

    if STATE == "playing" and puzzle != None and user_puzzle != None:
        buttonColor = "red"
        if buttonRect.collidepoint(mPos):
            buttonColor = "blue"
        button = pygame.draw.rect(screen,buttonColor,buttonRect)
        
        screen.blit(textRect , (1200 + 45, 925))
    
        # linee orizzontali e verticali di tutta la griglia
        for x in range(9):
            linee_orizzontali = pygame.draw.line(screen, "black", (150, 150 + (100 * x)), (1050, 150 + (100 * x)), 5)
            linee_verticali = pygame.draw.line(screen, "black", (250 + (100 * x), 50), (250 + (100 * x), 950), 5)
    
         # linee più spesse che creano la griglia tipica del sudoku
        for y in range(4):
            spesse_orizzontali = pygame.draw.line(screen, "black", (150, 50 + (300 * y)), (1050, 50 + (300 * y)), 10)
            spesse_verticali = pygame.draw.line(screen, "black", (150 + (300 * y), 50), (150 + (300 * y), 950), 10)
        
         # stabilisce delle variabili (posizione, altezza e larghezza) per ogni quadretto della griglia 
             
             # pygame.draw.rect(screen, colore, rect)
    
        # NUMERI E LETTERE FUORI DAL SUDOKU
        for i in range(9):
            # lettere A-I sopra le colonne
            testo_colonna = font_coordinate.render(lettere[i], True, "blue")
            
            # utilizza la variabile 'quadretto' per distanziarle: 150 (margine) + i * 100 + metà quadretto
            x_lettera = 150 + (i * quadretto) + (quadretto // 2) - 15
            # scrive la lettera
            screen.blit(testo_colonna, (x_lettera, 10))
            
            # numeri 1-9 a sinistra delle righe
            testo_riga = font_coordinate.render(str(i + 1), True, "blue")
            # usa 'quadretto' per l'altezza: 50 (margine) + i * 100 + metà quadretto
            y_riga = 50 + (i * quadretto) + (quadretto // 2) - 15
            # scrive il numero
            screen.blit(testo_riga, (110, y_riga))

        # NUMERI NELLE CASELLE
        for i in range(len(lista_pulsanti)):
            rettangolo_corrente = lista_pulsanti[i]
            
            # evidenzia la casella selezionata
            if casella_selezionata == i:
                # .inflate(-20, -20) riduce la larghezza e l'altezza di 20 pixel
                # lasciando 10 pixel di "bordo" bianco tutto intorno
                casella_piccola = rettangolo_corrente.inflate(-20, -20)
                
                # disegno la casella azzurra (versione ridotta)
                pygame.draw.rect(screen, (235, 245, 255), casella_piccola, border_radius=8)
            
            # trova riga e colonna (1-9) per la funzione prendi_valore_da_casella (per stabilire successivamente la variabile contenente entrambe le coordinate)
            riga = (i // 9) + 1
            colonna = (i % 9) + 1
            
            # leggiamo da user_puzzle (la griglia modificabile)
            valore_da_disegnare = user_puzzle[riga-1][colonna-1]
        
            # è tutto in questo if il programma che colora i numeri del sudoku
            # se la casella non è vuota
            if str(valore_da_disegnare) not in [".", ""]:
                # determina il colore: Nero se fisso, altrimenti Blu (valido) o Rosso (errore)
                if puzzle[riga-1][colonna-1] != ".":
                    colore = "black"
                else:
                    # usa la funzione mossa_valida passandogli riga e colonna (0-8)
                    valido = mossa_valida(user_puzzle, riga-1, colonna-1, valore_da_disegnare)
                    # colora la casella di blu se non ci sono doppioni (quando valido = True),
                    # altrimenti la colora di rosso (valido = False) (colora entrambe le caselle con i doppioni, tranne i numeri fissi che rimangono neri)
                    # colora entrambe le caselle perchè il ciclo analizza la griglia subito dopo che hai inserito il numero
                    # --> quindi verifica il primo numero che trova e lo rende rosso, poi quando trova il secondo rende rosso anche quello perch in entrambi i casi trova un doppione
                    colore = "blue" if valido else "red"
                
                testo_num = font_sudoku.render(str(valore_da_disegnare), True, colore)
                pos_centro = testo_num.get_rect(center=rettangolo_corrente.center)
                screen.blit(testo_num, pos_centro)
    
    elif STATE == "menu":
        screen.fill((10, 30, 80))
        # cambia il titolo con quello desiderato
        title_surface = font_sudoku.render("Sudoku Anna\u00b2!!", True, (135, 220, 255))
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6))
        screen.blit(title_surface, title_rect)

        pygame.draw.rect(screen, (0, 0, 0), (easy_difficulty_button_rect.topleft[0] -15, easy_difficulty_button_rect.topleft[1] - 5, easy_difficulty_button_rect.width + 30, easy_difficulty_button_rect.height + 10))
        screen.blit(easy_difficulty_button_text, easy_difficulty_button_rect)

        pygame.draw.rect(screen, (0, 0, 0), (medium_difficulty_button_rect.topleft[0] -15, medium_difficulty_button_rect.topleft[1] - 5, medium_difficulty_button_rect.width + 30, medium_difficulty_button_rect.height + 10))
        screen.blit(medium_difficulty_button_text, medium_difficulty_button_rect)

        pygame.draw.rect(screen, (0, 0, 0), (hard_difficulty_button_rect.topleft[0] -15, hard_difficulty_button_rect.topleft[1] - 5, hard_difficulty_button_rect.width + 30, hard_difficulty_button_rect.height + 10))
        screen.blit(hard_difficulty_button_text, hard_difficulty_button_rect)

    
    pygame.display.flip()
