import pygame
import math
import sys
import random

pygame.init()
pygame.display.set_caption('броуновское движение')
width = 1400
height = 800
win = pygame.display.set_mode((width, height))
nn = 20

rB = []
mB = []
xB = []
yB = []
aB = []
vB = []
cB = []

for i in range(nn + 1):
    rB.append(random.randint(10, 45))
    print(rB)
    mB.append(rB[i] * 2)
    xB.append(random.randint(rB[i], width - rB[i]))
    yB.append(random.randint(rB[i], height - rB[i]))
    aB.append(random.random() * 2 * math.pi) # угол движения шарика
    # print(aB)
    vB.append(2)
    cB.append(0) # цвет
    cB[i] = int(255 * random.random()), \
            int(255 * random.random()), \
            int(255 * random.random())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            sys.exit()
    win.fill((0, 0, 0))
    for i in range(1, nn + 1):
        xB[i] += vB[i] * math.cos(aB[i])
        yB[i] += vB[i] * math.sin(aB[i])
        pygame.draw.circle(win, cB[i], (xB[i], yB[i]), rB[i])
    pygame.time.delay(10)
    pygame.display.update()
# реакция на столкновение шара со стенами
    for i in range(1, nn + 1):
        if xB[i] <= rB[i] :
            aB[i] = math.pi - aB[i]
        if xB[i] >= width - rB[i] :
            aB[i] = math.pi - aB[i]
        if yB[i] <= rB[i] :
            aB[i] = -aB[i]
        if yB[i] >= height - rB[i] :
            aB[i] = -aB[i]

# проверка на столкновение друг с другом
    for i in range(1, nn + 1):
        for j in range(i + 1, nn + 1):
            Rast = ((xB[i] - xB[j]) ** 2 + (yB[i] - yB[j]) ** 2) ** 0.5
            if Rast <= rB[i] + rB[j]: # проверяем уменьшается ли растрояние между шарами, то есть сли
                #расстояние между шарами меньше или равнео сумме их радиусов
                xB1new = xB[i] + vB[i] * math.cos(aB[i])
                yB1new = yB[i] + vB[i] * math.sin(aB[i])
                xB2new = xB[j] + vB[j] * math.cos(aB[j])
                yB2new = yB[j] + vB[j] * math.sin(aB[j])

                RastNew = ((xB1new - xB2new) ** 2 + (yB1new - yB2new) ** 2) ** 0.5
                if Rast > RastNew:# шары столкнулись , то есть если расстояние уменьшается
                    BB = math.atan((yB[j] - yB[i]) / (xB[j] - xB[i]))# угол от оси до луча между осями шаров

                    W1 = aB[i] - BB # угол от луча к напрявлению движения шаров
                    W2 = aB[j] - BB
                    # проекции скоростей шара на луч и на перпендикуляр к нему до столкновения
                    Vw1 = vB[i] * math.cos(W1)
                    Vw2 = vB[j] * math.cos(W2)
                    Vwt1 = vB[i] * math.sin(W1)
                    Vwt2 = vB[j] * math.sin(W1)
                    # из формул центрального соударения
                    Vw1 = (2 * mB[j] * vB[j] * math.cos(W2) + (mB[i]
                                                               - mB[j]) * vB[i] * math.cos(W1)) / (mB[i] + mB[j])
                    Vw2 = (2 * mB[i] * vB[i] * math.cos(W1) + (mB[j]
                                                               - mB[i]) * vB[j] * math.cos(W2)) / (mB[i] + mB[j])
                    # скорость шаров после соударения
                    vB[i] = (Vw1 ** 2 + Vwt1 ** 2) ** 0.5
                    vB[j] = (Vw2 ** 2 + Vwt2 ** 2) ** 0.5
                    # угол от луча до направления движения после столкновения
                    W1 = math.atan(Vwt1 / Vw1)
                    if Vw1 < 0:
                        W1 += math.pi
                    W2 = math.atan(Vwt2 / Vw2)
                    if Vw2 < 0:
                        W2 += math.pi
                    # новое направление после столкновения
                    aB[i] = BB + W1
                    while aB[i] > math.pi:
                        aB[i] -= 2 * math.pi
                    while aB[i] < -math.pi:
                        aB[i] += 2 * math.pi
                    aB[j] = BB + W2
                    while aB[j] > math.pi:
                        aB[j] -= 2 * math.pi
                    while aB[j] < -math.pi:
                        aB[j] += 2 * math.pi
