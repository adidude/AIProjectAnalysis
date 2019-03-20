import pygame, sys, random, colorsys
from pygame.locals import *


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

dataFile = open("soc-sign-bitcoinotc.csv", "r")
dataList = []
while True:
    
    data = dataFile.readline().split(",")
    data[len(data) - 1] = data[len(data) - 1].replace("\n", "")
    if(data == ['']):
        break
    
    source = int(data[0])
    target = int(data[1])
    rating = int(data[2])
    time = float(data[3])

    dataList.append([source, target, rating, time])
    
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
offset = 50

rndList1 = []
for i in range(9000):
    rndList1.append(random.randint(0, 900))
                   
rndList2 = []
for i in range(9000):
    rndList2.append(random.randint(0, 900))

counter = 0
counterStep = 1
display = True
# run the game loop
while 1:
    # check for events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYUP:
            if event.key == ord("p"):
                pass
        if pygame.mouse.get_pressed()[0] == 1: #left
            counter += counterStep
            if(counter > 99):
                counter = 0
            display = True
        if pygame.mouse.get_pressed()[1] == 1: #middle
            pass           
        if pygame.mouse.get_pressed()[2] == 1: #right
            counter -= counterStep
            if(counter < 0):
                counter = 99
            display = True

    if(display):
        windowSurface.fill(BLACK)
        for i in range(int((counter) * len(dataList) / 100), int((counter + counterStep) * len(dataList) / 100)):
            randColour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            c = (dataList[i][2] + 10) * 12.5
            colour = HSV2RGB((c, 100, 100))
            pygame.draw.circle(windowSurface, RED, (rndList1[dataList[i][0]] + offset, rndList2[dataList[i][0]] + offset), 5)
            pygame.draw.circle(windowSurface, BLUE, (rndList1[dataList[i][1]] + offset, rndList2[dataList[i][1]] + offset), 4)
            pygame.draw.line(windowSurface, colour, (rndList1[dataList[i][0]] + offset, rndList2[dataList[i][0]] + offset), (rndList1[dataList[i][1]] + offset, rndList2[dataList[i][1]] + offset))

        msg=(str(counter + 1) + "%")
        label = myfont.render(msg, 1, WHITE, BLACK)
        windowSurface.blit(label, (25, 25))
        display = False

    pygame.display.update()
    mainClock.tick(140)


