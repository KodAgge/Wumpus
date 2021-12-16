import pygame, time
from hjälpfunktioner import *

#Alla funktioner har fönster och spelInfo som argument för att ha nödvändig info
def bakgrund(fönster, spelInfo): #en funktion som blitar spelbakgrunden

    fönster.blit(spelInfo.bild["golv"], (0, 0))

    #gör utgångarna
    pygame.draw.rect(fönster, spelInfo.brun[0], (0, 230, 50, 40))
    pygame.draw.rect(fönster, spelInfo.brun[0], (450, 230, 50, 40))
    pygame.draw.rect(fönster, spelInfo.brun[0], (230, 0, 40, 50))
    pygame.draw.rect(fönster, spelInfo.brun[0], (230, 450, 40, 50))

def delBakgrund(fönster, spelInfo): #en funktion som blitar den del av bakgrunden spelaren går på, så att inte lika mkt behöver uppdateras varje frame

    fönster.blit(spelInfo.bild["delGolv"], (0, 0))

    #gör utgångarna
    pygame.draw.rect(fönster, spelInfo.brun[0], (0, 230, 50, 40))
    pygame.draw.rect(fönster, spelInfo.brun[0], (450, 230, 50, 40))
    pygame.draw.rect(fönster, spelInfo.brun[0], (230, 0, 40, 50))
    pygame.draw.rect(fönster, spelInfo.brun[0], (230, 450, 40, 50))

def gåInIRum(fönster, spelInfo, hastighet): #en övergång när man byter rum, printar en skala av grått
    #hastigheten ändrar hur snabbt övergången går
    
    gråSkala = [(26, 26, 26), (51, 51, 51), (77, 77, 77), (102, 102, 102), (128, 128, 128), (166, 166, 166), (204, 204, 204), (242, 242, 242)]
    bakgrund(fönster, spelInfo)
    for nyans in range(len(gråSkala)): #fyller spelrutan med de olika färgerna i gråskalan
        pygame.draw.rect(fönster, gråSkala[nyans], (0, 0, 500, 500))
        pygame.display.flip()
        time.sleep((1/5) * (1/hastighet))

    pygame.event.clear()

def fladdermössÖvergång(fönster, spelInfo, rumsLista, aktivtRum): #lyfter spelaren ut ur rummet och släpper ner den i ett annat, behöver listan med rum och det aktiva rummet för att kunna välja ett nytt

    fladdermössRektangel = spelInfo.bild["fladdermöss"].get_rect() #hämtar dimensionerna
    fladdermössRektangel.center = (250, 250) #centrerar
    fladderX, fladderY = fladdermössRektangel[0], fladdermössRektangel[1] #startvärden (gör så att spelaren hamnar mitt i rummet)
    nyttRumsnummer = rumsLista[aktivtRum].slumpmässigtRum(rumsLista) #väljer ut det rummet spelaren ska släppas i
    
    while fladderX > -100: #fladdermössen drar spelaren upp till det övre vänsta hörnet
        delBakgrund(fönster, spelInfo)
        printaText(fönster, "Du känner fladdermusvingar mot kinden\noch lyfts uppåt.", 50, 510, 20, spelInfo.svart, spelInfo.brun[0])
        fönster.blit(spelInfo.bild["fladdermöss"], (fladderX, fladderY))
        fladderX -= 3/2*spelInfo.hastighet
        fladderY -= 3/2*spelInfo.hastighet
        nyBildOchStängaAv(2, True, spelInfo)
    
    gåInIRum(fönster, spelInfo,3) #lite snabbare animation

    while fladderX < 156: #fladdermössen släpper spelaren mitt i rummet från det övre vänstra hörnet
        delBakgrund(fönster, spelInfo)
        printaText(fönster, "Efter en kort flygtur släpper\nfladdermössen ner dig i rum " + str(rumsLista[nyttRumsnummer].nummer) + ".", 50, 510, 20, spelInfo.svart, spelInfo.brun[0])
        fönster.blit(spelInfo.bild["fladdermöss"], (fladderX, fladderY))
        fladderX += 3/2*spelInfo.hastighet
        fladderY += 3/2*spelInfo.hastighet
        nyBildOchStängaAv(2, True, spelInfo)

    vänta(1, False, spelInfo) #väntar en sekund

    return nyttRumsnummer #retunerar det nya aktivtRum

def wumpusAnimation(fönster, spelInfo): #en animation för när wumpus eller spelaren går in i varandras rum
    
    litenWumpusRektangel = spelInfo.bild["litenWumpus"].get_rect() #hämtar bildens dimensioner
    litenWumpusRektangel.center = (250, 250) #hämtar centeringsdata runt punkten 250, 250
    wumpusY = litenWumpusRektangel[1]

    #kommer in i rummet
    bakgrund(fönster, spelInfo)
    fönster.blit(spelInfo.bild["litenWumpus"], litenWumpusRektangel)
    fönster.blit(spelInfo.bild["spelare"], (235, 370))
    vänta(1, True, spelInfo)

    #spelaren märker wumpus
    delBakgrund(fönster, spelInfo)
    fönster.blit(spelInfo.bild["litenWumpus"], litenWumpusRektangel)
    fönster.blit(spelInfo.bild["spelare"], (235, 370))
    fönster.blit(spelInfo.bild["utropstecken"], (235, 335)) #blitar ett utropstecken över spelaren
    vänta(2, True, spelInfo)

    #wumpus springer till spelaren
    while wumpusY < 330:
        delBakgrund(fönster, spelInfo)
        fönster.blit(spelInfo.bild["spelare"], (235, 370))
        fönster.blit(spelInfo.bild["litenWumpus"], (litenWumpusRektangel[0], wumpusY))
        wumpusY += 2*spelInfo.hastighet
        nyBildOchStängaAv(2, True, spelInfo)

    vänta(1, False, spelInfo)

def bottenlöstHålAnimation(fönster, spelInfo): #animation för när spelaren faller ner i ett hål

    roteradSpelare = spelInfo.bild["spelare"] #sparar spelare-bilden till en annan så att den kan roteras och minskas
    bakgrund(fönster, spelInfo)
    
    for roteringar in range(45):
        pygame.draw.circle(fönster, spelInfo.svart, (250, 250), 200, 0) #blitar en cirkel som går från utgång till utgång
        roteradSpelare = pygame.transform.rotozoom(roteradSpelare, 2, 0.97) #roterar spelaren 2 grader och gör den 3 % mindre
        roteradSpelareRektangel = roteradSpelare.get_rect() #hämtar dimensions-info om den nya spelar-bilden så att den kan centreras
        roteradSpelareRektangel.center = (250, 250)
        fönster.blit(roteradSpelare, roteradSpelareRektangel)
        nyBildOchStängaAv(1*spelInfo.hastighet/4, True, spelInfo)

    pygame.event.clear() #för att få bort onödiga köande event

def wumpusSkjutenAnimation(fönster, spelInfo, riktning): #wumpus blir skjuten och dör, från vilket håll spelar roll

    litenWumpusRektangel = spelInfo.bild["litenWumpus"].get_rect() #hämtar dimensions-info
    litenWumpusRektangel.center = (250, 250) #centrerar

    #pilen lämnar en utgång beroende på vald utgång och flyger tills den träffar wumpus
    if riktning == "N":
        pilY = 430
        while pilY >= 250:
            delBakgrund(fönster, spelInfo)
            fönster.blit(spelInfo.bild["litenWumpus"], litenWumpusRektangel)
            fönster.blit(spelInfo.bild["pilNorr"], (240, pilY))
            pilY -= 3/2*spelInfo.hastighet
            nyBildOchStängaAv(2, True, spelInfo)

    if riktning == "V":
        pilX = 430
        while pilX >= 250:
            delBakgrund(fönster, spelInfo)
            fönster.blit(spelInfo.bild["litenWumpus"], litenWumpusRektangel)
            fönster.blit(spelInfo.bild["pilVäst"], (pilX, 240))
            pilX -= 3/2*spelInfo.hastighet
            nyBildOchStängaAv(2, True, spelInfo)

    if riktning == "S":
        pilY = 30
        while pilY <= 210:
            delBakgrund(fönster, spelInfo)
            fönster.blit(spelInfo.bild["litenWumpus"], litenWumpusRektangel)
            fönster.blit(spelInfo.bild["pilSyd"], (240, pilY))
            pilY += 3/2*spelInfo.hastighet
            nyBildOchStängaAv(2, True, spelInfo)

    if riktning == "Ö":
        pilX = 30
        while pilX <= 210:
            delBakgrund(fönster, spelInfo)
            fönster.blit(spelInfo.bild["litenWumpus"], litenWumpusRektangel)
            fönster.blit(spelInfo.bild["pilÖst"], (pilX, 240))
            pilX += 3/2*spelInfo.hastighet
            nyBildOchStängaAv(2, True, spelInfo)

    #wumpus blir sepia färgad
    delBakgrund(fönster, spelInfo)
    fönster.blit(spelInfo.bild["litenWumpusSkjuten"], litenWumpusRektangel)
    vänta(2, True, spelInfo)

    #wumpusliket tas bort
    delBakgrund(fönster, spelInfo)
    vänta(2, True, spelInfo)

def spelareSkjutenAnimation(fönster, spelInfo, riktning): #identisk till ovanstående animation förutom att wumpus är utbytt till spelaren

    if riktning == "N":
        pilY = 430
        while pilY >= 250:
            delBakgrund(fönster, spelInfo)
            fönster.blit(spelInfo.bild["spelare"], spelInfo.spelareKoordinater)
            fönster.blit(spelInfo.bild["pilNorr"], (240, pilY))
            pilY -= 3/2*spelInfo.hastighet
            nyBildOchStängaAv(2, True, spelInfo)

    if riktning == "V":
        pilX = 430
        while pilX >= 250:
            delBakgrund(fönster, spelInfo)
            fönster.blit(spelInfo.bild["spelare"], spelInfo.spelareKoordinater)
            fönster.blit(spelInfo.bild["pilVäst"], (pilX, 240))
            pilX -= 3/2*spelInfo.hastighet
            nyBildOchStängaAv(2, True, spelInfo)

    if riktning == "S":
        pilY = 30
        while pilY <= 250-spelInfo.bild["pilSyd"].get_height():
            delBakgrund(fönster, spelInfo)
            fönster.blit(spelInfo.bild["spelare"], spelInfo.spelareKoordinater)
            fönster.blit(spelInfo.bild["pilSyd"], (240, pilY))
            pilY += 3/2*spelInfo.hastighet
            nyBildOchStängaAv(2, True, spelInfo)

    if riktning == "Ö":
        pilX = 30
        while pilX <= 250-spelInfo.bild["pilÖst"].get_width():
            delBakgrund(fönster, spelInfo)
            fönster.blit(spelInfo.bild["spelare"], spelInfo.spelareKoordinater)
            fönster.blit(spelInfo.bild["pilÖst"], (pilX, 240))
            pilX += 3/2*spelInfo.hastighet
            nyBildOchStängaAv(2, True, spelInfo)

    delBakgrund(fönster, spelInfo)
    fönster.blit(spelInfo.bild["spelareSkjuten"], spelInfo.spelareKoordinater)
    vänta(2, True, spelInfo)

    delBakgrund(fönster, spelInfo)
    vänta(2, True, spelInfo)

def skjutaAnimation(fönster, spelInfo, riktning, genomSkjutnaRum): #animation för när pilen lämnar rummet beroende på vilken riktning som valdes

    #pilen lämnar mitten beroende på vilken riktning som valdes
    #om pilen befinner sig i första rummet kommer även spelaren blitas
    if riktning == "N":
        pilY = 250-spelInfo.bild["pilNorr"].get_height()-spelInfo.bild["spelare"].get_height()/2
        while pilY >= 50/2:
            delBakgrund(fönster, spelInfo)
            if genomSkjutnaRum == 0:
                fönster.blit(spelInfo.bild["spelare"], spelInfo.spelareKoordinater)
            fönster.blit(spelInfo.bild["pilNorr"], (240, pilY))
            pilY -= 3/2*spelInfo.hastighet
            nyBildOchStängaAv(2, True, spelInfo)

    if riktning == "V":
        pilX = 250-spelInfo.bild["pilVäst"].get_width()-spelInfo.bild["spelare"].get_width()/2
        while pilX >= 50/2:
            delBakgrund(fönster, spelInfo)
            if genomSkjutnaRum == 0:
                fönster.blit(spelInfo.bild["spelare"], spelInfo.spelareKoordinater)
            fönster.blit(spelInfo.bild["pilVäst"], (pilX, 240))
            pilX -= 3/2*spelInfo.hastighet
            nyBildOchStängaAv(2, True, spelInfo)

    if riktning == "S":
        pilY = 250+spelInfo.bild["spelare"].get_height()/2
        while pilY <= 500-spelInfo.bild["pilSyd"].get_height()-50/2:
            delBakgrund(fönster, spelInfo)
            if genomSkjutnaRum == 0:
                fönster.blit(spelInfo.bild["spelare"], spelInfo.spelareKoordinater)
            fönster.blit(spelInfo.bild["pilSyd"], (240, pilY))
            pilY += 3/2*spelInfo.hastighet
            nyBildOchStängaAv(2, True, spelInfo)

    if riktning == "Ö":
        pilX = 250+spelInfo.bild["spelare"].get_width()/2
        while pilX <= 500-spelInfo.bild["pilÖst"].get_width()-50/2:
            delBakgrund(fönster, spelInfo)
            if genomSkjutnaRum == 0:
                fönster.blit(spelInfo.bild["spelare"], spelInfo.spelareKoordinater)
            fönster.blit(spelInfo.bild["pilÖst"], (pilX, 240))
            pilX += 3/2*spelInfo.hastighet
            nyBildOchStängaAv(2, True, spelInfo)

    gåInIRum(fönster, spelInfo, 3)

def spelarenGår(fönster, spelInfo, riktningsTangent, rumsLista, aktivtRum): #får spelaren att gå och byter aktivtRum, behöver därför rumsListan, riktningen och det nuvarande rummet

    spelareX, spelareY = spelInfo.spelareKoordinater[0], spelInfo.spelareKoordinater[1]
    
    if riktningsTangent == "V":                        
        while spelareX >= 50/2:
            delBakgrund(fönster, spelInfo)
            fönster.blit(spelInfo.bild["spelareGårVäst"], (spelareX, spelareY))
            spelareX -= spelInfo.hastighet
            nyBildOchStängaAv(2, True, spelInfo)
        gåInIRum(fönster, spelInfo, 2)
        aktivtRum = rumsLista[aktivtRum].tillVäst - 1

    elif riktningsTangent == "N":
        while spelareY >= 50/2:
            delBakgrund(fönster, spelInfo)
            fönster.blit(spelInfo.bild["spelareGårNorr"], (spelareX, spelareY))
            spelareY -= spelInfo.hastighet
            nyBildOchStängaAv(2, True, spelInfo)
        gåInIRum(fönster, spelInfo, 2)
        aktivtRum = rumsLista[aktivtRum].tillNorr - 1

    elif riktningsTangent == "S":
        while spelareY <= 500-spelInfo.bild["spelare"].get_height()-50/2: #-höjden av karaktären minus halva öppningen
            bakgrund(fönster, spelInfo)
            fönster.blit(spelInfo.bild["spelareGårSyd"], (spelareX, spelareY))
            spelareY += spelInfo.hastighet
            nyBildOchStängaAv(2, True, spelInfo)
        gåInIRum(fönster, spelInfo, 2)
        aktivtRum = rumsLista[aktivtRum].tillSöder - 1

    elif riktningsTangent == "Ö":
        while spelareX <= 500-spelInfo.bild["spelare"].get_width()-50/2:#-bredden av karaktären minus halva öppningen
            bakgrund(fönster, spelInfo)
            fönster.blit(spelInfo.bild["spelareGårÖst"], (spelareX, spelareY))
            spelareX += spelInfo.hastighet
            nyBildOchStängaAv(2, True, spelInfo)
        gåInIRum(fönster, spelInfo, 2)
        aktivtRum = rumsLista[aktivtRum].tillÖst - 1

    return aktivtRum #retunerar det rummet spelaren gick in i

def printaUtgångarRum(fönster, spelInfo, aktivtRum, rumsLista): #numrerar utgånarna utifrån vilket rum man befinner sig i
    
    textCentrerad(fönster, str(rumsLista[aktivtRum].tillVäst), 0, 230, 50, 40, spelInfo.svart, spelInfo.brun[0])
    textCentrerad(fönster, str(rumsLista[aktivtRum].tillNorr), 230, 0, 40, 50, spelInfo.svart, spelInfo.brun[0])
    textCentrerad(fönster, str(rumsLista[aktivtRum].tillSöder), 230, 450, 40, 50, spelInfo.svart, spelInfo.brun[0])
    textCentrerad(fönster, str(rumsLista[aktivtRum].tillÖst), 450, 230, 50, 40, spelInfo.svart, spelInfo.brun[0])

def printaUtgångarVäderStreck(fönster, spelInfo): #ger utgångarna väderstreck
    
    textCentrerad(fönster, "V", 0, 230, 50, 40, spelInfo.svart, spelInfo.brun[0])
    textCentrerad(fönster, "N", 230, 0, 40, 50, spelInfo.svart, spelInfo.brun[0])
    textCentrerad(fönster, "S", 230, 450, 40, 50, spelInfo.svart, spelInfo.brun[0])
    textCentrerad(fönster, "Ö", 450, 230, 50, 40, spelInfo.svart, spelInfo.brun[0])
        
def varnaSpelare(fönster, spelInfo, svårighetsgrad): #varnar spelarna på de högre svårighetsgradern
    
    if svårighetsgrad != "Medel" and svårighetsgrad != "Lätt": #varnar spelaren efter den har gjort ett drag, gör spelet läskigare
        bakgrund(fönster, spelInfo)
        if svårighetsgrad == "Svårt":
            printaText(fönster, "Wumpus byter rum...", 50, 510, 20, spelInfo.svart, spelInfo.brun[0])
        elif svårighetsgrad == "Omöjligt":
            printaText(fönster, "Wumpus närmar sig!", 50, 510, 20, spelInfo.svart, spelInfo.brun[0])
        fönster.blit(spelInfo.bild["spelare"], spelInfo.spelareKoordinater)
        vänta(2, True, spelInfo)
