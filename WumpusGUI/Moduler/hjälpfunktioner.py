import pygame, os, signal, random
from pygame.locals import *

#Vissa funktioner har fönster och spelInfo som argument då de inte defineras i denna modul
def printaText(fönster, meddelande, xKord, yKord, storlek, färg, bakgrundsfärg): #printar text, på valda koordinater med en specifik färg och storlek

    ursprungsXKord = xKord
    rader = [rad for rad in meddelande.splitlines()] #gör en lista med varje rad av en text som element
    font = pygame.font.SysFont("comicsansms", storlek)

    for rad in rader:
        radYta = font.render(rad, 0, färg) #hämtar ytan av raden som ska printas
        radBredd, radHöjd = radYta.get_size() #delar upp ytan i x- o y-led

        if bakgrundsfärg != None:
            pygame.draw.rect(fönster, bakgrundsfärg, (xKord, yKord, radBredd, radHöjd)) #ritar rektangeln bakom texten
        fönster.blit(radYta, (xKord, yKord)) #ritar rektangeln med texten på samma plats

        xKord = ursprungsXKord #nollställer xKord
        yKord += radHöjd #hoppar till nästa rad

def textCentrerad(fönster, meddelande, xKord, yKord, bredd, höjd, färg, bakgrundsfärg): #gör en textruta med texten centrerad, samma som ovan fast med angivna dimensioner

    pygame.draw.rect(fönster, bakgrundsfärg, (xKord, yKord, bredd, höjd)) #ritar bakgrunden
    font = pygame.font.SysFont("comicsansms", 20) #bestämmer font och storlek på texten
    text = font.render(meddelande, True, färg) #rendrar texten med den angivna färgen
    textRektangel = text.get_rect() #får dimensionerna på texten
    textRektangel.center = ((xKord + (bredd / 2)), (yKord + (höjd / 2))) #centrerar texten i mitten av rektangeln
    fönster.blit(text, textRektangel) #blitar texten

def knapp(fönster, meddelande, xKord, yKord, bredd, höjd, färg, hoverFärg, textFärg, musPosition, klick): #skapar en knapp
    #man får välja vilken text som står i den, var den ska ligga, vilken färg den ska  ha osv. musPosition och klick är för att se om användaren har klickat inom knappens ramar
    tryckt = False

    if xKord + bredd > musPosition[0] > xKord and yKord + höjd > musPosition[1] > yKord: #om musen befinner sig innanför rektangeln ritar den med hoverfärgen
        pygame.draw.rect(fönster, hoverFärg, (xKord, yKord, bredd, höjd))
        if klick[0]: #om musen dessutom har klickats retuneras tryckt = True
            tryckt = True
    else:
        pygame.draw.rect(fönster, färg, (xKord, yKord, bredd, höjd)) #ritar rektangeln med den vanliga färgen när musen inte befinner sig inom området
    
    font = pygame.font.SysFont("comicsansms", 20) #bestämmer font och storlek på texten
    text = font.render(meddelande, True, textFärg) #rendrar texten med den angivna färgen
    textRektangel = text.get_rect() #får dimensionerna på texten
    textRektangel.center = ((xKord + (bredd / 2)), (yKord + (höjd / 2))) #centrerar texten i mitten av rektangeln
    fönster.blit(text, textRektangel) #blitar texten

    return tryckt #retunerar om man har tyrckt på knappen
        
def stängaAv(): #stänger ned programmet om användaren har klickat på [X]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            os.kill(os.getpid(), signal.SIGTERM)

def vänta(sekunder, uppdateraSkärm, spelInfo): #väntar en vis tid men låter användaren stänga fönstret samtidigt, och uppdaterar skärmen om så är specificerat

    if uppdateraSkärm:
        pygame.display.flip()
    for bilder in range(int(spelInfo.bps*sekunder)):
        stängaAv()
        spelInfo.klocka.tick(spelInfo.bps)

    pygame.event.clear() #tar bort onödig kvarvarande information

def nyBildOchStängaAv(hastighet, uppdateraSkärm, spelInfo): #gör så att spelaren kan stänga fönstret, håller fpsen, och uppdaterar skärmen om så är specificerat

    stängaAv()
    spelInfo.klocka.tick(spelInfo.bps*hastighet)
    if uppdateraSkärm:
        pygame.display.flip()

def trycktaTangenter(): #tittar efter de tangenter spelaren har tryckt på

    tangent = pygame.key.get_pressed()
    riktning = None
    mellanslag = None
    
    if tangent[K_LEFT] or tangent[K_a]:
        riktning = "V"
    if tangent[K_RIGHT] or tangent[K_d]:
        riktning = "Ö"
    if tangent[K_UP] or tangent[K_w]:
        riktning = "N"
    if tangent[K_DOWN] or tangent[K_s]:
        riktning = "S"
    if tangent[K_SPACE]:
        mellanslag = True
    
    return riktning, mellanslag #retunerar om användaren har tyrckt på någon av knapparna eller inte, och i så fall vilken riktning

def musInfo(): 

    musPosition = pygame.mouse.get_pos() #returnerar x- o y-koordinater för musen
    klick = pygame.mouse.get_pressed() #returnerar data om musen, [0] ger leftclick

    return musPosition, klick #retunerar position och klick info
