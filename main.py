import tkinter as tk
import math
import numpy as np
from cg import *

class App:

    def __init__(self, master):
        self.master = master
        self.create_menu()
        self.master.config(menu=self.menu)

        self.z_buffer = np.full((1366, 768), -100000)
        self.color_buffer = np.full((1366, 768), '#ffffff')
        self.observer = [0, 0, 100]
        self.light = [100, 0, 100]
        self.plane = []
        self.sphere = []
        
        self.canvas = tk.Canvas(self.master, height=768, width=1366, 
        background="#ffffff")        
        self.canvas.grid(row=0, column=0)
        self.set_plane()
        self.set_sphere()
        self.draw_color_buffer()

    def create_menu(self):
        self.menu = tk.Menu(self.master)
        self.model_1 = tk.Menu(self.menu)
        self.model_2 = tk.Menu(self.menu)
        self.model_1.add_command(
        label='Aplicar modelo',
        command=self.call_model_1)
        self.model_2.add_command(
            label=
            'Aplicar modelo'
            ,command=self.call_model_2)
        
        self.menu.add_cascade(label=
            'Ia.Ka+Il.kd.cos(theta)', menu=self.model_1)
        
        self.menu.add_cascade(label=
            '(Ia.Ka+Il/(d+k))(Kd.cos(theta) + Ks.cos^n(a))',
            menu=self.model_2)
    

    def call_model_1(self):
        pass


    def call_model_2(self):
        pass

    def draw_color_buffer(self):

        for line in range(len(self.color_buffer)):
            for column in range(len(self.color_buffer[line])):
                if self.color_buffer[line][column] != '#ffffff':
                    self.canvas.create_line(line, column, line+1,column,
                     fill=self.color_buffer[line][column])
                

    def set_plane(self):
        for i in range(0, 101):
            for j in range(0, 101):
                self.plane.append((i, j, 0, 1))
                if self.z_buffer[i+683][384-j] < 0:
                    self.z_buffer[i+683][384-j] = 0
                    self.color_buffer[i+683][384-j] = '#0000ff'
        

    def set_sphere(self):
        for r in range (50, -1, -1):
            CG.circunferencia(684,384, r, self.canvas,self.z_buffer,
                self.color_buffer, color='#ff00ff')

            



    def draw_plane(self):
        ort = np.array([   [1, 0, 0, 0],
                           [0, 1, 0, 0],
                           [0, 0, 0, 0],
                           [0, 0, 0, 1]])
        new_points = []
        for vector in self.plane:
            new_points.append(np.dot(vector, ort))    

        for point in new_points:
            CG.line_breasenham(point[0]+683, point[1]+384,point[0]+683,
            point[1]+384, self.canvas,point[2], self.z_buffer, color='#0000ff')
            print(f'x0: {point[0]+683} y0:{point[1]+384} x1: {point[2]+683} y1:{point[3]+384}')
            



def main():
    root = tk.Tk()
    root.geometry('%dx%d+%d+%d'% (1000, 1000, root.winfo_screenheight()/2, root.winfo_screenwidth()/2))
    root.title('Trabalho de Computação Gráfica')
    root.attributes('-zoomed', True)
    app = App(root)
    root.mainloop()

main()