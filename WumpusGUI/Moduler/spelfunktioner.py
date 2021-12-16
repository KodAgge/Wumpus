import pygame, random, operator
from hjälpfunktioner import *
from animationer import *

class SpelInfo: #lagrar all info som behövs för spelet som inte behöver göras om vid varje ny spelomgång

    def __init__(self):
        #läser in alla bilder
        sökVäg = os.getcwd() + "//Bilder//"
        bilderNamn = ["wumpusBild", "golv", "delGolv", "spelare", "spelare", "spelareSkjuten", "spelareGårNorr", "spelareGårVäst", "spelareGårÖst", "spelareGårSyd", "fladdermöss", "litenWumpus", "litenWumpusSkjuten", "utropstecken", "stjärnhimmel", "pilbåge", "pilÖst"]
        bild = dict()
        for bilder in range(len(bilderNamn)):
            bild[bilderNamn[bilder]] = pygame.image.load(sökVäg + bilderNamn[bilder] + ".png")
        bild["pilNorr"] = pygame.transform.rotate(bild["pilÖst"], 90) #pilen i nordlig riktning
        bild["pilVäst"] = pygame.transform.rotate(bild["pilÖst"], 180) #pilen i västlig riktning
        bild["pilSyd"] = pygame.transform.rotate(bild["pilÖst"], 270) #pilen i sydlig riktning
        bild["pilRoterad"] = pygame.transform.rotate(bild["pilÖst"], 45) #pilen roterad 45 grader från östlig riktning

        #spelaren centrerad i mitten av planen, används ofta så bra att ha som en klassvariabel så att den är lätt att komma åt
        spelareRektangel = bild["spelare"].get_rect() #hämtar dimensionerna
        spelareRektangel.center = (250, 250) #centrerar

        self.bild = bild
        self.spelareKoordinater = spelareRektangel
        self.bps = 48 #bilderpersekund
        self.klocka = pygame.time.Clock()
        self.hastighet = 4*(24/self.bps) #hur snabbt saker och ting rör sig
        self.startSvårighetsgrad = "Medel" #standardsvårighetsgrad
        #färger
        self.svart = (0, 0, 0)
        self.lila = [(13, 14, 71), (16, 17, 86), (20, 21, 108), (24, 25, 129), (28, 30, 151), (32, 34, 172)] #olika nyanser
        self.vit = (250, 255, 215) #vit-gulish som stjärnorna på bakgrundsbilden
        self.brun = [(169, 136, 104), (181, 153, 125), (190, 166, 142)] #olika nyanser

class Spelet: #en klass därinom spelet körs

    def __init__(self, fönster, spelInfo, svårighetsgrad):
        #startvärden
        self.fönster = fönster
        self.spelInfo = spelInfo
        self.gameOver = False
        self.antalDrag = 0
        self.svårighetsgrad = svårighetsgrad
        self.startaOm = False
        self.resultat = None
        
        #skapar all information som behövs
        self.hittaSvårighetsgrad() #skapar data utifrån vald svårighetsgrad
        self.skapaRum() #skapar rummen
        self.aktivtRum = self.rumsLista[random.randint(0, self.antalRum - 1)].slumpmässigtRum(self.rumsLista) #väljer startrum
        self.wumpusRum = self.rumsLista[self.aktivtRum].slumpmässigtRum(self.rumsLista) #placerar ut wumpus
        self.rumsLista[self.wumpusRum].wumpus = True

    def hittaSvårighetsgrad(self): #sätter info beroende på vilken svårighetsgrad som har valts
        if self.svårighetsgrad == "Lätt":
            self.antalRum = 20
            self.fladdermöss = 20 #procentsats
            self.bottenlöstHål = 10 #%
            self.antalPilar = 5
        elif self.svårighetsgrad == "Medel":
            self.antalRum = 30
            self.fladdermöss = 30
            self.bottenlöstHål = 20
            self.antalPilar = 4
        elif self.svårighetsgrad == "Svårt":
            self.antalRum = 40
            self.fladdermöss = 35
            self.bottenlöstHål = 25
            self.antalPilar = 3
        elif self.svårighetsgrad == "Omöjligt":
            self.antalRum = 50
            self.fladdermöss = 40
            self.bottenlöstHål = 30
            self.antalPilar = 2

    def skapaRum(self): #skapar tre listor, en med alla rum som instansobjekt sorterad efter rumsnummer
        #och två listor som beskriver hur rummen ligger intill varandra
        #tar in info om sannolikheten för faror och hur många rum det ska vara
        
        rumsLista = list() #skapar en tom lista
        self.västTillÖst = random.sample(range(1, self.antalRum + 1), self.antalRum) #skapar en lista med rum i random ordning (västTillÖst)
        self.norrTillSöder = random.sample(range(1, self.antalRum + 1), self.antalRum) #skapar en lista med rum i random ordning (norrTillSöder)
        
        for rumVÖ in range(self.antalRum):
            rumsLista.append(Rum(self.västTillÖst[rumVÖ], self.västTillÖst[rumVÖ - 1], self.västTillÖst[rumVÖ + 1 - self.antalRum]))
            for rumNS in range(self.antalRum):
                if self.västTillÖst[rumVÖ] == self.norrTillSöder[rumNS]: #om rumsnumret är samma i västTillÖst som norrTillSöder adderas även info rummen till norr och söder
                    rumsLista[rumVÖ].rumNorrOchSöder(self.norrTillSöder[rumNS - 1], self.norrTillSöder[rumNS + 1 - self.antalRum])
                    break
        #skapar först instansobjekt utifrån västTillÖst där rummet höger om blir det till öster och vice versa
        #elementen i västTillÖst och norrTillSöder jämförs därefter för att kunna lägga till attributen tillNorr och tillSöder

        rumsLista.sort(key=operator.attrgetter("nummer")) #listan sorteras för att det ska gå att hålla koll på rummen, indexet är ett (1) mindre än rumsnummret

        rumMedFaror = random.sample(range(0, self.antalRum), int(self.antalRum*(self.fladdermöss+self.bottenlöstHål)/100))
        for rum in range(int(self.antalRum*self.fladdermöss/100)):
            rumsLista[rumMedFaror[rum]].fladdermöss = True
        for rum in range(int(self.antalRum*self.bottenlöstHål/100)):
            rumsLista[rumMedFaror[-rum-1]].bottenlöstHål = True #väljer rummen bakifrån

        self.rumsLista = rumsLista

    ####

    def spelSlingan(self): #själva spelslingan som körs till spelet har avslutats
        while not self.gameOver: #kör spelet så länge self.gameOver == False
            self.föregåendeRum = self.aktivtRum
            self.spelBakgrund()
            self.inputSlingaVal()
            #det som händer efter användaren har avslutat input-loopen
            self.valGå()
            self.valSkjuta()
            self.valAvsluta()
            if self.resultat == None:
                self.wumpusFörflyttas()
        if self.resultat != "Avslutat": #om spelet inte avslutades för tidigt      
            self.slutSkärm() #kör slutskärmen

    def spelBakgrund(self): #printar all bakgrund som behövs när spelet spelas (inga animationer)
        if self.antalDrag > 0:
            varnaSpelare(self.fönster, self.spelInfo, self.svårighetsgrad)
        #blitar all information som inte behöver uppdateras när ingen input sker, dvs allt förutom knapparna
        bakgrund(self.fönster, self.spelInfo)
        printaUtgångarRum(self.fönster, self.spelInfo, self.aktivtRum, self.rumsLista)
        self.kollaEfterFaror()
        printaText(self.fönster, self.farorText, 50, 510, 18, self.spelInfo.svart, self.spelInfo.brun[0]) #printar farorna
        self.fönster.blit(self.spelInfo.bild["spelare"], self.spelInfo.spelareKoordinater) #blitar spelaren
        printaText(self.fönster, ("        Drag   -   " + str(self.antalDrag) + "        \n" + " "*34 + "\n   Pilar   -                   "), 530, 150, 25, self.spelInfo.svart, self.spelInfo.brun[0])
        self.kvarvarandePilar()
        
    def inputSlingaVal(self): #slingan som körs när man väntar på spelarens input
        while True:
            self.riktningsTangent, self.skjutaTangent = trycktaTangenter() #tittar om spelaren har tryckt på några knappar
            musPosition, klick = musInfo()                    
            self.trycktSkjuta = knapp(self.fönster, None, 575, 380, 120, 80, self.spelInfo.brun[0], self.spelInfo.brun[2], self.spelInfo.svart, musPosition, klick) #skapar en skjutknapp
            self.fönster.blit(self.spelInfo.bild["pilbåge"], (610, 395)) #lägger en pilbåge på skjutknappen
            self.trycktAvsluta = knapp(self.fönster, "Avsluta", 720, 0, 80, 50, self.spelInfo.brun[0], self.spelInfo.brun[2], self.spelInfo.svart, musPosition, klick) #avsluta-knapp
            if self.riktningsTangent != None or self.trycktSkjuta or self.skjutaTangent or self.trycktAvsluta:
                break
            nyBildOchStängaAv(1, True, self.spelInfo)

    def valGå(self): #det som händer om spelaren har valt att gå
        if self.riktningsTangent != None: #om spelaren har valt att gå
            self.aktivtRum = spelarenGår(self.fönster, self.spelInfo, self.riktningsTangent, self.rumsLista, self.aktivtRum)
            self.antalDrag += 1
            if self.rumsLista[self.aktivtRum].fladdermöss: #om spelaren är i ett rum med fladdermöss
                self.aktivtRum = fladdermössÖvergång(self.fönster, self.spelInfo, self.rumsLista, self.aktivtRum) #kör animationen och väljer nytt rum
            elif self.rumsLista[self.aktivtRum].bottenlöstHål: #om spelaren är i ett rum med ett bottenlösthål
                bottenlöstHålAnimation(self.fönster, self.spelInfo) #spelar animationen
                self.gameOver = True
                self.resultat = "Ramlade"
            elif self.rumsLista[self.aktivtRum].wumpus: #om spelaren är i rummet med wumpus
                wumpusAnimation(self.fönster, self.spelInfo) #spelar animationen
                self.gameOver = True
                self.resultat = "Uppäten"

    def valSkjuta(self): #det som händer när spelaren har valt att skjuta
        if self.trycktSkjuta or self.skjutaTangent: #man kan skjuta genom att klicka på knappen eller trycka på space
            self.skjuta() #kör skjut-funktionen
            self.antalPilar -= 1 #tar bort en pil och lägger till ett drag
            self.antalDrag += 1
            if self.antalPilar == 0 and self.resultat == None: #om spelaren får slut på pilar avslutas spelet
                self.gameOver = True
                self.resultat = "Slut på pilar"

    def valAvsluta(self): #avslutar spelet i förtid
        if self.trycktAvsluta:
            self.gameOver = True
            self.resultat = "Avslutat"

    def wumpusFörflyttas(self): #wumpus byter rum på de svårare svårighetsgraderna
        if self.svårighetsgrad != "Lätt" and self.svårighetsgrad != "Medel":
            
            if self.svårighetsgrad == "Svårt": #wumpus byter rum (randomly)
                self.wumpusRum = self.rumsLista[self.wumpusRum].wumpusGår(self.aktivtRum, self.rumsLista)
                
            elif self.svårighetsgrad == "Omöjligt": #wumpus flyttar sig närmre spelaren
                if self.rumsLista[self.föregåendeRum].fladdermöss: #om spelaren blev flyttad av fladderöss går wumpus mot det nya rummet
                    self.wumpusRum = self.rumsLista[self.wumpusRum].wumpusGårNärmre(self.aktivtRum, self.rumsLista, self.västTillÖst, self.norrTillSöder)
                    
                else: #annars går wumpus mot det rummet man befann sig i (eller befinner sig i om man skjöt)
                    self.wumpusRum = self.rumsLista[self.wumpusRum].wumpusGårNärmre(self.föregåendeRum, self.rumsLista, self.västTillÖst, self.norrTillSöder)
                    
                if self.rumsLista[self.aktivtRum].wumpus: #om wumpus kommer in i spelarens rum
                    bakgrund(self.fönster, self.spelInfo)
                    self.fönster.blit(self.spelInfo.bild["spelare"], (235, 370))
                    vänta(2, True, self.spelInfo)
                    wumpusAnimation(self.fönster, self.spelInfo) #spelar animationen
                    self.resultat = "Surprise!" #spelaren förlorar
                    self.gameOver = True

    def kvarvarandePilar(self): #blitar hur många pilar som finns kvar
        for pilar in range(self.antalPilar):
            self.fönster.blit(self.spelInfo.bild["pilRoterad"], ((650 + (pilar * 20)), 220))
    ####
        
    def skjuta(self): #spelaren får skjuta en pil som åker igenom tre rum, där en riktning får väljas i varje rum
        self.pilRumsnummer = self.aktivtRum #pilen börjar i det rummet spelaren befinner sig i
        self.ordning = ["första", "andra", "tredje"] #för att det ska stå lämnar första, andra, tredje rummet

        for försök in range(3): #körs tre gånger
            self.skjutaBakgrund(försök)
            self.inputSlingaSkjuta()
            self.nyttPilRumsnummer(försök)
            
            if self.pilRumsnummer == self.aktivtRum: #om spelaren skjuter sig själv
                self.gameOver = True
                spelareSkjutenAnimation(self.fönster, self.spelInfo, self.pilRiktningsTangent) #kör animationen
                self.resultat = "Självmord"
                break
            elif self.pilRumsnummer == self.wumpusRum: #om spelaren skjuter wumpus
                self.gameOver = True
                wumpusSkjutenAnimation(self.fönster, self.spelInfo, self.pilRiktningsTangent) #kör animationen
                self.resultat = "WumpusDöd"
                break
            elif försök == 2: #om spelaren inte träffade någonting
                self.gameOver = False
                bakgrund(self.fönster, self.spelInfo)
                self.fönster.blit(self.spelInfo.bild["spelare"], self.spelInfo.spelareKoordinater)
                printaText(self.fönster, "Pilen träffade ingenting", 50, 510, 18, self.spelInfo.svart, self.spelInfo.brun[0]) #printar att pilen inte träffade någonting
                vänta(2, True, self.spelInfo)
                self.resultat = None
                
    def skjutaBakgrund(self, försök): #printar bakgrunden som behövs när spelaren skjuter (spelar roll vilket försök det är)
        bakgrund(self.fönster, self.spelInfo)
        printaUtgångarVäderStreck(self.fönster, self.spelInfo)
        printaText(self.fönster, "Pilen lämnar " + str(self.ordning[försök]) + " rummet. Vilken riktning?", 50, 510, 18, self.spelInfo.svart, self.spelInfo.brun[0]) #printar vilket rum pilen lämnar
        if försök == 0: #innan pilen har lämnat rummet blitas spelaren i mitten
            self.fönster.blit(self.spelInfo.bild["spelare"], self.spelInfo.spelareKoordinater)
        pygame.display.update()

    def inputSlingaSkjuta(self): #slingan som körs när spelet väntar på att spelaren väljer riktning
        while True:
            self.pilRiktningsTangent, self.pilMellanslagTangent = trycktaTangenter() #tittar om spelaren har tryckt på några knappar
            nyBildOchStängaAv(1, False, self.spelInfo)
            if self.pilRiktningsTangent != None:
                break
        

    def nyttPilRumsnummer(self, försök): #kör en animation och byter pilRumsnummer
        skjutaAnimation(self.fönster, self.spelInfo, self.pilRiktningsTangent, försök) #animationen körs
        if self.pilRiktningsTangent == "V":
            self.pilRumsnummer = self.rumsLista[self.pilRumsnummer].tillVäst - 1
        elif self.pilRiktningsTangent == "N":
            self.pilRumsnummer = self.rumsLista[self.pilRumsnummer].tillNorr - 1
        elif self.pilRiktningsTangent == "S":
            self.pilRumsnummer = self.rumsLista[self.pilRumsnummer].tillSöder - 1
        elif self.pilRiktningsTangent == "Ö":
            self.pilRumsnummer = self.rumsLista[self.pilRumsnummer].tillÖst - 1
        
    ####
    
    def kollaEfterFaror(self): #skapar en text beroende på vilka faror som ligger i närheten
        faror = ""
        if self.rumsLista[self.rumsLista[self.aktivtRum].tillÖst - 1].fladdermöss or self.rumsLista[self.rumsLista[self.aktivtRum].tillVäst - 1].fladdermöss or self.rumsLista[self.rumsLista[self.aktivtRum].tillNorr - 1].fladdermöss or self.rumsLista[self.rumsLista[self.aktivtRum].tillSöder - 1].fladdermöss:
            faror += "Du hör fladdermöss!\n" #Kollar efter fladdermöss i närheten
        if self.rumsLista[self.rumsLista[self.aktivtRum].tillÖst - 1].bottenlöstHål or self.rumsLista[self.rumsLista[self.aktivtRum].tillVäst - 1].bottenlöstHål or self.rumsLista[self.rumsLista[self.aktivtRum].tillNorr - 1].bottenlöstHål or self.rumsLista[self.rumsLista[self.aktivtRum].tillSöder - 1].bottenlöstHål:
            faror += "Du känner vinddrag!\n" #Kollar efter hål i närheten
        if self.rumsLista[self.rumsLista[self.aktivtRum].tillÖst - 1].wumpus or self.rumsLista[self.rumsLista[self.aktivtRum].tillVäst - 1].wumpus or self.rumsLista[self.rumsLista[self.aktivtRum].tillNorr - 1].wumpus or self.rumsLista[self.rumsLista[self.aktivtRum].tillSöder - 1].wumpus:
            faror += "Du känner lukten av wumpus!" #Kollar om wumpus är i närheten

        self.farorText = faror

    ####
        
    def slutSkärm(self): #visar slutskärmen, dvs ger info om spelaren vann eller förlorade och hur det gick till
        self.skapaResultatText()
        self.visaResultat()
        if self.resultat == "WumpusDöd": #om spelaren vann så kollas det om det var ett nytt highscore
            self.jämföraHighscore()

    def skapaResultatText(self):
        if self.resultat == "Slut på pilar":
            text = "    GAME OVER\n\n    Du förlorade genom att få slut på pilar."
            text += "\n\n    Du förlorade på " + str(self.antalDrag) + " drag."
            text += "\n\n    Du befann dig i rum " + str(self.rumsLista[self.aktivtRum].nummer) + " medan wumpus\n    befann sig i rum " + str(self.rumsLista[self.wumpusRum].nummer) + "."
        elif self.resultat == "Ramlade":
            text = "    GAME OVER\n\n    Du föll ner i ett bottenlöst hål."
            text += "\n\n    Du förlorade på " + str(self.antalDrag) + " drag."
            text += "\n\n    Du dog i rum " + str(self.rumsLista[self.aktivtRum].nummer) + " medan wumpus\n    befann sig i rum " + str(self.rumsLista[self.wumpusRum].nummer) + "."
        elif self.resultat == "Uppäten":
            text = "    GAME OVER\n\n    Du blev uppäten av Wumpus."
            text += "\n\n    Du förlorade på " + str(self.antalDrag) + " drag."
            text += "\n\n    Du gick in i rum " + str(self.rumsLista[self.aktivtRum].nummer) + "\n    där wumpus befann sig."
        elif self.resultat == "Surprise!":
            text = "    GAME OVER\n\n    Du blev uppäten av Wumpus."
            text += "\n\n    Du förlorade på " + str(self.antalDrag) + " drag."
            text += "\n\n    Wumpus gick in i rum " + str(self.rumsLista[self.aktivtRum].nummer) + "\n    där du befann dig."
        elif self.resultat == "Självmord":
            text = "    GAME OVER\n\n    Du sköt dig själv."
            text += "\n\n    Du förlorade på " + str(self.antalDrag) + " drag."
            text += "\n\n    Du befann dig i rum " + str(self.rumsLista[self.aktivtRum].nummer) + "\n    när du blev träffad."
        elif self.resultat == "WumpusDöd": #om spelaren vann
            text = "    Grattis!\n\n    Du vann genom att skjuta Wumpus \n    som befann sig i rum " + str(self.rumsLista[self.wumpusRum].nummer) + "."
            text += "\n\n    Det tog dig " + str(self.antalDrag) + " drag."
            text += "\n\n    Du befann dig i rum " + str(self.rumsLista[self.aktivtRum].nummer) + " när du vann."

        text += "\n\n    Svårighetsgrad: " + self.svårighetsgrad.upper()
        self.resultatText = text

    def visaResultat(self): #printar resultatet som skapades
        self.fönster.blit(self.spelInfo.bild["stjärnhimmel"], (0, 0))
        printaText(self.fönster, self.resultatText, 150, 100, 30, self.spelInfo.vit, self.spelInfo.lila[0])
        vänta(6, True, self.spelInfo)
        
    def jämföraHighscore(self): #tittar om spelaren fick ett nytt highscore
        data = open(os.getcwd() + "//Highscores//Highscore" + self.svårighetsgrad + ".txt", "r") #öppnar och läser highscore-filen
        self.highscore = data.read().split()
        data.close()

        for score in range(len(self.highscore)):
            self.highscore[score] = int(self.highscore[score]) #gör om alla element till int från str

        if self.antalDrag < self.highscore[-1]: #om antalet drag är mindre än minst ett resultat i highscorefilen
            self.nyttHighscore()

    def nyttHighscore(self):

        self.skapaNyttHighscoreText()
        self.fönster.blit(self.spelInfo.bild["stjärnhimmel"], (0, 0))
        printaText(self.fönster, self.nyttHighscoreText, 230, 50, 25, self.spelInfo.vit, self.spelInfo.lila[0]) #printar highscore-listan
        vänta(4, True, self.spelInfo)
            
        del self.highscore[-1] #ta bort förra sista highscore
        self.highscore.append(self.antalDrag) #lägg till nya
        self.highscore.sort()

        data = open(os.getcwd() + "\\Highscores\\Highscore" + self.svårighetsgrad + ".txt", "w") #öppnar highscore-filen så att den kan skrivas till
        for score in self.highscore: #skriver den nya uppdaterade highscore-filen
            data.write(str(score) + "\n")
        data.close()

    def skapaNyttHighscoreText(self): #skapar texten som ska printas
        text = "    Nytt highscore!"
        for resultat in range(len(self.highscore)):
            text += "\n\n    " + str(resultat + 1) + "." + " "*18 + str(self.highscore[resultat]) + " drag"
        text += "\n\n    Ditt score    " + str(self.antalDrag) + " drag"

        self.nyttHighscoreText = text

#varje instansobjekt får information om faror och närliggande rum
class Rum: #en klass för rummen man kan gå mellan

    def __init__(self, rumsnummer, tillVäst, tillÖst):
        self.nummer = rumsnummer
        self.tillÖst = tillÖst
        self.tillVäst = tillVäst
        self.fladdermöss = False
        self.bottenlöstHål = False
        self.wumpus = False

    def rumNorrOchSöder(self, tillNorr, tillSöder):
        self.tillNorr = tillNorr
        self.tillSöder = tillSöder

    def slumpmässigtRum(self, rumsLista): #väljer ett nytt slumpmässigt rum där inga faror finns
        while True:
            slumpmässigttal = random.randint(0, len(rumsLista) - 1)
            #OBS! If-satserna nedan hade kunnats göras om till en enda if-sats, men det här blir tydligare
            if not rumsLista[slumpmässigttal].fladdermöss:
                if not rumsLista[slumpmässigttal].bottenlöstHål:
                    if not rumsLista[slumpmässigttal].wumpus:
                        if slumpmässigttal != self.nummer - 1: #det rummet som man utgick ifrån
                            break
        
        return slumpmässigttal #returnerar det nya rumsnummret

    def wumpusGår(self, aktivtRum, rumsLista): #wumpus går ett steg i en random riktning, men inte in i spelarens rum, därför behövs rumsListan och spelarens rumsnummer

        riktning = random.sample(range(4), 4)
        nyttWumpusRum = self.nummer - 1 # om han inte kan flytta på sig

        for i in range(4): #gör en loop så att wumpus får större chans att gå
            if riktning[i] == 0 and not rumsLista[self.tillÖst - 1].bottenlöstHål and self.tillÖst - 1 != aktivtRum: 
                nyttWumpusRum = self.tillÖst - 1 #rummets index i rumsLista är ett lägre än rummets nummer
                break
            elif riktning[i] == 1 and not rumsLista[self.tillVäst - 1].bottenlöstHål and self.tillVäst - 1 != aktivtRum: 
                nyttWumpusRum = self.tillVäst - 1 #rummets index i rumsLista är ett lägre än rummets nummer
                break
            elif riktning[i] == 2 and not rumsLista[self.tillSöder - 1].bottenlöstHål and self.tillSöder - 1 != aktivtRum: 
                nyttWumpusRum = self.tillSöder - 1 #rummets index i rumsLista är ett lägre än rummets nummer
                break
            elif riktning[i] == 3 and not rumsLista[self.tillNorr - 1].bottenlöstHål and self.tillNorr - 1 != aktivtRum: 
                nyttWumpusRum = self.tillNorr - 1 #rummets index i rumsLista är ett lägre än rummets nummer
                break
            
        if nyttWumpusRum == self.nummer - 1: #om han var omringad av hål och därmed inte kunde gå
            nyttWumpusRum = rumsLista[nyttWumpusRum].slumpmässigtRum(rumsLista, nyttWumpusRum)
        self.wumpus = False #tas bort från det förra numret
        rumsLista[nyttWumpusRum].wumpus = True
        rumsLista[nyttWumpusRum].fladdermöss = False #wumpus flyttas och om det finns fladdermöss i rummet äter han dem

        return nyttWumpusRum #retunerar det nya rummet wumpus befinner sig i

    def wumpusGårNärmre(self, aktivtRum, rumsLista, västTillÖst, norrTillSöder): #wumpusgår ett rum i den riktning som är närmst spelaren, om det inte är ett hål, därför behövs rumsListan och spelarens rumsnummer
        
        nyttWumpusRum = self.nummer - 1 #behövs ifall han inte kan flytta på sig
        
        for rum in range(len(rumsLista)): #hittar positionerna i västTillÖst och norrTillSöder
            if västTillÖst[rum] ==  rumsLista[aktivtRum].nummer:
                aktivtRumÖV = rum
            if västTillÖst[rum] ==  self.nummer:
                wumpusRumÖV = rum
            if norrTillSöder[rum] ==  rumsLista[aktivtRum].nummer:
                aktivtRumNS = rum
            if norrTillSöder[rum] ==  self.nummer:
                wumpusRumNS = rum

        #tittar om wumpus befinner sig österut eller inte
        wumpusTillÖst = True
        if aktivtRumÖV > wumpusRumÖV:
            wumpusTillÖst = False

        #beräknar avståndet i öst- och västled beroende på om wumpus befann sig till öst eller inte
        if not wumpusTillÖst:
            avståndÖst = aktivtRumÖV - wumpusRumÖV
            avståndVäst = len(rumsLista) - aktivtRumÖV + wumpusRumÖV #20 - aktivtrum ger avståndet till högra kanten av listan, därför måste man lägga på wumpusRummet
        else:
            avståndÖst = len(rumsLista) - wumpusRumÖV + aktivtRumÖV #20 - aktivtrum ger avståndet till högra kanten av listan, därför måste man lägga på wumpusRummet
            avståndVäst = wumpusRumÖV - aktivtRumÖV
    
        #tittar om wumpus befinner sig söderut eller inte
        wumpusTillSöder = False
        if aktivtRumNS < wumpusRumNS:
            wumpusTillSöder = True
            
        #beräknar avståndet i nord- och söderled beroende på om wumpus befann sig söderut eller inte
        if not wumpusTillSöder:
            avståndSöder = aktivtRumNS - wumpusRumNS
            avståndNorr = len(rumsLista) - aktivtRumNS + wumpusRumNS #20 - aktivtrum ger avståndet till högra kanten av listan, därför måste man lägga på wumpusRummet
        else:
            avståndSöder = len(rumsLista) - wumpusRumNS + aktivtRumNS #20 - aktivtrum ger avståndet till högra kanten av listan, därför måste man lägga på wumpusRummet
            avståndNorr = wumpusRumNS - aktivtRumNS 

        #sorterar avstånden efter storlek
        ordningAvstånd = [avståndÖst, avståndVäst, avståndNorr, avståndSöder]
        ordningAvstånd.sort()
        
        #letar efter avståndet som är kortast
        #därefter går wumpus ett steg i den riktningen om det inte finns ett hål där
        for avstånd in range(len(ordningAvstånd)):
            
            if ordningAvstånd[avstånd] == avståndÖst and not rumsLista[self.tillÖst - 1].bottenlöstHål: 
                nyttWumpusRum = self.tillÖst - 1 #rummets index i rumsLista är ett lägre än rummets nummer
                break
            elif ordningAvstånd[avstånd] == avståndVäst and not rumsLista[self.tillVäst - 1].bottenlöstHål: 
                nyttWumpusRum = self.tillVäst - 1 #rummets index i rumsLista är ett lägre än rummets nummer
                break
            elif ordningAvstånd[avstånd] == avståndSöder and not rumsLista[self.tillSöder - 1].bottenlöstHål: 
                nyttWumpusRum = self.tillSöder - 1 #rummets index i rumsLista är ett lägre än rummets nummer
                break
            elif ordningAvstånd[avstånd] == avståndNorr and not rumsLista[self.tillNorr - 1].bottenlöstHål: 
                nyttWumpusRum = self.tillNorr - 1 #rummets index i rumsLista är ett lägre än rummets nummer
                break

        if nyttWumpusRum == self.nummer - 1: #om han var omringad av hål och därmed inte kunde gå
            nyttWumpusRum = self.slumpmässigtRum(rumsLista)
        self.wumpus = False #tas bort från det förra rummet
        rumsLista[nyttWumpusRum].wumpus = True
        rumsLista[nyttWumpusRum].fladdermöss = False #wumpus flyttas och om det finns fladdermöss i rummet äter han dem

        return nyttWumpusRum #retunerar det nya rummet wumpus befinner sig i
