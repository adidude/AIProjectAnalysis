import pygame, sys, random, snap, colorsys
from pygame.locals import *
from AI_Project import getNetwork

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()
myfont = pygame.font.SysFont("monospace", 15)
# set up the window
WINDOWWIDTH = 1000
WINDOWHEIGHT = 1000
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Game')

def HSV2RGB(hsv):
    h, s, v = hsv;
    h /= 358;
    s /= 100;
    v /= 100;
    rgb = (colorsys.hsv_to_rgb(h, s, v)[0] * 255, colorsys.hsv_to_rgb(h, s, v)[1] * 100, colorsys.hsv_to_rgb(h, s, v)[2] * 100);
    return rgb;

def nextMonthDate(thisDate):
    date = thisDate.split(".")
    date[1], date[2] = int(date[1]), int(date[2])
    date[1] += 1
    if(date[1] == 13):
        date[1] = 1
        date[2] += 1

    if(date[1] < 10):
        date[1] = "0" + str(date[1])
    else:
        date[1] = str(date[1])
    date[2] = str(date[2])
    return date[0] + "." + date[1] + "." + date[2]

def nextHalfMonthDate(thisDate):
    date = thisDate.split(".")
    date[1], date[2] = int(date[1]), int(date[2])
    date[1] += 6
    if(date[1] > 12):
        date[1] = date[1] - 12
        date[2] += 1

    if(date[1] < 10):
        date[1] = "0" + str(date[1])
    else:
        date[1] = str(date[1])
    date[2] = str(date[2])
    return date[0] + "." + date[1] + "." + date[2]

def nextYearDate(thisDate):
    date = thisDate.split(".")
    date[2] = int(date[2])
    date[2] += 1
    date[2] = str(date[2])
    return date[0] + "." + date[1] + "." + date[2]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

offset = 50

msg = ""

configFile = open("config.txt", "r")
config = configFile.readline()
config = config.replace("\n", "")
config = config.split(";")

showAll = int(config[0])
threshold = int(config[1])
thickness = int(config[2])
radius = int(config[3])
startDate = config[4]

#08.11.2010
#25.01.2016
network = getNetwork()
display = True
# run the game loop
while 1:
    # check for events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYUP:
            if event.key == K_SPACE:
                network = getNetwork()
                startDate = endDate
                display = True
        if pygame.mouse.get_pressed()[0] == 1: #left
            pass
        if pygame.mouse.get_pressed()[1] == 1: #middle
            pass           
        if pygame.mouse.get_pressed()[2] == 1: #right
            pass

    if(display):

        if(threshold == 1):
            endDate = nextYearDate(startDate)
        elif(threshold == 2):
            endDate = nextHalfMonthDate(startDate)
        elif(threshold == 3):
            endDate = nextMonthDate(startDate)
        elif(threshold == 4):
            endDate = "25.01.2016"
            
        
        network.thresholdNetwork(startDate, endDate)

        
        rndList1 = []
        for i in range(1000000):
            rndList1.append(random.randint(0, WINDOWWIDTH - offset*2))
                           
        rndList2 = []
        for i in range(1000000):
            rndList2.append(random.randint(0, WINDOWHEIGHT - offset*2))
            
        windowSurface.fill((16, 16, 16))
        
        for EI in (network.network.Edges()):
            if(showAll):
                c = (network.network.GetIntAttrDatE(EI, "rating") + 10) * 12.5
                colour = HSV2RGB((c, 100, 100))            
                pygame.draw.line(windowSurface, colour, (rndList1[EI.GetSrcNId()] + offset, rndList2[EI.GetSrcNId()] + offset), (rndList1[EI.GetDstNId()] + offset, rndList2[EI.GetDstNId()] + offset), thickness)            
                pygame.draw.circle(windowSurface, WHITE, (rndList1[EI.GetSrcNId()] + offset, rndList2[EI.GetSrcNId()] + offset), radius)
                pygame.draw.circle(windowSurface, WHITE, (rndList1[EI.GetDstNId()] + offset, rndList2[EI.GetDstNId()] + offset), radius)
            else:
                if not(network.network.GetIntAttrDatE(EI, "rating") < 6 and network.network.GetIntAttrDatE(EI, "rating") > -6):
                    c = (network.network.GetIntAttrDatE(EI, "rating") + 10) * 12.5
                    colour = HSV2RGB((c, 100, 100))            
                    pygame.draw.line(windowSurface, colour, (rndList1[EI.GetSrcNId()] + offset, rndList2[EI.GetSrcNId()] + offset), (rndList1[EI.GetDstNId()] + offset, rndList2[EI.GetDstNId()] + offset), thickness)            
                    pygame.draw.circle(windowSurface, WHITE, (rndList1[EI.GetSrcNId()] + offset, rndList2[EI.GetSrcNId()] + offset), radius)
                    pygame.draw.circle(windowSurface, WHITE, (rndList1[EI.GetDstNId()] + offset, rndList2[EI.GetDstNId()] + offset), radius)
        msg=(startDate + " - " + endDate)


        
        label = myfont.render(msg, 1, WHITE, BLACK)
        windowSurface.blit(label, (25, 25))
        display = False

    pygame.display.update()
    mainClock.tick(140)
