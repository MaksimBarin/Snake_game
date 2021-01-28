'''
Реализованные идеи:
- сохранение игры в файл
- создание поля по массиву (это позволяет сделать несколько различных карт, записав их массивами в разные фалы)
- использование клавиш для упраления змейкой
'''


from tkinter import *
from random import randint


def keyUp(event):
    global dy, dx, is_direction_changed
    if is_direction_changed:
        return
    if not dy:
        dy = -1
        dx = 0
        is_direction_changed = True


def keyDown(event):
    global dy, dx, is_direction_changed
    if is_direction_changed:
        return
    if not dy:
        dy = 1
        dx = 0
        is_direction_changed = True


def keyLeft(event):
    global dy, dx, is_direction_changed
    if is_direction_changed:
        return
    if not dx:
        dx = -1
        dy = 0
        is_direction_changed = True


def keyRight(event):
    global dy, dx, is_direction_changed
    if is_direction_changed:
        return
    if not dx:
        dx = 1
        dy = 0
        is_direction_changed = True


def apple():
    global x_apl, y_apl
    x_apl, y_apl = randint(0, width-1), randint(0, height-1)
    # пока координаты яблока совпадают с координатами любого сегмента змейки
    while [x_apl, y_apl] in bits or borders[y_apl][x_apl]:
        # координаты яблока получают другие значения
        x_apl, y_apl = randint(0, width-1), randint(0, height-1)


def load(event=None):
    global width, height
    with open('snake_save.txt', 'r') as file:
        game_dict = eval(file.read())
    for perem in game_dict:
        globals()[perem] = game_dict[perem]
    width = len(borders[0])
    height = len(borders)
    canv["width"] = width*a
    canv["height"] = height*a
    status_label['text'] = "загрузилось последнее сохранение"
    if not game_is_on:
        newframe()


def save(event=None):
    global game_dict
    game_dict = {}
    for perem in ['a', 'x', 'y', 'dx', 'dy', 'bits', 'x_apl', 'y_apl', 'borders', 'is_direction_changed']:
        game_dict[perem] = globals()[perem]
    with open('snake_save.txt', 'w') as file:
        file.write(str(game_dict))
    status_label['text'] = "игра сохранена"


def newframe():
    global x, y, dx, dy, fig, bits, game_is_on, is_direction_changed

    x = (x+dx) % width
    y = (y+dy) % height

    # если "голова"" змейки наехала на её "хвост" или препятствие
    if [x, y] in bits or borders[y][x]:
        status_label['text'] = "Crash"
        game_is_on = False
        return
    bits = bits + [[x, y]]

    # если "голова" змейки на яблоке
    if x == x_apl and y == y_apl:
        status_label['text'] = str(len(bits) - start_snake_len)
        apple()

    else:
        bits = bits[1:]

    canv.delete(ALL)
    border = canv.create_rectangle(0, 0, width*a, height*a, width=2, fill="black", offset="0,0")

    # отображение препятствий
    for y in range(len(borders)):
        for x in range(len(borders[y])):
            if borders[y][x]:
                canv.create_rectangle(x*a, y*a, (x+1)*a, (y+1)*a, width=2, fill="yellow", offset="0,0")

    for x, y in bits:
        canv.create_rectangle(x*a, y*a, x*a+a, y*a+a, width=2, fill="green")
    canv.create_oval([x_apl*a, y_apl*a], [x_apl*a+a, y_apl*a+a], fill="red")
    
    is_direction_changed = False
    tk.after(100, newframe)


borders = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
           [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0], \
           [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0], \
           [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0], \
           [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0], \
           [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0], \
           [0,0,0,0,0,0,0,0,1,1,1,1,1,1,0], \
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]  ]

width = len(borders[0]) # 40
height = len(borders) # 30

a = 15
dx = 1
dy = 0
bits = [] # список пар значений [x, y - координаты фигуры на Canvas]
x = y = 2
start_snake_len = 3
game_is_on = True
is_direction_changed = False


# создание первых сегментов змейки
for i in range(start_snake_len):
    x += i*10
    bits.append([20+i*a, 20])

tk = Tk()
canv = Canvas(width=width*a, height=height*a)
but_load = Button(text="Загрузить", command=load)
but_save = Button(text="Сохранить", command=save)
status_label = Label(text="Добро пожаловать!")

status_label.pack()
canv.pack()
but_load.pack()
but_save.pack()

apple()
newframe()

tk.bind("<Up>", keyUp)
tk.bind("<Down>", keyDown)
tk.bind("<Left>", keyLeft)
tk.bind("<Right>", keyRight)
tk.bind("<s>", save)
tk.bind("<l>", load)

mainloop()