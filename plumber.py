# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 21:45:02 2018

@author: Ania
"""

import pygame, sys, math, copy, random

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.mixer.init()
pygame.init()
random.seed(8)
myfont = pygame.font.SysFont("ariblk", 40)
screen_h = 800
screen_w = 700
klocek_bok = 70

rx = 70
ry= 150

win = pygame.display.set_mode((screen_h,screen_w))
pygame.display.set_caption("Plumber")

#obrazek tła
tlo = pygame.image.load("tlo.png")
wylot_im = pygame.image.load("wylot.png")
tlo_menu = pygame.image.load("tlo_menu.png")
#obrazki klocków           
kolanko_image = [pygame.image.load('UR.png'), pygame.image.load('BR.png'),\
                 pygame.image.load('BL.png'),pygame.image.load('UL.png')]
rura_image = [pygame.image.load('poziom.png'),pygame.image.load('pion.png')]
pusty_image = [pygame.image.load('pusty.png')]
#obrazki przycisków
start_button = pygame.image.load("start.png")
dalej_button = pygame.image.load("dalej.png")
wyjdz_button = pygame.image.load("wyjdz.png")
menu_button = pygame.image.load("menu.png")
powtorz_button = pygame.image.load("powtorz.png")
powrot_button = pygame.image.load("powrot.png")

muzyka_button = [pygame.image.load("muzyka_on.png"), pygame.image.load("muzyka_off.png")]

#rozmiar przycisku (wszystkie są takich samych rozmiarów)
button = start_button.get_size() #(width, height)

# muzyka i dźwięki 
rotationSound = pygame.mixer.Sound("click.wav")
music = pygame.mixer.music.load("music.mp3")
pygame.mixer.music.set_volume(0.2) # między 0, a 1
pygame.mixer.music.play(-1) #powtarzamy nieksonczenie wiele razy muzyczkę

isMusic = True

    
class level():
    def __init__(self, klocki, szer, wys):
        self.klocki = klocki
        self.szer = szer
        self.wys = wys
        self.rozmiar = wys*szer



class rura(object):
    def __init__(self, size, obrazki, up, down, left, right, opcja, pozycja):
        self.size = size
        self.obrazki = obrazki
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.pozycja = pozycja
        self.image = self.obrazki[pozycja]
        self.opcja = opcja #opcja- 1 kolanko, 2 rura, 3 pusty
        
    def draw(self, miejsce, win): #dla tablicy bokXxbokX, trzeba uogólnić później
        if(miejsce//bokX == miejsce /bokX ):
            i= poz//bokX
        else:
            i=miejsce//bokX + 1
        j= miejsce-(i-1)*bokX
        x = (j-1)*klocek_bok + rx
        y = (i-1)*klocek_bok + ry       
        win.blit(self.image, (x,y ))
        
    def polaczenia(self, miejsce):
        wloty = []
        if(miejsce//bokX == miejsce /bokX ): #czyli jest położony w ostatniej kolumnie
            i= miejsce//bokX
        else:
            i=miejsce//bokX + 1
        j= miejsce-(i-1)*bokX
        
        
        if (self.right == True):
            if (j<bokX):  # j< bokX
                wloty.append(miejsce + 1) #miejsce + 1
            else:
                wloty.append(0)
                
        if(self.up == True):
            if( i > 1):
                wloty.append(miejsce - bokX) # miejsce - bokX
            else:
                wloty.append(0)
                
        if (self.left == True):
                if( j > 1):
                    wloty.append(miejsce - 1)  #miejsce -1 
                else:
                    wloty.append(0)       
        
        if(self.down == True):
            if( i < bokY):
                wloty.append(miejsce + bokX) # miejsce + bokX
            else:
                wloty.append(0)
                

                
        if(len(wloty)==0):
            wloty.append(0)
            wloty.append(0)
            
        return (i, j, wloty[0], wloty[1])
    
    def wloty(self):
        return (self.up, self.down, self.left, self.right)
            
    def obrot(self): #obrót o 90 stopni w prawo
        nowa_pozycja = (self.pozycja + 1) % len(self.obrazki)
        self.pozycja = nowa_pozycja
        self.image = self.obrazki[nowa_pozycja]
        temp = self.right
        self.right = self.up
        self.up = self.left
        self.left = self.down
        self.down = temp 
        
        
    def startowaPozycja(self, nowa_pozycja): 
        if not(nowa_pozycja == self.pozycja):
            if( self.opcja ==1 ):       
                self.up = 1
                self.down = 0
                self.right = 1
                self.left = 0
            elif(self.opcja == 2):
                self.up = 0
                self.down = 0 
                self.right = 1
                self.left =1 
            else:
                self.up = 0
                self.down = 0 
                self.right = 0
                self.left = 0
           
            
            self.pozycja = nowa_pozycja % len(self.obrazki)
            self.image = self.obrazki[self.pozycja]
            for i in range(1, self.pozycja + 1):
                temp = self.right
                self.right = self.up
                self.up = self.left
                self.left = self.down
                self.down = temp 
            
def czyPolaczone(klocki): #klocki to tablica z wszystkimi kolankami i rurami
    global ktoryLevel
    rozmiar = len(klocki)
    ile =1 
    poz = 1
    if(klocki[0].left == True and klocki[rozmiar-1].right == True):
        poz = 1
        
        wylot_stary = 0
        sprawdzamy = True
    else:
        sprawdzamy = False
        return False
    
    while sprawdzamy: 
        ile += 1

        (o, u, wlot1,wlot2) = klocki[poz-1].polaczenia(poz)
#        if(poz < rozmiar + 1):
#            label = myfont.render(" (pozycja, wlot, wylot, wylot_stary)" + str((poz, wlot1,wlot2, wylot_stary)),1, (255,255,255))
#            win.blit(label, (350, 50 + ile *20)) 
        if(wlot1 == wylot_stary): # czyli, czy jest połączenie między klockami
            if(wlot2 == False): #czyli, że wychodzi poza plansze
                if(poz == rozmiar): #czyli, że jestemy na ostatnim klocku
                    return True # bo juz sprawdzalismy czy ma odplyw na prawo
                else:
                    return False # gdzies w niepozadanym miejscu wychodzimy
          
            else:
                wylot_stary = poz
                poz = wlot2 # przechodzimy do klocka do którego woda popłynie
                
        elif(wlot2 == wylot_stary):
            if(wlot1 == False): #czyli, że wychodzi poza plansze
                if(poz == rozmiar): #czyli, że jestemy na ostatnim klocku
                    return True # bo juz sprawdzalismy czy ma odplyw na prawo
                else:
                    return False # gdzies w niepozadanym miejscu wychodzimy
          
            else:
                wylot_stary = poz
                poz = wlot1 # przechodzimy do klocka do którego woda popłynie            
            
        else:
            return False #czyli badane dwa klocki nie maja polaczenia
   
def aktualizujLevel():
    global ktoryLevel
    ktoryLevel += 1
    (rozmiar, klocki, bokX, bokY) = wybierzLevel(ktoryLevel)
    return (rozmiar, klocki, bokX, bokY)

def wybierzLevel(ktoryLevel):
    random.seed(8)
    if(ktoryLevel == 0):
        for k in levele[0].klocki:
            k.startowaPozycja(random.randint(0,6))
            
    elif (ktoryLevel == 1):
        # drugi poziom
        for k in levele[1].klocki:
            k.startowaPozycja(random.randint(0,6))
    elif (ktoryLevel == 2):
        #trzeci poziom
         for k in levele[2].klocki:
            k.startowaPozycja(random.randint(0,6))
    elif (ktoryLevel == 3):
        #trzeci poziom
         for k in levele[3].klocki:
            k.startowaPozycja(random.randint(0,6))
            
    elif (ktoryLevel == 4):
        #trzeci poziom
         for k in levele[4].klocki:
            k.startowaPozycja(random.randint(0,6))
            
    elif (ktoryLevel == 5):
        #trzeci poziom
         for k in levele[5].klocki:
            k.startowaPozycja(random.randint(0,6))
    
    level = levele[ktoryLevel]
    rozmiar = level.rozmiar
    klocki = level.klocki
    bokX = level.szer
    bokY = level.wys
    return (rozmiar, klocki, bokX, bokY)


def Menu(intro = False): 
    global isMusic
    global klocki, bokX, bokY, rozmiar, t0, ktoryLevel
    isMenu = True
    while isMenu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isMenu = False
                pygame.quit()
                
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                
                
                if(screen_h/2 - button[0]/2 < pos[0] < (screen_h/2 + button[0]/2 )):
                    
                    # wracamy do gry?
                    if(intro == False):
                        if(( screen_w/2 - 1.5* button[1]) < pos[1] < (screen_w/2 - button[1]/2) ):
                            isMenu= False
 
                     # czy start od początku
                    if(( screen_w/2 - button[1]/2) < pos[1] < (screen_w/2 + button[1]/2) ):
                        isMenu= False
                        ktoryLevel = 0
                        (rozmiar, klocki, bokX, bokY) = wybierzLevel(0)
                        t0= pygame.time.get_ticks()   

                        #muzyka wlacz/wylacz
                    if(( screen_w/2 + button[1]/2) < pos[1] < (screen_w/2 + 1.5* button[1]) ):
                        if isMusic == True:
                            pygame.mixer.music.pause()
                            isMusic= False
                        else:
                            pygame.mixer.music.unpause()
                            isMusic = True
                    if(( screen_w/2 + 1.5*button[1] ) < pos[1] < (screen_w/2 + 2.5* button[1]) ):
                         pygame.quit()
                        
                        
                         
                        
        win.fill((0,0,0)) #ustawiamy tło ekranu
        win.blit(tlo_menu,(0,0))
        
        #wyswietalnie przyciskow na ekranie
        if intro == False:
            win.blit(powrot_button, (screen_h/2 - button[0]/2 , screen_w/2 - 1.5* button[1])) 
        win.blit(start_button, (screen_h/2 - button[0]/2 , screen_w/2 - button[1]/2)) 
        win.blit(muzyka_button[isMusic], (screen_h/2 - button[0]/2 , screen_w/2 + button[1]/2))
        win.blit(wyjdz_button, (screen_h/2 - button[0]/2 , screen_w/2 + 1.5 * button[1]))
        pygame.display.update()  
        

    
#komunikat po wygraniu poziomu
def komunikat():
    global ktoryLevel, bokX, bokY, rozmiar, klocki, t0
    isPause = True
    while isPause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isPause = False
                pygame.quit()
                
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                
                
                if((screen_w - button[0] - 20 ) < pos[0] < (screen_w - 20)):
                     # gram dalej
                    if( 300 -2*button[1] < pos[1] < 300- button[1] ):
                        isPause= False
                        if ktoryLevel < ileLeveli -1: #jesli sa jeszcze wyzsze poziomy do przejscia
                            (rozmiar, klocki, bokX, bokY) = aktualizujLevel()
                            t0= pygame.time.get_ticks()
                            
                        # czy menu
                    if( 300 -button[1] < pos[1] < 300 ):
                        isPause = False
                        Menu()
                        
              
        label = myfont.render("Brawo!!" ,1, (255,255,255))
        win.blit(label, (400, 110 ))
          
        win.blit(dalej_button, (screen_w - button[0] - 20, 300 -2*button[1] )) 
        win.blit(menu_button, (screen_w - button[0] - 20 , 300 -button[1])) 
        pygame.display.update()

def koniecCzasu():
    global ktoryLevel, bokX, bokY, rozmiar, klocki, t0
    isPause = True
    while isPause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isPause = False
                pygame.quit()
                
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                
                
                if((screen_w - button[0] - 20 ) < pos[0] < (screen_w - 20)):
                     # powtarzam level 
                    if( 300 -2*button[1] < pos[1] < 300- button[1] ):
                        isPause= False
                        (rozmiar, klocki, bokX, bokY) = wybierzLevel(ktoryLevel)
                        t0= pygame.time.get_ticks()
                        # czy menu
                    if( 300 -button[1] < pos[1] < 300 ):
                        isPause = False
                        Menu()
                        
              
        label = myfont.render("Koniec czasu :(((((",1, (255,255,255))
        win.blit(label, (400, 110 ))
          
        win.blit(powtorz_button, (screen_w - button[0] - 20, 300 -2*button[1] )) 
        win.blit(menu_button, (screen_w - button[0] - 20 , 300 -button[1]))        
        pygame.display.update()

def Wygrales():
    global ktoryLevel, bokX, bokY, rozmiar, klocki, t0
    isPause = True
    while isPause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isPause = False
                pygame.quit()
                
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                
                
                if((screen_w - button[0] - 20 ) < pos[0] < (screen_w - 20)):
                        # idz do menu
                    if( 300 -button[1] < pos[1] < 300 ):
                        isPause = False
                        Menu(intro = True)
                        
              
        label = myfont.render("Brawo !!! Koniec gry :D",1, (255,255,255))
        win.blit(label, (400, 110 ))
           
        win.blit(menu_button, (screen_w - button[0] - 20 , 300 -button[1]))        
        pygame.display.update()
#----------------tworzenie klocków różnych w pozycjach 0 -----------------------------------
# kolanka 
kol1 = rura(klocek_bok, kolanko_image, 1, 0, 0, 1,1, 0) # teraz góra-prawo
kol2 = rura(klocek_bok, kolanko_image, 1, 0, 0, 1,1, 0) # teraz góra-prawo
kol3= rura(klocek_bok, kolanko_image, 1, 0, 0, 1,1, 0) # teraz góra-prawo
kol4 = rura(klocek_bok, kolanko_image, 1, 0, 0, 1,1, 0) # teraz góra-prawo
kol5 = rura(klocek_bok, kolanko_image, 1, 0, 0, 1,1, 0) # teraz góra-prawo
kol6 = rura(klocek_bok, kolanko_image, 1, 0, 0, 1,1, 0) # teraz góra-prawo
kol7 = rura(klocek_bok, kolanko_image, 1, 0, 0, 1,1, 0) # teraz góra-prawo
kol8 = rura(klocek_bok, kolanko_image, 1, 0, 0, 1,1, 0) # teraz góra-prawo
kol9 = rura(klocek_bok, kolanko_image, 1, 0, 0, 1,1, 0) # teraz góra-prawo
kol10 = rura(klocek_bok, kolanko_image, 1, 0, 0, 1,1, 0) # teraz góra-prawo
kol11 = rura(klocek_bok, kolanko_image, 1, 0, 0, 1,1, 0) # teraz góra-prawo
kol12 = rura(klocek_bok, kolanko_image, 1, 0, 0, 1,1, 0) # teraz góra-prawo
kol13 = rura(klocek_bok, kolanko_image, 1, 0, 0, 1,1, 0) # teraz góra-prawo
kol14 = rura(klocek_bok, kolanko_image, 1, 0, 0, 1,1, 0) # teraz góra-prawo
kol15= rura(klocek_bok, kolanko_image, 1, 0, 0, 1,1, 0) # teraz góra-prawo
kol16= rura(klocek_bok, kolanko_image, 1, 0, 0, 1,1, 0) # teraz góra-prawo
kol17= rura(klocek_bok, kolanko_image, 1, 0, 0, 1,1, 0) # teraz góra-prawo
kol18= rura(klocek_bok, kolanko_image, 1, 0, 0, 1,1, 0) # teraz góra-prawo
kol19= rura(klocek_bok, kolanko_image, 1, 0, 0, 1,1, 0) # teraz góra-prawo
kol20= rura(klocek_bok, kolanko_image, 1, 0, 0, 1,1, 0) # teraz góra-prawo
kol21= rura(klocek_bok, kolanko_image, 1, 0, 0, 1,1, 0) # teraz góra-prawo
kol22= rura(klocek_bok, kolanko_image, 1, 0, 0, 1,1, 0) # teraz góra-prawo
kol23= rura(klocek_bok, kolanko_image, 1, 0, 0, 1,1, 0) # teraz góra-prawo
kol24= rura(klocek_bok, kolanko_image, 1, 0, 0, 1,1, 0) # teraz góra-prawo
kol25= rura(klocek_bok, kolanko_image, 1, 0, 0, 1,1, 0) # teraz góra-prawo
kol26= rura(klocek_bok, kolanko_image, 1, 0, 0, 1,1, 0) # teraz góra-prawo
# rury
r1 = rura(klocek_bok, rura_image, 0, 0, 1, 1,2, 0) #pozioma 
r2 = rura(klocek_bok, rura_image, 0, 0, 1, 1,2, 0) #pozioma 
r3 = rura(klocek_bok, rura_image, 0, 0, 1, 1,2, 0) #pozioma 
r4 = rura(klocek_bok, rura_image, 0, 0, 1, 1,2, 0) #pozioma 
r5 = rura(klocek_bok, rura_image, 0, 0, 1, 1,2, 0) #pozioma 
r6 = rura(klocek_bok, rura_image, 0, 0, 1, 1,2, 0) #pozioma 
r7 = rura(klocek_bok, rura_image, 0, 0, 1, 1,2, 0) #pozioma 
r8 = rura(klocek_bok, rura_image, 0, 0, 1, 1,2, 0) #pozioma 
r9 = rura(klocek_bok, rura_image, 0, 0, 1, 1,2, 0) #pozioma 
r10 = rura(klocek_bok, rura_image, 0, 0, 1, 1,2, 0) #pozioma 
r11 = rura(klocek_bok, rura_image, 0, 0, 1, 1,2, 0) #pozioma 
r12 = rura(klocek_bok, rura_image, 0, 0, 1, 1,2, 0) #pozioma 
r13 = rura(klocek_bok, rura_image, 0, 0, 1, 1,2, 0) #pozioma 
r14 = rura(klocek_bok, rura_image, 0, 0, 1, 1,2, 0) #pozioma 
r15 = rura(klocek_bok, rura_image, 0, 0, 1, 1,2, 0) #pozioma 
r16 = rura(klocek_bok, rura_image, 0, 0, 1, 1,2, 0) #pozioma 
r17 = rura(klocek_bok, rura_image, 0, 0, 1, 1,2, 0) #pozioma 
r18 = rura(klocek_bok, rura_image, 0, 0, 1, 1,2, 0) #pozioma 
#puste klocki
p1 = rura(klocek_bok, pusty_image, 0, 0, 0, 0,3, 0) # pusty
p2 = rura(klocek_bok, pusty_image, 0, 0, 0, 0,3, 0) # pusty
p3 = rura(klocek_bok, pusty_image, 0, 0, 0, 0,3, 0) # pusty
p4 = rura(klocek_bok, pusty_image, 0, 0, 0, 0,3, 0) # pusty
p5 = rura(klocek_bok, pusty_image, 0, 0, 0, 0,3, 0) # pusty
p6 = rura(klocek_bok, pusty_image, 0, 0, 0, 0,3, 0) # pusty
p7 = rura(klocek_bok, pusty_image, 0, 0, 0, 0,3, 0) # pusty
p8 = rura(klocek_bok, pusty_image, 0, 0, 0, 0,3, 0) # pusty
p9 = rura(klocek_bok, pusty_image, 0, 0, 0, 0,3, 0) # pusty
p10 = rura(klocek_bok, pusty_image, 0, 0, 0, 0,3, 0) # pusty

#----------------tworzenie leveli --------------------------------
klocki1 = [kol1, kol2, p1,\
           kol3, r1, kol4,\
           kol5, kol6, kol7]
level1 = level(klocki1, 3, 3)
#kolejny:
klocki2 = [kol1, kol2, r1, kol3,\
           kol4, kol5, kol6, kol7,\
           r2, r3, kol8, r4]
level2 = level(klocki2, 4, 3)
#kolejny:
klocki3 = [r1, kol1, p1, kol2, p2,\
           kol3, kol4, p3, kol5, kol6,\
           kol7, r2, r3, kol8, r4,\
           r5, p4, r6, p5, kol9]
level3 = level(klocki3, 5, 4)
# kolejny 
klocki4 = [kol1, kol2, kol3, p1,\
           r1, r2, kol4, kol5,\
           kol6, kol7, kol8, kol9,\
           kol10, r3, kol11, kol12,\
           kol13, r4, r5, r6]
level4 = level(klocki4, 4, 5)
#kolejny
klocki5 = [kol1, kol2, kol3, kol4, kol5,\
           r1, kol6, kol7, kol8, kol9,\
           kol10, kol11, kol12, r2, r3,\
           kol13, kol14, p1, kol15, kol16]

level5 = level(klocki5, 5, 4)

#kolejny
klocki10=[r1, kol1, kol2, r2, kol3,\
         kol4, kol5, kol6, kol7, kol8,\
         p1, kol9, p2, kol10, kol11,\
         kol12, kol13, kol14, kol15, kol16,\
         kol17, kol18, kol19, kol20, kol21,\
         kol22, r3, r4, kol23, p3,\
         p4, r5, r6, kol24, r7]
level10 = level(klocki10, 5,7)

#----wszystkie levele w liscie--------------
levele = [ level1, level2, level3,level5, level4, level10]

#----początkowe wartosci -------------------------------

# rozmiar - liczba klocków, bokX bokY- wymiary planszy , klocki - lista klocków na planszy
(rozmiar, klocki, bokX, bokY) = wybierzLevel(0)
czas = 30 
ileLeveli = len(levele)

run = True
ile_klikniec = 0 
n1 = 0 #miejsce klikniętego klocka w liscie klocki z aktualnego levelu

isMenu = True
ktoryLevel = 0 
t0= pygame.time.get_ticks()

# ---------pętla gry-------------------
while run :
          
    if isMenu==True:
        Menu(intro = True)
        t0= pygame.time.get_ticks()
        isMenu = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type ==pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            
            if rx < pos[0] < rx + bokX*klocek_bok:
                if ry < pos[1] < ry + bokY*klocek_bok:
                    j = ( (pos[0] - rx)//klocek_bok +1 )
                    i = ( (pos[1]- ry)//klocek_bok +1)       
                    n1 = (i-1)*bokX + j                 
                    klocki[n1-1].obrot()
                    rotationSound.play()
                    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:        
        Menu()
        isMenu = False
        

    
    win.fill((0,0,0)) #ustawiamy tło ekranu
    win.blit(tlo, (0, 0))
    for poz in range(1, rozmiar + 1):  
        klocki[poz-1].draw(poz, win)

    label = myfont.render(" Level " + str(ktoryLevel + 1),1, (0,0,0))
    win.blit(label, (screen_w/2 - 100 , 10 )) 
    
    t1 = math.floor((pygame.time.get_ticks() - t0)/1000)
    label = myfont.render(" Czas " + str(30-t1),1, (0,0,0))
    win.blit(label, (screen_w/2 + 100 , 30)) 
    
    
    win.blit(wylot_im, (bokX*klocek_bok + rx ,(bokY-1)*klocek_bok + ry )) 
    
    pygame.display.update() #wyswietlamy wszystko na ekranie
    
    if czyPolaczone(klocki)== True:
        if ktoryLevel < ileLeveli - 1:
            komunikat() # tu wybierzemy czy gramy dalej czy od poczatku
        else:
            Wygrales()
    elif 30-t1 < 0 :
        koniecCzasu()
            

pygame.quit()
        