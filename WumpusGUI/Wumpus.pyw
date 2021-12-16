import pygame, sys, os
sys.path.append(os.getcwd() + "//Moduler") #gör så att moduler kan importeras från en annan mapp
from menyfunktioner import *

def main(): #startar pygame, öppnar fönstret och kallar därefter på huvudmenyn
    pygame.init()
    pygame.display.set_caption("Wumpus TM v0.9.8 [BETA]") #döper fönstret till Wumpus
    huvudSkärm = pygame.display.set_mode((800, 600)) #öppnar pygame fönstret
    spelInfo = SpelInfo()
    meny = Huvudmeny(huvudSkärm, spelInfo)
    while True:
         meny.startmeny() #kallar på startmenyn

main()
