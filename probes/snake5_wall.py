from tkinter import *
from random import randint
# import tkinter as tk


# ========    объявляем функции    ========
def keyUp(a):
    global dx, dy
    if not dy:
        dy = -side
        dx = 0

def keyDown(a):
    global dx, dy
    if not dy:
        dy = side
        dx = 0

def keyLeft(a):
    global dx, dy
    if not dx:
        dx = -side
        dy = 0

def keyRight(a):
    global dx, dy
    if not dx:
        dx = side
        dy = 0


def new_frame():
    global x, y, snake_parts, x_ap, y_ap
    x = (x+dx) % width
    y = (y+dy) % height
    canv.delete(ALL)

    # проверим, наехала ли змейка головой на свой хвост или на ящик
    if [x, y] in snake_parts or [x, y] in boxes:
        print("Смерть")
        return
    # добавляем новую голову в список (внутри памяти компьютера)
    snake_parts = snake_parts + [[x, y]]

    # проверим наезд головы на яблоко
    if x == x_ap and y == y_ap:
        apple()
    else:
        # удалим хвост (операция внутри памяти компьютера)
        snake_parts = snake_parts[1:]

    # когда-то это прога рисовала только один квадрат -> canv.create_rectangle(x, y, x+side, y+side)
    # отрисовка змейки по содержимому списка snake_parts
    for x_part, y_part in snake_parts:
        # x -> snake_parts[i][0]
        # y -> snake_parts[i][1]
        # canv.create_rectangle(snake_parts[i][0], snake_parts[i][1], snake_parts[i][0]+side, snake_parts[i][1]+side)
        canv.create_rectangle(x_part, y_part, x_part+side, y_part+side, fill="green")
    canv.create_oval(x_ap, y_ap, x_ap+side, y_ap+side, fill="red")

    for x_box, y_box in boxes:
        canv.create_rectangle(x_box, y_box, x_box+side, y_box+side, fill="saddle brown")

    # print(snake_parts)

    tk.after(100, new_frame)

def apple():
    global x_ap, y_ap
    x_ap = randint(0, width-side)
    x_ap = x_ap - x_ap % side
    y_ap = randint(0, height-side)
    y_ap = y_ap - y_ap % side
    while [x_ap, y_ap] in snake_parts or [x_ap, y_ap] in boxes:
        apple()


# ========    создаём основные объекты приложения    ========
tk = Tk()
width = 400
height = 400
# button = Button(text="button", command=butt)
canv = Canvas(bg='old lace', width=width, height=height)
# button.pack()
canv.pack()

x = y = 100
dx = 20
dy = 0
side = 20
snake_parts = []
boxes = []

# создадим преграду для змеи
for i in range(6):
    for j in range(2):
        boxes = boxes + [[180+j*side, 140+i*side]]

# snake_parts = snake_parts + [[x, y]]
# создадим в цикле 3 первых сегмента змейки
start_pack = 5
for i in range(start_pack):
    snake_parts = snake_parts + [[x + i*side, y]]
x = x + (start_pack-1)*side
print(snake_parts)

apple()
new_frame()

# tk.bind(/название клавиши/, /название функции, которая должна сработать/)
tk.bind("<Up>", keyUp)
tk.bind("<Down>", keyDown)
tk.bind("<Left>", keyLeft)
tk.bind("<Right>", keyRight)

mainloop()