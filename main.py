import tkinter as tk
import math
import numpy as np
from cg import *


class App:

    def __init__(self, master):

        # CONSTANTES -- BEGIN
        self.Kd = {'esfera':.3,'plano':.7}
        self.Ka = {'esfera':.6,'plano': .3}
        self.Ks = {'esfera':.8,'plano': .4}
        self.n = {'esfera':50,'plano': 5}
        self.Il = 1
        self.Ia = 1
        self.k = .01
        self.d = 1
        self.plane_color = (0, 0, 255)
        self.sphere_color = (255, 0, 255)
        self.background = (255, 255, 255)
        self.observer = [0, 0, 100]
        self.plane_vector = [0, 0, 100]
        self.light = [100, 0, 100]
        # CONSTANTES -- END

        # INTERFACE SETUP -- BEGIN
        self.master = master
        self.create_menu()
        self.master.config(menu=self.menu)
        self.canvas = tk.Canvas(self.master, height=768, width=1366, 
        background="#ffffff")        
        self.canvas.grid(row=0, column=0)
        # INTERFACE SETUP -- END
        
        #BUFFER SETUP BEGIN
        self.color_buffer = np.empty((1366, 768), dtype=object)
        
        self.fill_buffer()
        self.z_buffer = np.full((1366, 768), -100000)
        self.set_plane_into_buffer()
        self.set_sphere_into_buffer()
        self.color_buffer_changed = False
        #BUFFER SETUP END

        #DRAW BUFFER BEGIN
        self.draw_color_buffer()
        self.color_buffer_backup = self.color_buffer
        #DRAW BUFFER END

    def fill_buffer(self):
        for i in range(0, 1366):
            for j in range(0, 768):
                self.color_buffer[i][j] = self.background


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
    
    @classmethod
    def dot_product(cls, vector_v, vector_u):
        return (vector_v[0]*vector_u[0]+vector_v[1]*vector_u[1]+
        vector_v[2]*vector_u[2])


    def get_cos(self, vector_v, vector_u):
        dot_product = App.dot_product(vector_u,vector_v)
        product_norma = App.norma_vector(vector_v)*App.norma_vector(vector_u)

        return dot_product/product_norma        


    def equation_model_1(self, cos, objeto):
        if objeto == '':
            return self.Ia*self.Ka['plano']+self.Il*self.Kd['plano']*cos
        if objeto == 'plano':
            return self.Ia*self.Ka['plano']+self.Il*self.Kd['plano']*cos
        elif objeto == 'esfera':
            return self.Ia*self.Ka['esfera']+self.Il*self.Kd['esfera']*cos


    def equation_model_2(self, cos_theta, cos_a, objeto):
        if objeto == 'esfera':
            return self.Ia*self.Ka['esfera']+(self.Il/(self.d+self.k))*(self.Kd['esfera']*cos_theta+
                self.Ks['esfera']*cos_a**self.n['esfera'])
        else:
            return self.Ia*self.Ka['plano']+(self.Il/(self.d+self.k))*(self.Kd['plano']*cos_theta+
                self.Ks['plano']*cos_a**self.n['plano'])
        

    @classmethod
    def adjust(cls, r, g, b):
        if r > 255:
            r = 255
        if g > 255:
            g = 255
        if b > 255:
            b = 255
        return(r,g,b)

    def call_model_1(self):
        if(self.color_buffer_changed):
            self.color_buffer_changed = False
            self.color_buffer = self.color_buffer_backup

        cos_theta_plano = self.get_cos(self.plane_vector, self.light)
        cos_theta = 1
        obj = ''        
        I_plano = self.equation_model_1(cos_theta_plano, 'plano')
        
        

        for line in range(0, len(self.color_buffer)-1):
            
            for column in range(0, len(self.color_buffer[line])):
                
                v = self.color_buffer[line][column]
                if self.color_buffer[line][column] != self.background:
                    if self.color_buffer[line][column]==self.plane_color:
                        I = I_plano
                        obj = 'plano'
                        cos_theta = cos_theta_plano

                    elif self.color_buffer[line][column]==self.sphere_color:
                        
                        normal = [2*(line-683), 2*(column-384), 2*self.z_buffer[line][column]]
                        norma = App.norma_vector(normal)
                        normal =[normal[0], normal[1], normal[2]]
                        
                        
                        print(normal)
                        print(self.light)
                        cos_theta = self.get_cos(normal, self.light)
                        obj = 'esfera'

                    I = self.equation_model_1(cos_theta, obj)
                    
                    r = int(I*self.color_buffer[line][column][0])
                    g = int(I*self.color_buffer[line][column][1])
                    b = int(I*self.color_buffer[line][column][2])
                        
                    self.color_buffer[line][column] = App.adjust(r,g,b)
                    # print(f'antes: {v}, depois:{(r,g,b)}')
                    
        self.color_buffer_changed = True       
        self.draw_color_buffer()


    def call_model_2(self):
        if(self.color_buffer_changed):
            
            self.color_buffer = self.color_buffer_backup
            self.color_buffer_changed = False

        cos_theta_plano = self.get_cos(self.plane_vector, self.light)
        cos_a_plano = self.get_cos(self.plane_vector, self.observer)
        
        cos_theta = 1
        cos_a = 1
        obj = ''        
        I_plano = self.equation_model_2(cos_theta, cos_a, 'plano')
        

        for line in range(0, len(self.color_buffer)-1):
            
            for column in range(0, len(self.color_buffer[line])):
                # print(f'({line}, {column})')


                v = self.color_buffer[line][column]
                if self.color_buffer[line][column] != self.background:
                    if self.color_buffer[line][column]==self.plane_color:
                        I = I_plano
                        obj = 'plano'
                        cos_theta = cos_theta_plano
                        cos_a = cos_a_plano

                    elif self.color_buffer[line][column]==self.sphere_color:
                        
                        normal = [2*(line-683), 2*(column-384), 2*self.z_buffer[line][column]]
                        norma = App.norma_vector(normal)
                        normal =[normal[0], normal[1], normal[2]]
                        
                        cos_theta = self.get_cos(normal, self.light)
                        cos_a = self.get_cos(normal, self.observer)
                        obj = 'esfera'

                    I = self.equation_model_2(cos_theta, cos_a, obj)
                    
                    r = int(I*self.color_buffer[line][column][0])
                    g = int(I*self.color_buffer[line][column][1])
                    b = int(I*self.color_buffer[line][column][2])
                        
                    self.color_buffer[line][column] = App.adjust(r,g,b)
                    # print(f'antes: {v}, depois:{(r,g,b)}')
                    
        self.color_buffer_changed = True        
        self.draw_color_buffer()



    def rgb2hex(self, rgb):
        return '#%02x%02x%02x' % rgb


    def draw_color_buffer(self):
        if self.canvas:
            self.canvas.delete('all')
            self.canvas = None

        self.canvas = tk.Canvas(self.master, height=768, width=1366, 
        background="#ffffff")        
        self.canvas.grid(row=0, column=0)

        for line in range(len(self.color_buffer)):
            for column in range(len(self.color_buffer[line])):
                # print(self.rgb2hex(self.color_buffer[line][column]))
                # print(f'{line}, {column} ')
                if self.color_buffer[line][column]!=(255,255,255):
                    self.canvas.create_line(line, column, line+1,column,
                    fill=self.rgb2hex(self.color_buffer[line][column]))


    def set_plane_into_buffer(self):
        z_plane = 0
        for i in range(0, 101):
            for j in range(0, 101):
                
                if self.z_buffer[i+683][384-j] < z_plane:

                    self.z_buffer[i+683][384-j] = z_plane
                    self.color_buffer[i+683][384-j] = self.plane_color
        

    def set_sphere_into_buffer(self):
        for r in range (50, -1, -1):
            CG.circunferencia(683,384, r, self.canvas,self.z_buffer,
                self.color_buffer, color=self.sphere_color)
    

    @classmethod        
    def norma_vector(cls, vector):
        return (vector[0]**2+vector[1]**2+vector[2]**2)**(1/2)

def main():
    root = tk.Tk()
    root.geometry('%dx%d+%d+%d'% (1000, 1000, root.winfo_screenheight()/2, root.winfo_screenwidth()/2))
    # print(root.winfo_screenheight()/2)
    # print(root.winfo_screenwidth()/2)

    root.title('Trabalho de Computação Gráfica')
    root.attributes('-zoomed', True)
    app = App(root)
    root.mainloop()

main()