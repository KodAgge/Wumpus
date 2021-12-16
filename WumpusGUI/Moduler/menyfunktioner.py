import pygame, os
from hjälpfunktioner import *
from animationer import *
from spelfunktioner import *

class Huvudmeny():

    def __init__(self, fönster, spelInfo):
        self.fönster = fönster
        self.spelInfo = spelInfo
        self.svårighetsgrad = self.spelInfo.startSvårighetsgrad
        
    #Alla funktioner tar minst in var saker ska printas och spelInfo
    def startmeny(self): #huvudmenyn för spelet, det är här all funktionalitet nås
        self.startmenyBakgrund()
        self.inputSlingaStartmeny()
            
        if self.trycktInstruktioner:
            self.instruktioner()
        elif self.trycktSvårighetsgrad:
            self.väljaSvårighetsgrad()
        elif self.trycktHighscores:
            self.seHighscore()
        elif self.trycktSpela:
            nyttSpel = Spelet(self.fönster, self.spelInfo, self.svårighetsgrad)
            nyttSpel.spelSlingan()

    def startmenyBakgrund(self):
        self.fönster.blit(self.spelInfo.bild["stjärnhimmel"], (0, 0)) #lägger stjärnhimmel som bakgrund
        self.fönster.blit(self.spelInfo.bild["wumpusBild"], (150, 20))

    def inputSlingaStartmeny(self):
        while True:
            musPosition, klick = musInfo()

            self.trycktInstruktioner = knapp(self.fönster, "Instruktioner", 0, 500, 150, 100, self.spelInfo.lila[2], self.spelInfo.lila[3], self.spelInfo.vit, musPosition, klick) #gör en knapp som tar användaren till instruktionerna
            self.trycktSvårighetsgrad = knapp(self.fönster, "Svårighetsgrad", 310, 500, 180, 100, self.spelInfo.lila[2], self.spelInfo.lila[3], self.spelInfo.vit, musPosition, klick) #gör en knapp som låter användaren byta svårighetsgrad
            self.trycktHighscores = knapp(self.fönster, "Highscores", 650, 500, 150, 100, self.spelInfo.lila[2], self.spelInfo.lila[3], self.spelInfo.vit, musPosition, klick) #gör en knapp som låter användaren se highscores
            self.trycktSpela = knapp(self.fönster, "Spela", 300, 325, 200, 120, self.spelInfo.lila[2], self.spelInfo.lila[3], self.spelInfo.vit, musPosition, klick) #startar spelet

            if self.trycktInstruktioner or self.trycktSvårighetsgrad or self.trycktHighscores or self.trycktSpela: #bryter loopen när en knapp har tryckts på
                break

            nyBildOchStängaAv(1, True, self.spelInfo)

    ####

    def instruktioner(self): #visar användaren instruktioner och info om kontroller

        self.visarInstruktioner = True #det börjar med att man ser instruktionerna
        self.skapaInstruktionerText()
        self.fönster.blit(self.spelInfo.bild["stjärnhimmel"], (0, 0))
        self.instruktionerSlinga()

    def instruktionerSlinga(self):        
        while True:
            musPosition, klick = musInfo()
            
            if self.visarInstruktioner: #när instruktionerna visas printas instruktiontexten och en kontroll-knapp skapas
                self.visaInstruktioner(musPosition, klick)
                
            elif not self.visarInstruktioner: #när kontrollerna visas printas kontrolltexten och en instruktion-knapp skapas
                self.visaKontroller(musPosition, klick)
                
            tryckt = knapp(self.fönster, "Tillbaka", 490, 520, 140, 80, self.spelInfo.lila[2], self.spelInfo.lila[3], self.spelInfo.vit, musPosition, klick) #gör en tillbaka-knapp
            if tryckt == True:
                break

            nyBildOchStängaAv(1, True, self.spelInfo)
        
    def visaInstruktioner(self, musPosition, klick):
        printaText(self.fönster, self.instruktioner, 100, 40, 18, self.spelInfo.vit, self.spelInfo.lila[0])
        byta = knapp(self.fönster, "Kontroller", 170, 520, 140, 80, self.spelInfo.lila[2], self.spelInfo.lila[3], self.spelInfo.vit, musPosition, klick)
        if byta == True:
            self.visarInstruktioner = False
            time.sleep(1/4) #eftersom kontroll- och instruktion-knappen ligger på samma koordinater måste det vara en liten delay emellan
            #så användaren inte råkar trycka flera gånger
            self.fönster.blit(self.spelInfo.bild["stjärnhimmel"], (0, 0))
            pygame.draw.rect(self.fönster, self.spelInfo.lila[2], (170, 520, 140, 80))

    def visaKontroller(self, musPosition, klick):
        printaText(self.fönster, self.kontroller, 100, 150, 20, self.spelInfo.vit, self.spelInfo.lila[0])
        byta = knapp(self.fönster, "Instruktioner", 170, 520, 140, 80, self.spelInfo.lila[2], self.spelInfo.lila[3], self.spelInfo.vit, musPosition, klick)
        if byta == True:
            self.visarInstruktioner = True
            time.sleep(1/4)
            self.fönster.blit(self.spelInfo.bild["stjärnhimmel"], (0, 0))
            pygame.draw.rect(self.fönster, self.spelInfo.lila[2], (170, 520, 140, 80))
        

    def skapaInstruktionerText(self):
        #gör instruktion-texten som ska printas
        instruktioner = "Du befinner dig i kulvertarna under CSC, där den glupske Wumpus bor."
        instruktioner += "\nFör att undvika att bli uppäten måste du skjuta Wumpus med din pil"
        instruktioner += "\noch båge. Kulverterna har 30 rum  som är förenade med smala gångar."
        instruktioner += "\nDu kan röra dig åt norr, öster, söder eller väster från ett rum"
        instruktioner += "\ntill ett annat."
        instruktioner += "\nHär finns dock faror som lurar. I vissa rum finns bottenlösa hål. Kliver"
        instruktioner += "\ndu ner i ett sådant dör du omedelbart. I andra rum finns fladdermöss"
        instruktioner += "\nsom lyfter upp dig, flyger en bit och släpper dig i ett godtyckligt"
        instruktioner += "\nrum. I ett av rummen finns Wumpus, och om du vågar dig in i det rummet"
        instruktioner += "\nblir du genast uppäten. Som tur är kan du från rummen bredivd känna"
        instruktioner += "\nvinddraget från ett avgrundshål eller lukten av Wumpus. Du får också"
        instruktioner += "\ni varje rum reda på vilka rum som ligger intill."
        instruktioner += "\nFör att vinna spelet måste du skjuta Wumpus. När du skjuter iväg en"
        instruktioner += "\npil förflyttar den sig igenom tre rum - du kan styra vilken riktning"
        instruktioner += "\npilen ska välja i varje rum. Glöm inte bort att tunnlarna vindlar sig"
        instruktioner += "\npå oväntade sätt. Du kan råka skjuta dig själv..."
        instruktioner += "\nDu har fem pilar. Lycka till!"

        self.instruktioner = instruktioner

        #gör kontroll-texten som ska printas
        kontroller = "Förflyttning"
        kontroller += "\nDu kan gå genom att använda piltangenterna eller [w, a, s, d]."
        kontroller += "\n\n\nSkjuta"
        kontroller += "\nDu kan starta skjutprocessen genom att klicka på skjutknappen eller"
        kontroller += "\ngenom att trycka på [mellanslag]. Du styr pilens riktning genom att"
        kontroller += "\nanvända piltangenterna eller [w, a, s, d]."

        self.kontroller = kontroller

    ####
                
    def väljaSvårighetsgrad(self): #låter spelaren byta svårighetsgrad

        self.skapaSvårighetsText()
        self.startpositionSvårighetsgrad()
        self.svårighetsgradBakgrund()
        self.svårighetsgradSlinga()

    def startpositionSvårighetsgrad(self): #så att slidern börjar på den svårighetsgraden som man tidigare har valt
        if self.svårighetsgrad == "Lätt":
            self.svårighetsSliderPos = int(200+100/2)
        if self.svårighetsgrad == "Medel":
            self.svårighetsSliderPos = int(300+100/2)
        if self.svårighetsgrad == "Svårt":
            self.svårighetsSliderPos = int(400+100/2)
        if self.svårighetsgrad == "Omöjligt":
            self.svårighetsSliderPos = int(500+100/2)

    def svårighetsgradBakgrund(self): #printar bakgrunden som behövs när man väljer svårighetsgrad
        self.fönster.blit(self.spelInfo.bild["stjärnhimmel"], (0, 0))
        pygame.draw.rect(self.fönster, self.spelInfo.lila[3], (200, 420, 400, 20))
        pygame.draw.circle(self.fönster, self.spelInfo.lila[3], (200, 430), 10, 0)
        pygame.draw.circle(self.fönster, self.spelInfo.lila[3], (600, 430), 10, 0)
        pygame.draw.circle(self.fönster, self.spelInfo.lila[5], (self.svårighetsSliderPos, 430), 30, 0)

    def svårighetsgradSlinga(self): #slingan som körs när det väntas på spelarens input
        while True:
            musPosition, klick = musInfo()
            self.svårighetsSlider(musPosition, klick)
            tryckt = knapp(self.fönster, "Tillbaka", 490, 520, 120, 80, self.spelInfo.lila[2], self.spelInfo.lila[3], self.spelInfo.vit, musPosition, klick) #gör en tillbaka-knapp

            if self.svårighetsSliderPos >= 200 and self.svårighetsSliderPos < 300:
                self.svårighetsgrad = "Lätt"
            elif self.svårighetsSliderPos >= 300 and self.svårighetsSliderPos < 400:
                self.svårighetsgrad = "Medel"
            elif self.svårighetsSliderPos >= 400 and self.svårighetsSliderPos < 500:
                self.svårighetsgrad = "Svårt"
            elif self.svårighetsSliderPos >= 500 and self.svårighetsSliderPos < 600:
                self.svårighetsgrad = "Omöjligt"
            
            printaText(self.fönster, self.svårighetsText[self.svårighetsgrad], 250, 75, 22, self.spelInfo.vit, self.spelInfo.lila[0])

            if tryckt == True:
                break
            
            nyBildOchStängaAv(1, True, self.spelInfo)

    def skapaSvårighetsText(self): #skapar texten som ska printas
        self.svårighetsText = dict()
        self.svårighetsText["Lätt"] = "LÄTT\n\nFaror: Låg risk för faror\n\nRum: 20 st\n\nPilar: 5"
        self.svårighetsText["Medel"] = "MEDEL\n\nFaror: Normal risk för faror\n\nRum: 30 st\n\nPilar: 4"
        self.svårighetsText["Svårt"] = "SVÅRT\n\nFaror: Hög risk för faror\n\nRum: 40 st\n\nBonus: Wumpus byter rum\n            efter varje drag\n\nPilar: 3"
        self.svårighetsText["Omöjligt"] = "OMÖJLIGT\n\nFaror:  Faror nästan överallt\n\nRum: 50 st\n\nBonus: Wumpus kommer närmre\n            efter varje drag\n\nPilar: 2"        
        
    def svårighetsSlider(self, musPosition, klick): #skapar en slider och retunerar dess position
        #behöver info om var slidern är och info om musen
        föregåendeSliderPos = self.svårighetsSliderPos
        
        #här separeras musens koordinater så att de ska kunna användas som variabler
        xMus, yMus = musPosition[0], musPosition[1]
        
        if klick[0]: #om man har klickat (1 == True)
            if xMus >= self.svårighetsSliderPos - 30 and xMus <= self.svårighetsSliderPos + 30 and yMus >= 400 and yMus <= 460: #om musen befinner sig inom en kvardat runtom cirkeln på slidern
                self.svårighetsSliderPos =  xMus
                if self.svårighetsSliderPos < 200: #så att slidern inte ska kunna dras för långt
                    self.svårighetsSliderPos = 200
                if self.svårighetsSliderPos > 600:
                    self.svårighetsSliderPos = 600

        if föregåendeSliderPos != self.svårighetsSliderPos: #om spelaren har flyttat på slidern uppdateras skärmen
            self.svårighetsgradBakgrund()

    ####
    
    def seHighscore(self): #visar highscores för alla svårighetsgrader (som kan ändras med en slider)

        self.visadSvårighetsgrad = self.svårighetsgrad #för att spara den nuvarande svårighetsgraden utan att ändra den
        self.visarHighscore = True
        self.startpositionHighscore()
        self.skapaHighscoreText()
        
        while self.visarHighscore: #körs till self.visarHighscore = False
            self.svårighetsgradBryta = self.visadSvårighetsgrad #om en ny svårighetsgrad väljs ska den nedanstående loopen startas om med rätt text
            self.highscoreBakgrund()
            self.highscoreSlinga()

    def startpositionHighscore(self):
        #så att slidern börjar på den svårighetsgraden som man tidigare har valt
        if self.visadSvårighetsgrad == "Lätt":
            self.highscoreSliderPos = int(130+75/2)
        if self.visadSvårighetsgrad == "Medel":
            self.highscoreSliderPos = int(205+75/2)
        if self.visadSvårighetsgrad == "Svårt":
            self.highscoreSliderPos = int(280+75/2)
        if self.visadSvårighetsgrad == "Omöjligt":
            self.highscoreSliderPos = int(355+75/2)
        

    def skapaHighscoreText(self): #skapar higschore texten som ska printas (beroende på svårighetsgrad)
        svårighetsgrader = ["Lätt", "Medel", "Svårt", "Omöjligt"]
        self.highscoreText = dict()
        for svårighetsgrad in svårighetsgrader:
            data = open(os.getcwd() + "//Highscores//Highscore" + svårighetsgrad + ".txt", "r") #öppnar och läser highscore-filen
            highscore = data.read().split()
            data.close()
            highscoreText = "Topplistan - " + svårighetsgrad #lägger till rubriken i text

            for resultat in range(len(highscore)): #lägger till varje drag i text
                highscoreText += "\n\n" + str(resultat + 1) + "." + " "*18 + str(highscore[resultat]) + " drag"
        
            self.highscoreText[svårighetsgrad] = highscoreText

    def highscoreBakgrund(self): #printar bakgrunden och slidern som behövs för att visa highscore
        self.fönster.blit(self.spelInfo.bild["stjärnhimmel"], (0, 0))
        pygame.draw.rect(self.fönster, self.spelInfo.lila[3], (650, 130, 20, 300))
        pygame.draw.circle(self.fönster, self.spelInfo.lila[3], (660, 130), 10, 0)
        pygame.draw.circle(self.fönster, self.spelInfo.lila[3], (660, 430), 10, 0)
        pygame.draw.circle(self.fönster, self.spelInfo.lila[5], (660, self.highscoreSliderPos), 30, 0)

    def highscoreSlinga(self): #slingan som körs när det väntas på spelaren input
        while True:
            musPosition, klick = musInfo()
            self.highscoreSlider(musPosition, klick)
            printaText(self.fönster, self.highscoreText[self.visadSvårighetsgrad], 250, 40, 25, self.spelInfo.vit, self.spelInfo.lila[0]) #printar highscore listan
            trycktTillbaka = knapp(self.fönster, "Tillbaka", 490, 520, 120, 80, self.spelInfo.lila[2], self.spelInfo.lila[3], self.spelInfo.vit, musPosition, klick) #skapar en tillbaka-knapp

            #printar olika saker beroende på vilken svårighetsgrad som är vald
            if self.highscoreSliderPos >= 130 and self.highscoreSliderPos < 205:
                self.visadSvårighetsgrad = "Lätt"
            elif self.highscoreSliderPos >= 205 and self.highscoreSliderPos < 280:
                self.visadSvårighetsgrad = "Medel"
            elif self.highscoreSliderPos >= 280 and self.highscoreSliderPos < 355:
                self.visadSvårighetsgrad = "Svårt"
            elif self.highscoreSliderPos >= 355 and self.highscoreSliderPos < 430:
                self.visadSvårighetsgrad = "Omöjligt"

            if self.svårighetsgradBryta != self.visadSvårighetsgrad:
                break
            if trycktTillbaka == True:
                self.visarHighscore = False
                break

            nyBildOchStängaAv(1, True, self.spelInfo)
        
    def highscoreSlider(self, musPosition, klick): #skapar en slider och retunerar dess position

        föregåendeSliderPos = self.highscoreSliderPos
        
        #här separeras musens koordinater så att de ska kunna användas som enskilda variabler
        xMus, yMus = musPosition[0], musPosition[1]
        
        if klick[0]: #om man har klickat
            if xMus >= 630 and xMus <= 690 and yMus >= self.highscoreSliderPos - 30 and yMus <= self.highscoreSliderPos + 30: #om musen befinner sig inom en kvardat runtom cirkeln på slidern
                self.highscoreSliderPos =  yMus
                if self.highscoreSliderPos < 130: #så att slidern inte ska kunna dras för långt
                    self.highscoreSliderPos = 130
                if self.highscoreSliderPos > 430:
                    self.highscoreSliderPos = 430

        if föregåendeSliderPos != self.highscoreSliderPos:
            #printar cirkeln, strecket den rör sig på och rundar dessutom av kanterna med små cirklar
            self.highscoreBakgrund()
