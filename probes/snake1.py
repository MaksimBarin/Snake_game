from tkinter import *
from random import randint

# =========================================================================
# ===================    объявление собственных    ========================
# ===================            функций           ========================
# =========================================================================
def keyUp(a):
    # против оси y
    global dx, dy
    if not dy:
        dx = 0
        dy = -side

def keyDown(a):
    # по оси y
    global dx, dy
    if not dy:
        dx = 0
        dy = side

def keyLeft(a):
    # против оси x
    global dx, dy
    if not dx:
        dx = -side
        dy = 0

def keyRight(a):
    # по оси x
    global dx, dy
    if not dx:
        dx = side
        dy = 0


def redraw():
    global x, y, xapl, yapl, apple_time
    if flag:
        x += dx 
        x %= width
        y += dy
        y %= width
        canv.delete(ALL)

        apple_time += speed_arm.get()
        if apple_time / 1000 > 6.0:
            apple_time = 0
            apple()

        # проверка самопересечения:
        if [x, y] in bits:
            print("Busted")
            return
        bits.append([x,y])

        # проверка наезда на яблоко
        if x == xapl and y == yapl:
            apple_time = 0
            apple()
            score_lbl["text"] = str(len(bits)-3)
        else:
            del bits[0]

    # отрисовка всех элементов
    for xbit, ybit in bits:
        canv.create_rectangle(xbit, ybit, xbit+side, ybit+side, fill='khaki', outline='HotPink4', width=2)
    canv.create_oval(xapl, yapl, xapl+side, yapl+side, fill='tomato', width=1.5)

    tk.after(speed_arm.get(), redraw)

def pause():
    global flag
    flag = not flag
    print("button pressed")

def restart():
    global x, y, dx, dy, bits
    bits = []
    x, y = 50, 50
    dx, dy = side, 0

    for i in range(3):
        bits.append([x, y+i*side])
    x = bits[-1][0]
    y = bits[-1][1]

    apple()
    redraw()


def apple():
    global xapl, yapl
    # генерим координаты для яблока и приводим к значениям, кратным стороне квадрата
    xapl = randint(0, width-side) // side * side
    yapl = randint(0, height-side) // side * side
    if [xapl, yapl] in bits:
        apple()

# =========================================================================
# ========================    игровая логика    ===========================
# =========================================================================

tk = Tk()
width = 400
height = 400
canv = Canvas(width=width, height=height, bg="light cyan")
but = Button(text="pause", command=pause)
but_restart = Button(text="restart", command=restart)
speed_arm = Scale(tk, orient=HORIZONTAL, length=width//2, from_=50, to=1000, resolution=1)
speed_arm.set(400)
flag = True
apple_time = 0

canv.pack()
speed_arm.pack()
but.pack()
but_restart.pack()


side = 25
x, y = 50, 50
dx, dy = side, 0
bits = [] # список для хранения координат частей змейки


for i in range(3):
    bits.append([x, y+i*side])
x = bits[-1][0]
y = bits[-1][1]

# неудавшийся эксперимент с отображением счета
score_lbl = Label(tk, text=str(len(bits)-3), font=("Helvetica", 16))
score_lbl.pack()

apple()
redraw()


tk.bind("<Left>", keyLeft)
tk.bind("<Up>", keyUp)
tk.bind("<Right>", keyRight)
tk.bind("<Down>", keyDown)

mainloop()