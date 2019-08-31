import tkinter as tk
class grid:
    def __init__(
        self, numberx, numbery=None, text = '', xoffset = 0, yoffset = 0,
        command = None, root = None, do_title = True
    ):
        if not root:
            root = tk.Tk()
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.text = text
        self.root = root
        self.boxlist, self.varlist = [], []
        self.numberx, self.numbery = numberx, numbery
        self.xgrid, self.ygrid = 0, 0
        if do_title:
            self.root.title('gridcreation')

        self.coordrost = [[i for i in range(self.numberx*x,self.numberx+self.numberx*x)] for x in range(numbery)]

        for i in range(10000):
            self.varlist.append(tk.BooleanVar())
            self.boxlist.append(tk.Checkbutton(
                self.root,
                text=self.text,
                variable=self.varlist[i],
                command = command,
                highlightthickness=0,
            )
            )
            row, col = self.ygrid+self.yoffset, self.xgrid + self.xoffset
            self.boxlist[i].grid(row=row, sticky=tk.W, column=col)
            self.boxlist[i].configure(bg='light gray')
            self.xgrid += 1
            if self.xgrid == self.numberx:
                self.ygrid += 1
                self.xgrid = 0

            if self.ygrid == self.numbery:
                break


    def coords(self, x, y=None):
        if type(x) == tuple or type(x) == list:
            x, y = x[0], x[1]
        elif not y:
            print('Please enter a y')
            return
        return self.coordrost[self.numbery-y][x-1]
    def uncoords(self, coord):
        for i in range(len(self.coordrost)):
            if coord in self.coordrost[i]:
                x1 = self.coordrost[i].index(coord) + 1
                y1 = self.numbery - i
                return [x1, y1]

class grid_reverse:
    def __init__(self, numberx, numbery=None, text = '', xoffset = 0, yoffset = 0, command = None, root = None, do_title = True):
        if not root:
            root = tk.Tk()
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.text = text
        self.root = root
        self.boxlist, self.varlist = [], []
        self.numberx, self.numbery = numberx, numbery
        self.xgrid, self.ygrid = 0, 0
        if do_title:
            self.root.title('gridcreation')

        self.coordrost = [[i for i in range(self.numberx*x,self.numberx+self.numberx*x)] for x in range(numbery)]
        for i in range(10000):
            self.varlist.append(tk.IntVar())
            #self.boxlist.append(Checkbutton(self.root, text=f'{self.uncoords(i)} ({i})', variable=self.varlist[i]))
            self.boxlist.append(tk.Checkbutton(
                self.root,
                text=self.text,
                variable=self.varlist[i],
                command = command,
                highlightthickness=0,
            ))
            row, col = self.ygrid+self.yoffset, self.xgrid + self.xoffset
            self.boxlist[i].grid(row=row, sticky=tk.W, column=col)
            self.boxlist[i].configure(bg='light gray')
            self.xgrid += 1
            if self.xgrid == self.numberx:
                self.ygrid += 1
                self.xgrid = 0

            if self.ygrid == self.numbery:
                break


    def coords(self, x, y=None):
        if type(x) == tuple or type(x) == list:
            x, y = x[0], x[1]
        elif not y:
            print('Please enter a y')
            return
        return self.coordrost[y-1][x-1]
    def uncoords(self, coord):
        for i in range(len(self.coordrost)):
            if coord in self.coordrost[i]:
                x1 = self.coordrost[i].index(coord) + 1
                y1 = i + 1
                return [x1, y1]


if __name__ == "__main__":
    def hey():
        print('hey')
    grid1 = grid(2,2, command=hey)
    grid1.root.mainloop()
