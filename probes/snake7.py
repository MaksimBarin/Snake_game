# В самом начале программы подключаем нужные модули
from tkinter import *
from random import randint, choice

# =========================================================================
# ===================    объявление собственных    ========================
# ===================            функций           ========================
# =========================================================================
# Место для функций, которые будут реагировать на нажания клавиш
def left(a):
    global dx, dy
    # if квадрат не двигается по горизонтали (dx = 0):
    # if dx == 0:
    if not dx:
        dx = -side
        dy = 0

def right(a):
    global dx, dy
    if not dx:
        dx = side
        dy = 0

def up(a):
    global dx, dy
    if not dy:
        dx = 0
        dy = -side

def down(a):
    global dx, dy
    if not dy:
        dx = 0
        dy = side
    

# функция redraw() обновляет экран
def redraw():
    global x, y, frame_time
    
    if flag:
        x += dx
        x %= width
        y += dy
        y %= height
        if frame_time > 100:
            frame_time -= 1
        else:
            frame_time = 100

        if [x, y] in bits:
            print("shit happens -_-")
            return
        bits.append([x,y])

        if x == xap and y == yap:
            lbl['text'] = '+1'
            score_lbl['text'] += 1
            if apl_color == 'gold':
                score_lbl['text'] += 2
                lbl['text'] = '+3'
            lbl.place(x=bits[-1][0]+side, y=bits[-1][1]-side)
            apple()
        else:
            del bits[0]

    canv.delete(ALL)
    for xbit,ybit in bits:
        canv.create_rectangle(xbit, ybit, xbit+side, ybit+side, fill='dark green')
    canv.create_oval(xap, yap, xap+side, yap+side, fill=apl_color)

    main.after(frame_time, redraw)


# Ниже будет функция для создания случайных координат яблока
def apple():
    global xap, yap, apl_color
    xap = randint(0, width-side) // side * side
    yap = randint(0, height-side) // side * side
    apl_color = choice(['red'] * 9 + ['gold'])
    while [xap, yap] in bits:
        print("ATTANSION: APPLE ON SNAKE!!!")
        apple()

# Здесь, если успеем, напишем функцию для режима "пауза"
def pause():
    global flag
    print("press button")
    flag = not flag


def start():
    global side, x, y, dx, dy, start_pack, bits, xap, yap, apl_color, frame_time, flag

    score_lbl['text'] = 0

    # Блок, в котором мы создаём необходимые переменные и константы
    side = 20
    x, y = 20, 20
    dx, dy = side, 0
    start_pack = 3
    bits = []

    xap = yap = 0
    apl_color = "red"

    frame_time = 400
    flag = True

    # Место сотворения змейки в её первозданном виде
    for i in range(start_pack):
        bits.append([x+i*side,y])
    x, y = bits[-1][0], bits[-1][1]
    # bits = [[20,20], [40,20], [60,20]]

    apple()
    redraw()


# =========================================================================
# ========================    игровая логика    ===========================
# =========================================================================

# Блок, отвечающий за создание окна и расстановки в нём виджетов
main = Tk()
pause_button = Button(text="pause", command=pause)
restart_btn = Button(text="restart", command=start)
width, height = 400, 400
canv = Canvas(width=width, height=height, bg='light yellow')
lbl = Label(text="+1", bg='light yellow')
score_lbl = Label(text=0, bg='light yellow')

canv.pack()
pause_button.pack()
restart_btn.pack()
score_lbl.place(x=width-12, y=2)

start()

# Назначаем бинды кнопок, формат такой -> название_окна.bind("название_кнопки", название_функции)
main.bind("<Left>", left)
main.bind("<Right>", right)
main.bind("<Up>", up)
main.bind("<Down>", down)

# Это конец программы, после функции mainloop() ничего не пишем
mainloop()
