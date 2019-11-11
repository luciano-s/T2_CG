import tkinter as tk
import math
import numpy as np
from cg import *

class App:

    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(self.master, height=768, width=1366, 
        background="#ffffff")
        self.canvas.grid(row=0, column=0)
        self.z_buffer = np.full((768, 1366), -100000)
        self.observer = [0, 0, 100]
        self.light = [100, 0, 100]
        self.plane = []
        self.sphere = [0, 0, 0]
        self.draw_sphere()
        self.set_plane()
        self.draw_plane()


    def set_plane(self):
        for i in range(0, 101):
            for j in range(0, 101):
                self.plane.append((i, j, 0, 1))
                self.z_buffer[i][j] = math.sqrt(i**2 + j**2)


    def draw_sphere(self):

        for r in range (50, -1, -1):
            
            CG.circunferencia(683,384, r, self.canvas, color='#ff00ff')
            CG.circunferencia(684,384, r, self.canvas, color='#ff00ff')


    def draw_plane(self):
        ort = np.array([[1, 0, 0, 0],
                           [0, 1, 0, 0],
                           [0, 0, 0, 0],
                           [0, 0, 0, 1]])
        new_points = []
        for vector in self.plane:
            new_points.append(np.dot(vector, ort))    

        for point in new_points:
            CG.line_breasenham(point[0]+683, point[1]+384,point[0]+684,
            point[1]+385, self.canvas, color='#0000ff')
            



def main():
    root = tk.Tk()
    root.geometry('%dx%d+%d+%d'% (1000, 1000, root.winfo_screenheight()/2, root.winfo_screenwidth()/2))
    root.title('Trabalho de Computação Gráfica')
    root.attributes('-zoomed', True)
    app = App(root)
    root.mainloop()

main()