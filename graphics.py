import gridcreation as gc
import tkinter as tk

class Graphics:
    def __init__(self):
        self.root = tk.Tk()
        self.grid = gc.grid_reverse(64,32, root = self.root)
        self.previous1 = []
        self.previous2 = []

    def draw(self, x, y, mem, height):
#        print(x,y,mem, height)
        self.previous1 = self.previous2
        self.previous2 = []
        mem = bin(int("".join(mem), 16))[2:]
        flag = 0
        for y1 in range(height):
            for x1, state in enumerate(mem[y1*8:(1+y1)*8]):
                x2 = x+(x1+1)
                y2 = y+(y1+1)
                print((x2, y2))
                if x2 > 255:
                    x2 -= 255
                while x2 > 64:
                    x2 -= 64
                if y2 > 32:
                    y2 -= 32
                print((x2, y2))
                var = self.grid.varlist[self.grid.coords(x2, y2)]
                box = self.grid.boxlist[self.grid.coords(x2, y2)]
                cur = bool(int(state))
                if var.get() and not cur:
                    flag = 1
                var.set(cur)
                if cur:
                    if not (x2, y2) in self.previous1:
                        self.previous2.append((x2, y2))
                    box.configure(bg='black')
                else:
                    box.configure(bg='light gray')

        return flag

    def clear(self):
        for c, i in enumerate(self.grid.boxlist):
            i.config(bg='light gray')
            self.grid.varlist[c].set(False)
        self.root.update()

    def clear_previous(self):
        for i in self.previous1:
            var = self.grid.varlist[self.grid.coords(i)]
            box = self.grid.boxlist[self.grid.coords(i)]
            var.set(False)
            box.configure(bg='light gray')

if __name__ == "__main__":
    Graphics().root.mainloop()
