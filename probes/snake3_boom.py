from tkinter import *
from random import randint


# ====================================================
# =======    объявление собственных функций    =======
# ====================================================

def Up(p):
    global dx, dy
    if not dy:
        dx = 0
        dy = -side
    print("'up' pressed")

def Down(p):
    global dx, dy
    if not dy:
        dx = 0
        dy = side
    print("'down' pressed")
        

def Left(p):
    global dx, dy
    if not dx:
        dx = -side
        dy = 0
    print("'left' pressed")

def Right(p):
    global dx, dy
    if not dx:
        dx = side
        dy = 0
    print("'right' pressed")


def redraw():
    global x, y, score_widget

    if flag:
        x += dx
        x %= width
        y += dy
        y %= height
        canv.delete(ALL)

        # crach check
        if [x, y] in bits:
            canv.grid_remove()
            score_widget.grid_remove()
            canv.grid_remove()
            velocity_wid.grid_remove()
            pause_button.grid_remove()

            final_widget["text"] = "BOOM!!!\n" + "score: " + str(len(bits)-3) 
            final_widget.grid()
            print("BOOM!")
            return
        bits.append([x, y])

        # apple check
        if x == xapp and y == yapp:
            score_widget["text"] = len(bits)-3
            apple()
        else:
            del bits[0]

    for x_b, y_b in bits:
        canv.create_rectangle(x_b, y_b, x_b+side, y_b+side, fill='PaleGreen2')
    canv.create_oval(xapp, yapp, xapp+side, yapp+side, fill='chocolate1')

    # вызвать саму себя
    tk.after(velocity_wid.get(), redraw)


def apple():
    global xapp, yapp
    # генерим координаты яблока
    xapp = randint(0, width-side) // side * side
    yapp = randint(0, height-side) // side * side
    if [xapp, yapp] in bits:
        apple()


def pause():
    global flag
    flag = not flag
    print(flag)


# ====================================================
# =========    создание основных объектов    =========
# ====================================================

width = 600
height = 420
tk = Tk()
pause_button = Button(text='start/pause', command=pause)
canv = Canvas(width=width, height=height, bg='azure')
velocity_wid = Scale(tk, orient=HORIZONTAL, from_=50, to=500)
velocity_wid.set(300)
score_widget = Label(tk, text=0)
final_widget = Label(tk, text='', padx=width//3, pady=height//3, font=("Times", 40))


score_widget.grid()
canv.grid()
velocity_wid.grid()
pause_button.grid()

x, y = 300, 180
side = 30
dx, dy = 0, side
bits = []
flag = False

for i in range(3):
    bits.append([x, y+i*side])
print(bits)
x = bits[-1][0]
y = bits[-1][1]

apple()
redraw()

tk.bind("<Up>", Up)
tk.bind("<Down>", Down)
tk.bind("<Left>", Left)
tk.bind("<Right>", Right)

mainloop()