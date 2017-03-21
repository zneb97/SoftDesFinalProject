from PIL import Image
import pyscreenshot as ImageGrab
import pyautogui

def distance(a,b):
    "this obviously finds the distance between two points"
    return (abs(a[0] - b[0])**2 + abs(a[1] - b[1])**2) ** .5

def findList(pixels, x_size, y_size, C, me):
    "this is the image processing part of the program"
    "the for loops will run through each pixel, skipping C pixels every time. If it notices a long line of pixels that are all the same color"
    "it will go to the center and mark how large the line is, if there is another close mark, it will delete the mark with the shorter line"
    "this attempt to find one mark per blob, although it has errors"
    listDangers = []
    last = 0
    counter = 0
    for i in range(0,y_size-1,C):
        for j in range(0,x_size-1,C):
            r, g, b = pixels[j, i]
            if last < 200 and last == (r + g + b)/3:
                counter += 1
            else:
                if counter > me/C:
                    for tup in listDangers:
                        if distance(tup, (j - counter * C / 2, i)) < 30:
                            if tup[2] < counter:
                                listDangers.remove(tup)
                            else:
                                counter = 0
                        if distance((j - counter * C / 2, i), (x_size/2, y_size/2)) < me:
                            counter = 0
                    if counter != 0:
                        listDangers.append((j - counter * C / 2, i, counter))
                counter = 0
            last = (r + g + b)/3
        for tup in listDangers:
            if distance(tup, (j - counter C / 2, i)) < 30:
                if tup[2] < counter:
                    listDangers.remove(tup)
                else:
                    counter = 0

        if counter != 0:
            listDangers.append((j - counter * C / 2, i, counter))

    return listDangers

if __name__ == '__main__':
    "this is the main script"
    "the entire thing is within a while loop that starts off with grabbing the screen and converting it into pixels"
    "it will then go to the center and keep stepping right until it finds a different colored pixel, once it does it will mark the length"
    "labeled 'me'. this should find the radius of the player"
    "it then calls findList witch will return a list of all danger"
    "finally it will find which danger is closer to it and ron away from that"
    # im = Image.open("agario.jpg")
    while True:
        C = 8
        im = ImageGrab.grab()
        pixels = im.load()
        counter = 0
        me = 100
        x = 0
        y = 0
        last = 0
        x_size, y_size = im.size
        r, g, b = pixels[x_size/2, y_size/2]
        last = (r + g + b)/3
        while last == (r + g + b)/3:
            last = (r + g + b)/3
            counter += 1
            x += C
            r, g, b = pixels[x_size/2 + x, y_size/2 + y]
        pixels[x_size/2 + x, y_size/2] = (0, 0, 0)
        print(x_size/2 + x, y_size/2)
        me = counter * C
        print(me)
        print(x_size/2)
        print(y_size/2)
        listDangers = findList(pixels, x_size, y_size, C, 2 * me)
        x = x_size/2
        y = y_size/2

        lowest = (0, 0)
        for tup in listDangers:
            # pixels[tup[0],tup[1]] = (0,0,0)
            print(tup)
            if distance(tup, (x_size/2, y_size/2)) <= distance(lowest,(x_size/2, y_size/2)):
                lowest = tup
        print("low: " + str(lowest))
        try:

            pyautogui.moveTo(x_size-lowest[0], y_size-lowest[1])
        except KeyboardInterrupt:
            break
