import tkinter as tk

yeah_no = True


master2 = tk.Tk()

class Var:
    def __init__(self):
        self.var = 0

var_1 = Var()

def set_blinker_start(var2):
    var2.var = 10

def set_var2(var2):
    var2.var = 2


tk.Label(master2, text='Enter time events')
tk.Button(master2, text='blinker start', command=lambda: set_blinker_start(var_1)).pack()
tk.Button(master2, text='haywan', command=lambda: set_var2(var_1)).pack()

master2.mainloop()

print(var_1.var)