from random import randint
import math as math
import matplotlib.pyplot as plotovanje
import matplotlib.axes as axes
import numpy as np
from pynput import keyboard
import sys

x = np.random.random(20)
y = np.random.random(20)
broj = 0




listaTacakaX = []
listaTacakaY = []

leveTacke = []
desneTacke = []

class _pobednickeTakce:
    def __init__(self, tacka1, tacka2, razdaljina):

        self.tacka1 = tacka1
        self.tacka2 = tacka2
        self.razdaljina = razdaljina



pobednickeTacke = _pobednickeTakce(None,None, 1000000)


class Tacka:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getKordinate(self):
        return x, y


def on_press(key):
    if (key == keyboard.Key.space):
        print("PRITISNUT SPEEEEEJS")
        global broj
        # plotovanje.scatter(x, y)

        # plotovanje.plot([x[1],x[1+1]],[y[1],y[1+1]],"ro-")
        broj += 1
        print(broj)


def iscrtaj(tacka1, tacka2):
    plotovanje.clf()
    xlimit = plotovanje.xlim(0, 1)
    ylimit = plotovanje.ylim(0, 1)
    plotovanje.axvline(x=1 / 2, color="black")

    for tacka in listaTacakaY:
        if tacka.x < 1 / 2:
            plotovanje.scatter(tacka.x, tacka.y, color="blue")
        else:
            plotovanje.scatter(tacka.x, tacka.y, color="red")
    plotovanje.plot([tacka1.x, tacka2.x],
                    [tacka1.y, tacka2.y], "yo-")
    plotovanje.pause(0.01)



def izracunajDistancu(tacka1, tacka2):
    return math.fabs(math.sqrt(pow((tacka1.x - tacka2.x), 2) + pow((tacka1.y - tacka2.y), 2)))



def bruteForce(xTacke, n):

    minimalnaRazdaljina = 10000000
    for i in range(n):
        for j in range(i+1, n):

            distancaTacaka = izracunajDistancu(xTacke[i],xTacke[j])
            iscrtaj(xTacke[i], xTacke[j])
            if distancaTacaka < minimalnaRazdaljina:
                minimalnaRazdaljina = distancaTacaka
                if minimalnaRazdaljina < pobednickeTacke.razdaljina:
                    pobednickeTacke.tacka1 = xTacke[i]
                    pobednickeTacke.tacka2 = xTacke[j]
                    pobednickeTacke.razdaljina = minimalnaRazdaljina

    return minimalnaRazdaljina


def najbliziStrip(strip, n, d):
    minimum = d
    for i in range(n):
        j = i+1
        if j < n and math.fabs(strip[j].y - strip[i].y) < minimum:
            for j in range(n):
                minimum = izracunajDistancu(strip[i], strip[j])

                iscrtaj(strip[i], strip[j])
                if minimum < pobednickeTacke.razdaljina and minimum != 0.0:
                    pobednickeTacke.tacka1 = strip[i]
                    pobednickeTacke.tacka2 = strip[j]
                    pobednickeTacke.razdaljina = minimum
    return minimum


def resiNajbliziPar(xTacke, yTacke, n):
    if n <= 3 and n >1:
        return bruteForce(xTacke, n)

    print(n)

    mid = round(n/2)
    srednjaTacka = xTacke[mid]

    tackeLevo = []  #Tacke levo od vertikalne linije
    tackeDesno = []   #Tacke desno do vertikalne linije

    leviiterator = 0
    desniiterator = 0

    for i in range(n):
        if yTacke[i].x <= srednjaTacka.x:
            tackeLevo.append(yTacke[i])
            leviiterator+=1
        else:
            tackeDesno.append(yTacke[i])
            desniiterator+=1

    minimalnaDesno = resiNajbliziPar(xTacke[mid:], tackeDesno,desniiterator )
    minimalnaLevo = resiNajbliziPar(xTacke, tackeLevo, leviiterator)

    minimalnaRazdaljina = 0

    if minimalnaLevo < minimalnaDesno:
        minimalnaRazdaljina = minimalnaLevo


    else:
        minimalnaRazdaljina = minimalnaDesno


    tackeBlizuSredine = []

    j = 0
    for i in range(len(yTacke)):
        if(math.fabs(yTacke[i].x - srednjaTacka.x) < minimalnaRazdaljina):
            tackeBlizuSredine.append(yTacke[i])
            j += 1
    sredisnjaDistanca = 1000000
    if j > 1:
        sredisnjaDistanca = najbliziStrip(tackeBlizuSredine, j, minimalnaRazdaljina)
    print("Strip = " + str(sredisnjaDistanca))
    if minimalnaRazdaljina > sredisnjaDistanca:

        return sredisnjaDistanca



    return minimalnaRazdaljina








if __name__ == '__main__':
    minDesno = 1000000
    minLevo = 1000000
    minSredina = 100000

    minimalneTacke = np.empty(shape=(2,), dtype = Tacka )



    # boing = Avion(imeAviona="boing",rasponKrila= 52, brojPutnika=1000)
    # boing.aprint()
    # boing.getimeAviona()
    niz = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # plotovanje.plot([x[5],x[6]],[y[5],y[6]],"ro-")
    listener = keyboard.Listener(
        on_press=on_press
    )
    listener.start()

    sortiranX = np.sort(x, kind='mergesort')

    sortiranY = np.sort(y, kind='mergesort')




    print(x)

    for xCord, yCord in zip(sortiranX, y):
        listaTacakaX.append(Tacka(xCord, yCord))

    for xCord, yCord in zip(x, sortiranY):
        listaTacakaY.append(Tacka(xCord, yCord))

    razdaljina = resiNajbliziPar(listaTacakaX, listaTacakaY, len(listaTacakaY))

    print("razdaljina = " + str(razdaljina))
    print("pobednickeTacke.razdaljina = " + str(pobednickeTacke.razdaljina))
    plotovanje.plot([pobednickeTacke.tacka1.x, pobednickeTacke.tacka2.x],
                    [pobednickeTacke.tacka1.y, pobednickeTacke.tacka2.y], "mo-")





    # leviiterator = 0
    # desniiterator = 0
    # for tacka in listaTacaka:
    #     if tacka.x < 1 / 2:
    #         leveTacke.append(tacka)
    #     else:
    #         desneTacke.append(tacka)
    # flag = 0
    # while broj < len(leveTacke) + 2 or broj < len(desneTacke) + 2:
    #     plotovanje.clf()
    #     plotovanje.axvline(x=1 / 2, color="black")
    #
    #     xlimit = plotovanje.xlim(0, 1)
    #     ylimit = plotovanje.ylim(0, 1)
    #
    #     for tacka in listaTacaka:
    #         if tacka.x < 1 / 2:
    #             plotovanje.scatter(tacka.x, tacka.y, color="blue")
    #         else:
    #             plotovanje.scatter(tacka.x, tacka.y, color="red")
    #
    #     if flag == 3:
    #         plotovanje.plot([minimalneTacke[0].x, minimalneTacke[1].x],
    #                         [minimalneTacke[0].y, minimalneTacke[1].y], "mo-")
    #         plotovanje.pause(20)
    #
    #     if flag == 2:
    #         minSredina = izracunajDistancu(desneTacke[0], leveTacke[len(leveTacke) - 1])
    #         plotovanje.plot([desneTacke[0].x, leveTacke[len(leveTacke) - 1].x],
    #                         [desneTacke[0].y, leveTacke[len(leveTacke) - 1].y], "yo-")
    #
    #         print("Uzeta sredina u obzir")
    #
    #         if minSredina < minLevo and minSredina < minDesno:
    #             print("minLevo = " + minLevo)
    #             print("minDesno = " + minDesno)
    #             print("minSredina = " + minSredina)
    #
    #
    #             minimalneTacke[0] = desneTacke[0]
    #             minimalneTacke[1] = leveTacke[len(leveTacke) - 1]
    #
    #
    #
    #         flag += 1
    #
    #     if leviiterator < len(leveTacke) - 1:
    #         plotovanje.plot([leveTacke[leviiterator].x, leveTacke[leviiterator + 1].x],
    #                         [leveTacke[leviiterator].y, leveTacke[leviiterator + 1].y], "yo-")
    #         distanca = izracunajDistancu(leveTacke[leviiterator], leveTacke[leviiterator + 1])
    #
    #         if distanca < minLevo:
    #             minLevo = distanca
    #             if minLevo < minDesno:
    #                 minimalneTacke[0] = leveTacke[leviiterator]
    #                 minimalneTacke[1] = leveTacke[leviiterator+1]
    #
    #
    #         leviiterator += 1
    #     elif leviiterator == len(leveTacke) - 1:
    #         plotovanje.plot([leveTacke[leviiterator].x, leveTacke[0].x],
    #                         [leveTacke[leviiterator].y, leveTacke[0].y], "yo-")
    #         distanca = izracunajDistancu(leveTacke[leviiterator], leveTacke[0])
    #
    #         if distanca < minLevo:
    #             minLevo = distanca
    #             if minLevo < minDesno:
    #                 minimalneTacke[0] = leveTacke[leviiterator]
    #                 minimalneTacke[1] = leveTacke[0]
    #
    #
    #
    #         print("BBB")
    #         leviiterator += 1
    #         flag += 1
    #
    #     if desniiterator < len(desneTacke) - 1:
    #         plotovanje.plot([desneTacke[desniiterator].x, desneTacke[desniiterator + 1].x],
    #                         [desneTacke[desniiterator].y, desneTacke[desniiterator + 1].y], "yo-")
    #         distanca = izracunajDistancu(desneTacke[desniiterator], desneTacke[desniiterator + 1])
    #
    #         if distanca < minDesno:
    #             minDesno = distanca
    #             if minDesno < minLevo:
    #                 minimalneTacke[0] = desneTacke[desniiterator]
    #                 minimalneTacke[1] = desneTacke[desniiterator+1]
    #
    #         desniiterator += 1
    #
    #     elif desniiterator == len(desneTacke) - 1:
    #         plotovanje.plot([desneTacke[desniiterator].x, desneTacke[0].x],
    #                         [desneTacke[desniiterator].y, desneTacke[0].y], "yo-")
    #         distanca = izracunajDistancu(desneTacke[desniiterator], desneTacke[0])
    #
    #         if distanca < minDesno:
    #             minDesno = distanca
    #             if minDesno < minLevo:
    #                 minimalneTacke[0] = desneTacke[desniiterator]
    #                 minimalneTacke[1] = desneTacke[0]
    #
    #         print("AAA")
    #         desniiterator += 1
    #         flag += 1
    #
    #
    #     plotovanje.ylabel("Brojevi na Y osi")
    #     plotovanje.xlabel("Brojevi na X osi")
    #
    #     plotovanje.show()
    #     plotovanje.pause(1)
    #     broj += 1



    # plotovanje.close('all')
    # sys.exit()
