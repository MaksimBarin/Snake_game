import tkinter as tk
from random import randint

def new_game():
    label['text'] = 'button click'


def up_func(event):
    global dx, dy
    if not dy:
        dx = 0
        dy = -side
    if flag:
        label['text'] = 'key "W" pressed'

def down_func(event):
    global dx, dy
    if not dy:
        dx = 0
        dy = side
    if flag:
        label['text'] = 'key "S" pressed'

def left_func(event):
    global dx, dy
    if not dx:
        dx = -side
        dy = 0
    if flag:
        label['text'] = 'key "A" pressed'

def right_func(event):
    global dx, dy
    if not dx:
        dx = side
        dy = 0
    if flag:
        label['text'] = 'key "D" pressed'


def computer():
    global x, y, xa, ya, score, flag
    x = x + dx
    x %= WIDTH
    y = y + dy
    y %= HEIGH

    # если произошёл наезд
    if [x, y] in bits:
        flag = False
        label['text'] = f'GAME OVER\nscore: {score}'
        return None

    bits.append([x, y])
    
    if x == xa and y == ya:
        score += 1
        label['text'] = f'score: {score}'
        xa, ya = ap()
    else:
        del bits[0]

    canv.delete(tk.ALL)
    for xbit, ybit in bits:
        if [xbit, ybit] == bits[-1]:
            canv.create_rectangle(xbit, ybit, xbit + side, ybit + side, fill='DeepPink4', width=1.5)
        else:
            canv.create_rectangle(xbit, ybit, xbit + side, ybit + side, fill='plum4', width=1.5)
    canv.create_oval(xa, ya, xa + side, ya + side, fill='blue2', width=1)

    main.after(100, computer)


def ap():
    x = randint(0, WIDTH - side)
    x -= x % side
    y = randint(0, HEIGH - side)
    y -= y % side
    # исключение варианта отрисовки яблока на змейке
    if [x, y] in bits:
        return ap()
    return x, y


main = tk.Tk()

flag = True

WIDTH, HEIGH = 400, 400
x, y = 200, 200
side = 20
dx = 0
dy = side
bits = [[x, y - 2 * side], 
        [x, y - side], 
        [x, y]]
score = 0

xa, ya = ap()


canv = tk.Canvas(main, bg='azure', width=WIDTH, heigh=HEIGH)
button = tk.Button(main, text='new game', command=new_game)
label = tk.Label(main, text="")

# canv.create_rectangle(x, y, x + side, y + side)

canv.grid()
button.grid()
label.grid()

computer()


main.bind('<w>', up_func) # <Up> <Down> <Left> <Right>
main.bind('<Up>', up_func)

main.bind('<s>', down_func)
main.bind('<Down>', down_func)

main.bind('<a>', left_func)
main.bind('<Left>', left_func)

main.bind('<d>', right_func)
main.bind('<Right>', right_func)

main.mainloop()