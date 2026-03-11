# Gioco Sudoku
# La potete utilizzare finchè Anna smette di ridere

# importiamo tutti i moduli che ci servono
import pygame
import random
import time 

from sudoku9 import SudokuSolver
from sudoku9 import SudokuGenerator

# in questo modo la variabile puzzle può equivalere ad una lista oppure a niente(None) e in questo caso vale niente(None)
puzzle: list | None = None
# dobbiamo stabilire anche il puzzle dell'utente così da poterci salvare le modifiche dell'utente e riuscire a vedere se halla fine ha risolto il sudoku o no
user_puzzle: list | None = None

pygame.init()

# carichiamo l'immagine
immagine_originalesx = pygame.image.load("immagine_sinistra.jpeg")
immagine_originaledx = pygame.image.load("immagine_destra.jpeg")

# ridimensiona le immagini
immagine_sinistra = pygame.transform.scale(immagine_originalesx, (215, 120))
immagine_destra = pygame.transform.scale(immagine_originaledx, (200, 150))

# gli stati del gioco sono "menu" e "playing"
STATE = "menu"

# grandezza della finestra
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 1000

# variabile della misura del quadretto
quadretto = 100

# lettere che andranno sulle colonne della griglia
lettere = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]

# font per le lettere e numeri da mettere ai lati della tabella e all'interno delle caselle
font_sudoku = pygame.font.SysFont('Arial', 60)
font_titolo = pygame.font.SysFont('Georgia', 80, bold=True)
font_coordinate = pygame.font.SysFont('Georgia', 30, italic=True)

# CICLO CHE CREA OGNI CASELLA SU OGNI RIGA
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
        # crea gli oggetti (i quadrati)
        oggetto_pulsante = pygame.Rect(50 + (x * 100), (50 + y), quadretto, quadretto)
        lista_pulsanti.append(oggetto_pulsante)
    # in questo modo si cambia sempre riga (si scende ogni volta della misura del quadretto che è 100)
    y += 100

# impostiamo i font
font = pygame.font.SysFont('Georgia',30)  
buttonRect = pygame.Rect(1100, 910, 180, 50)

# colore e carattere dei rettangoli per le tre difficoltà del sudoku (facile, medio, difficile) della scheramata iniziale
easy_difficulty_button_text = font.render("FACILE", True, (120, 200, 255))
easy_difficulty_button_rect = easy_difficulty_button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))

medium_difficulty_button_text = font.render("MEDIO", True, (150, 210, 255))
medium_difficulty_button_rect = medium_difficulty_button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 75))

hard_difficulty_button_text = font.render("DIFFICILE", True, (200, 230, 255))
hard_difficulty_button_rect = hard_difficulty_button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 150))

# variabili necessarie per calcolare il tempo impiegato a risolvere il sudoku
start_time = 0
vittoria_registrata = False

# FUNZIONI

# in base alla riga e alla colonna prende dal puzzle creato dal generatore il valore che va inserito nella casella
def prendi_valore_da_casella(riga, colonna):
    row = puzzle[riga-1]
    valore = row[colonna-1]
    
    return valore

# funzione che verifica se il numero inserito è già presente nella stessa riga o colonna
def mossa_valida(griglia, r, c, val):
    # se la casella è vuota, non c'è errore
    if val == ".": return True
    # controlla riga e colonna
    # tranne quella appena selezionata perchè se no
    # dovrebbe controllare se il numero da controllare c'è nella casella dove c'è il numero stesso
    # e c'è sicuramente perciò renderebbe la casella selezionata rossa ogni volta
    for i in range(9):
        # griglia alla riga r e alla colonna i
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

# funzione che controlla se i numeri inseriti nello user_puzzle( il sudoku dell'utente ) coincidono con i numeri della soluzione
def controlla_vittoria():
    # r = righe
    for r in range(9):
        # c = colonne
        for c in range(9):
            # se c'è un punto o il numero è diverso dalla soluzione
            if user_puzzle[r][c] == "." or user_puzzle[r][c] != soluzione_completa[r][c]:
                return False
    return True

# creo questa variabile che all'inizio deve essere nulla e ogni volta che genra il sudoku la soluzione cambia valore
soluzione_completa = None

# funzione che genera il puzzle in base al livello selezionato dall'utente
def genera_puzzle(opzione: str):
    # in pratica global evita di creare una variabile DENTRO la funzione e quindi si riferisce a "puzzle" che si trova fuori dalla funzione
    global puzzle, user_puzzle, soluzione_completa

    generator = SudokuGenerator(difficulty=opzione)
    # prende il puzzle dal generatore della difficoltà inserita
    puzzle = generator.get_puzzle()
    
    # prende la funzione soluzione
    solver = SudokuSolver(puzzle)
    # fa la soluzione del puzzle generato
    soluzione_completa = solver.solve()
    
    # aggiunge i numeri fissi al puzzle dell'utente
    user_puzzle = [list(row) for row in puzzle]

    print("Puzzle Generato:")
    
    # stampa la griglia sudoku generata nel terminale
    for row in puzzle: # type: ignore
        print(" ".join(row))
    
    #  nel caso si volesse stampare la soluzione nel terminale
#     print("Soluzione del Sudoku:")
#     for row in soluzione_completa:
#         print(" ".join(row))

# funzione che cambia la variabile STATE, fa partire il cronometro e fa si che la variabile vittoria_registrata diventi sempre False ogni volta che si inizia il gioco
def inizia_gioco(opzione: str):
    # global = permette di interagire e utilizzare le variabili già esistenti fuori dalla funzione, dentro la funzione
    global STATE, puzzle, start_time, vittoria_registrata
    # reset per la nuova partita
    vittoria_registrata = False
    print(f"Inizio il gioco con difficoltà {opzione}")
    # genera il puzzle della difficoltà selezionata
    genera_puzzle(opzione)
    # parte il cronometro
    start_time = time.time()
    STATE = "playing"

# funzione che scrive il tempo impiegato in un file di testo quando hai completato il sudoku
def salva_punteggio(tempo_totale):
    minuti = int(tempo_totale // 60)
    secondi = int(tempo_totale % 60)
    tempo_formattato = f"{minuti:02}:{secondi:02}"
    
    file = open("risultati_sudoku.txt", "a")
    file.write(f"Partita completata in: {tempo_formattato} minuti\n")
    file.close() 
    print(f"Punteggio salvato manualmente: {tempo_formattato}")


# all'inizio nessuna casella è selezionata (variabile che serve per scrivere nel terminale quale casella hai selezionato)
casella_selezionata = None

# schermo
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

running = True

# quando inizia il gioco
while running:
    # colora lo sfondo di bianco
    screen.fill("white")

    # posizione del mouse
    mPos = pygame.mouse.get_pos() 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        # quando clicchi sopra al pulsante esci, chiude il gioco
        if event.type == pygame.MOUSEBUTTONDOWN: 
            if buttonRect.collidepoint(mPos):
                running = False
                
        # quando clicchi sopra un pulsante
        if event.type == pygame.MOUSEBUTTONDOWN:
            if STATE == "playing":
                for i in range(len(lista_pulsanti)):
                    if lista_pulsanti[i].collidepoint(mPos):
                        # Memorizzo l'indice della casella
                        casella_selezionata = i
                    
                        # trova il nome della casella che hai cliccato dalla lista_pulsanti
                        nome = lista_nomipulsanti[i]
                        print("Il nome della casella è:", nome)
                        
                        # splitta il nome per avere solo i valori di riga e colonna
                        valori = nome.replace("buttonRect_", "").split("_")
                        
                        riga = int(valori[0])
                        colonna = int(valori[1])
                        
                        # trova la lettera del sudoku
                        lettera_colonna = lettere[colonna-1]
                        
                        print(riga, lettera_colonna)
                        
                        # trova quale valore del puzzle generato va su quella casella
                        valore_dal_puzzle = prendi_valore_da_casella(riga, colonna)
                        
                        print(f"Il valore che hai selezionato è {valore_dal_puzzle}")
        
            elif STATE == "menu":
                # si passa allo stato playing che è diverso in base a quale livello clicchi
                # perchè in base al livello crea una griglia diversa
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
    

    if STATE == "playing" and puzzle != None and user_puzzle != None:
        buttonColor = "red"
        if buttonRect.collidepoint(mPos):
            buttonColor = "blue"
        button = pygame.draw.rect(screen, buttonColor, buttonRect)
        
        textRect = font.render('Esci' , True , "white")
        textRect_centrato = textRect.get_rect(center=buttonRect.center)
        # la funzione blit praticamente inserisce gli oggetti creati (che abbiamo creato figuratamente) nello schermo
        screen.blit(textRect, textRect_centrato)
        
        # linee orizzontali e verticali di tutta la griglia
        for x in range(9):
            linee_orizzontali = pygame.draw.line(screen, "black", (150, 150 + (100 * x)), (1050, 150 + (100 * x)), 5)
            linee_verticali = pygame.draw.line(screen, "black", (250 + (100 * x), 50), (250 + (100 * x), 950), 5)
    
         # linee più spesse che creano la griglia tipica del sudoku
        for y in range(4):
            spesse_orizzontali = pygame.draw.line(screen, "black", (150, 50 + (300 * y)), (1050, 50 + (300 * y)), 10)
            spesse_verticali = pygame.draw.line(screen, "black", (150 + (300 * y), 50), (150 + (300 * y), 950), 10)
        
    
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
        
            # in questo if c'è il programma che colora i numeri del sudoku
            # se la casella non è vuota
            if str(valore_da_disegnare) not in [".", ""]:
                # determina il colore: Nero se fisso, altrimenti Blu (valido) o Rosso (errore)
                # numeri fissi -> neri
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
                
                # scrive i numeri centralmente nelle caselle
                testo_num = font_sudoku.render(str(valore_da_disegnare), True, colore)
                pos_centro = testo_num.get_rect(center=rettangolo_corrente.center)
                screen.blit(testo_num, pos_centro)
        
        # se hai vinto ti fa vedere il rettangolo con scritto "HAI VINTO!" e ti da delle info su dove vedere quanto tempo hai impiegato
        if controlla_vittoria():
            # disegna un rettangolo per far risaltare la scritta (posizione orizzontale, posizione verticale, larghezza, altezza)
            messaggio_rect = pygame.Rect(SCREEN_WIDTH // 2 - 350, SCREEN_HEIGHT // 2 - 90, 600, 180)
            # (0,200,0) stanno ad indicare il colore verde, disegna il rettangolo
            pygame.draw.rect(screen, (0, 200, 0), messaggio_rect, border_radius=15)
            
            # stabiliamo le caratteristiche del font
            testo_vittoria = font_sudoku.render("HAI VINTO!", True, "white")
            text_rect = testo_vittoria.get_rect(center=messaggio_rect.center)
            # scriviamo il font nello schermo
            screen.blit(testo_vittoria, text_rect)   
            
            # creiamo un font più piccolo da inserire sotto la scritta hai vinto
            font_info = pygame.font.SysFont('Georgia', 22, italic=True)
            testo_info = font_info.render("Il tempo impiegato è scritto nel file risultati_sudoku.txt", True, "white")
            info_rect = testo_info.get_rect(center=(messaggio_rect.centerx, messaggio_rect.bottom - 45))
            # scriviamo il font nello schermo
            screen.blit(testo_info, info_rect)
            
            # se vittoria_registrara non è False quindi è True, ferma il tempo e lo salva 
            if not vittoria_registrata:
                tempo_finale = time.time() - start_time
                salva_punteggio(tempo_finale)
                vittoria_registrata = True
    
    # disegna tutte le cose del menu iniziale
    elif STATE == "menu":
        # colore dello schermo del menu
        screen.fill((8, 18, 60))
        # cambia il titolo con quello desiderato
        title_surface = font_titolo.render("Sudoku Anna\u00b2", True, (170, 230, 255))
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6))
        screen.blit(title_surface, title_rect)
        
        # disegna i rettangoli delle difficoltà (posizione orizzontale, posizione verticale, larghezza, altezza)
        pygame.draw.rect(screen, (30, 60, 120), (easy_difficulty_button_rect.topleft[0] -15, easy_difficulty_button_rect.topleft[1] - 5, easy_difficulty_button_rect.width + 30, easy_difficulty_button_rect.height + 10))
        screen.blit(easy_difficulty_button_text, easy_difficulty_button_rect)

        pygame.draw.rect(screen, (40, 80, 150), (medium_difficulty_button_rect.topleft[0] -15, medium_difficulty_button_rect.topleft[1] - 5, medium_difficulty_button_rect.width + 30, medium_difficulty_button_rect.height + 10))
        screen.blit(medium_difficulty_button_text, medium_difficulty_button_rect)

        pygame.draw.rect(screen, (50, 100, 170), (hard_difficulty_button_rect.topleft[0] -15, hard_difficulty_button_rect.topleft[1] - 5, hard_difficulty_button_rect.width + 30, hard_difficulty_button_rect.height + 10))
        screen.blit(hard_difficulty_button_text, hard_difficulty_button_rect)
        
        # posizionamento immagini ai lati dei pulsanti
        # sinistra: accanto al primo pulsante (FACILE)
        screen.blit(immagine_sinistra, (easy_difficulty_button_rect.left - 245, easy_difficulty_button_rect.centery - 60))

        # destra: accanto all'ultimo pulsante (DIFFICILE)
        screen.blit(immagine_destra, (hard_difficulty_button_rect.right + 30, hard_difficulty_button_rect.centery - 60))

    
    # mostra tutto quello che hai disegnato durante il ciclo while
    pygame.display.flip()
