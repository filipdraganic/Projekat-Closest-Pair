from random import randint
import math as math
import matplotlib.pyplot as plotovanje
import matplotlib.axes as axes
import numpy as np
from pynput import keyboard
import sys
from pynput.keyboard import Key, Listener
import config

# x = np.random.random(20)
# y = np.random.random(20)
broj = 0

x = []
y = []
listaTacakaX = []
listaTacakaY = []

leveTacke = []
desneTacke = []

config.pokrenuto = False

globalnibrojac = 0

levox = 0
desnox = 1
sredina = 1 / 2
gorey = 1
doley = 1

class _PobednickeTacke:
    def __init__(self, tacka1, tacka2, razdaljina):
        self.tacka1 = tacka1
        self.tacka2 = tacka2
        self.razdaljina = razdaljina


pobednickeTacke = _PobednickeTacke(None, None, 1000000)


class Tacka:
    def __init__(self, xKoordinata, yKoordinata):
        self.x = xKoordinata
        self.y = yKoordinata

    def getKordinate(self):
        return self.x, self.y


def iscrtaj(tacka1, tacka2, xLinija=sredina, tackeUObziru=None):
    plotovanje.clf()
    global desnox, gorey, globalnibrojac
    if desnox > gorey:
        limit = desnox
    else:
        limit = gorey
    if tacka1 == tacka2: return

    globalnibrojac += 1

    xlimit = plotovanje.xlim(0, limit+0.05)
    ylimit = plotovanje.ylim(0, limit+0.05)
    plotovanje.axvline(x=xLinija, color="black")
    global x, y

    for xCord, yCord in zip(x, y):
        if xCord < 1 / 2:
            plotovanje.scatter(xCord, yCord, color="blue")
        else:
            plotovanje.scatter(xCord, yCord, color="red")

    plotovanje.plot([tacka1.x, tacka2.x],
                    [tacka1.y, tacka2.y], "yo-")
    plotovanje.pause(0.01)


def izracunajDistancu(tacka1, tacka2):
    return math.sqrt(pow((tacka1.x - tacka2.x), 2) + pow((tacka1.y - tacka2.y), 2))


def bruteForce(xTacke, n):
    minimalnaRazdaljina = 10000000
    for i in range(n):
        for j in range(i + 1, n):

            distancaTacaka = izracunajDistancu(xTacke[i], xTacke[j])

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

            for j in range(i+1, n):
                if j < n and (strip[j].y - strip[i].y) < minimum:
                    tempminimum = izracunajDistancu(strip[i], strip[j])
                    iscrtaj(strip[i], strip[j])

                    if tempminimum < minimum:
                        minimum = tempminimum

                    if minimum < pobednickeTacke.razdaljina and minimum != 0.0:
                        pobednickeTacke.tacka1 = strip[i]
                        pobednickeTacke.tacka2 = strip[j]
                        pobednickeTacke.razdaljina = minimum
    return minimum


def resiNajbliziPar(xTacke, yTacke,  n):
    if 3 >= n > 1:
        return bruteForce(yTacke, n)
    if n == 1:
        return 10000

    print(n)

    mid = round(n / 2)
    srednjaTacka = xTacke[mid]

    global sredina
    sredina = xTacke[mid].x

    tackeLevo = []  # Tacke levo od vertikalne linije
    tackeDesno = []  # Tacke desno do vertikalne linije

    leviiterator = 0
    desniiterator = 0

    for i in range(n):
        if yTacke[i].x <= srednjaTacka.x:
            tackeLevo.append(yTacke[i])
            #leviiterator += 1
        else:
            tackeDesno.append(yTacke[i])
            #desniiterator += 1

    minimalnaDesno = resiNajbliziPar(xTacke[mid:], tackeDesno, len(tackeDesno))  # Rekurzivno se pozivaju za levo i desno od vertikalne linije
    minimalnaLevo = resiNajbliziPar(xTacke, tackeLevo, len(tackeLevo))

    minimalnaRazdaljina = min(minimalnaDesno, minimalnaLevo)

    tackeBlizuSredine = []

    j = 0
    for i in range(len(yTacke)):
        if math.fabs(yTacke[i].x - srednjaTacka.x) < minimalnaRazdaljina:  # Proverava se razdaljina po x izmedju svake tacke i srednje tacke
            tackeBlizuSredine.append(yTacke[i])  # Ako je manja od minimalne razdaljine uzima se da se proveri da li
            j += 1  # je manja razdaljina izmedju tih tacaka koje su na suprotnim stranama
    sredisnjaDistanca = 1000000  # vertikalne linije
    if j > 1:
        sredisnjaDistanca = najbliziStrip(tackeBlizuSredine, len(tackeBlizuSredine), minimalnaRazdaljina)
    print("Strip = " + str(sredisnjaDistanca))

    if minimalnaRazdaljina > sredisnjaDistanca:
        return sredisnjaDistanca

    return minimalnaRazdaljina


def prvoPozvati():
    pokrenuto = True
    minDesno = 1000000
    minLevo = 1000000
    minSredina = 100000

    minimalneTacke = np.empty(shape=(2,), dtype=Tacka)
    listaTupleTacaka = []

    for xCord, yCord in zip(x, y):
        listaTupleTacaka.append((xCord, yCord))


    listaTupleTacaka.sort(key=lambda tup: tup[1])

    print(listaTupleTacaka)

    for tacka in listaTupleTacaka:
        listaTacakaY.append(Tacka(tacka[0], tacka[1]))

    listaTupleTacaka.sort(key=lambda tup: tup[0])

    print(listaTupleTacaka)

    for tacka in listaTupleTacaka:
        listaTacakaX.append(Tacka(tacka[0], tacka[1]))

    global levox, desnox, sredina, gorey, doley

    desnox = listaTacakaX[len(listaTacakaX) - 1].x
    gorey = listaTacakaY[len(listaTacakaY) - 1].y
    levox = listaTacakaX[0].x
    doley = listaTacakaY[0].y
    broj = round(len(listaTacakaX)/2)
    sredina = listaTacakaX[broj].x

    #
    # print("LISTA TACAKA OD NULA = ")
    # print(listaTacakaX[0].x)

    razdaljina = resiNajbliziPar(listaTacakaX, listaTacakaY, len(listaTacakaX))

    # print(desnox)
    # print(levox)
    # print(sredina)
    print("UKUPAN BROJ ISCRTAVANJA  = " + str(globalnibrojac))

    print("razdaljina = " + str(razdaljina))
    print("pobednickeTacke.razdaljina = " + str(pobednickeTacke.razdaljina))
    iscrtaj(pobednickeTacke.tacka1, pobednickeTacke.tacka2)
    plotovanje.plot([pobednickeTacke.tacka1.x, pobednickeTacke.tacka2.x],
                    [pobednickeTacke.tacka1.y, pobednickeTacke.tacka2.y], "mo-")
    plotovanje.show()




pokrenuti = 1
if __name__ == '__main__':
    fig = plotovanje.figure()
    ax = fig.add_subplot(111)
    xlimit = plotovanje.xlim(0, 1)
    ylimit = plotovanje.ylim(0, 1)


    def on_press(key):
        print('{0} pressed'.format(
            key))

        if key == Key.esc:
            sys.exit()


    def onclick(event):
        print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
              (event.button, event.x, event.y, event.xdata, event.ydata))
        # plotovanje.plot(event.xdata, event.ydata, ',')
        plotovanje.scatter(event.xdata, event.ydata, color='blue')
        x.append(event.xdata)
        y.append(event.ydata)
        fig.canvas.draw()


    def keyclick(event):
        global x, y

        print(event.key)
        if event.key == "r":
            global pokrenuti
            if pokrenuti == 1:
                pokrenuti += 1

                prvoPozvati()
        if event.key == "enter":
            f = open("fajlSaTackama.txt", "w")

            f.write(str(x))
            f.write("\n")
            f.write(str(y))
            f.close()
        if event.key == "escape":
            sys.exit()

        if event.key == "t":
            f = open("fajlSaTackama.txt", "r")
            xstring = f.readline()
            ystring = f.readline()
            ystring = ystring[1:-1].split(", ")
            xstring = xstring[1:-2].split(", ")

            for i in range(len(xstring)):
                t = float(xstring[i])
                x.append(t)
                t = float(ystring[i])
                y.append(t)

            print(x)
            print("AAAAAAA")
            print(y)
            plotovanje.scatter(x, y, color="blue")
            fig.canvas.draw()

            f.close()


    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    cidkeyboard = fig.canvas.mpl_connect('key_press_event', keyclick)

    plotovanje.show()
