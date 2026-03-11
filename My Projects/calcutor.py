from tkinter import *

def press(num):
    global expression
    expression = expression + str(num)
    equation.set(expression)

def equalpress():
    global expression
    try:
        total = str(eval(expression))
        equation.set(total)
        expression = total
    except:
        equation.set(" error ")
        expression = ""

def clear():
    global expression
    expression = ""
    equation.set("")

root = Tk()
root.title("Calculator")
root.geometry("270x150")

expression = ""
equation = StringVar()

entry = Entry(root, textvariable=equation)
entry.grid(columnspan=4)

Button(root, text='1', command=lambda: press(1)).grid(row=1, column=0)
Button(root, text='2', command=lambda: press(2)).grid(row=1, column=1)
Button(root, text='3', command=lambda: press(3)).grid(row=1, column=2)
Button(root, text='+', command=lambda: press("+")).grid(row=1, column=3)

Button(root, text='4', command=lambda: press(4)).grid(row=2, column=0)
Button(root, text='5', command=lambda: press(5)).grid(row=2, column=1)
Button(root, text='6', command=lambda: press(6)).grid(row=2, column=2)
Button(root, text='-', command=lambda: press("-")).grid(row=2, column=3)

Button(root, text='7', command=lambda: press(7)).grid(row=3, column=0)
Button(root, text='8', command=lambda: press(8)).grid(row=3, column=1)
Button(root, text='9', command=lambda: press(9)).grid(row=3, column=2)
Button(root, text='*', command=lambda: press("*")).grid(row=3, column=3)

Button(root, text='C', command=clear).grid(row=4, column=0)
Button(root, text='0', command=lambda: press(0)).grid(row=4, column=1)
Button(root, text='=', command=equalpress).grid(row=4, column=2)
Button(root, text='/', command=lambda: press("/")).grid(row=4, column=3)

root.mainloop()
