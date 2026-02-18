# Anna Pieralisi
# funzione in cui se clicchi su una casella ti dice che casella è
# numeri ----> per le righe e lettere ---->  per le colonne
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
        variabile = f"buttonRect_{z}_{x}"
        lista_nomipulsanti.append(variabile)
        
        oggetto_pulsante = pygame.Rect(50 + (x * 100), (50 + y), quadretto, quadretto)
        lista_pulsanti.append(oggetto_pulsante)
    y += 100 

running = True

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
                    # trova i numeri delle coordinate
                    numeroriga = int(nome[11]) + 1
                    numerocolonna = int(nome[13])
                    # trova la lettera corrispondente
                    letteracolonna = lettere[numerocolonna- 1]
                    posizionecasella = ("Casella selezionata: ", numeroriga, letteracolonna)
                
    buttonColor = "white"