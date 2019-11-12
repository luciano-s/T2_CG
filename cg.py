from tkinter import *
from tkinter import messagebox
import numpy as np
import math

# CLASSE QUE IMPLEMENTA A MAIORIA DOS ALGORITMOS UTILIZADOS

class CG:

    def __init__(self):
        self.center_x = 683
        self.center_y = 438
        self.A = [100, 100, 100, 1]
        self.B = [100, 100, 250, 1]
        self.C = [150, 100, 320, 1]
        self.D = [200, 100, 250, 1]
        self.E = [200, 100, 100, 1]
        self.F = [100, 200, 100, 1]
        self.G = [100, 200, 250, 1]
        self.H = [150, 200, 320, 1]
        self.I = [200, 200, 250, 1]
        self.J = [200, 200, 100, 1]

        self.A2 = [0, 0, 0]
        self.B2 = [0, 0, 0]
        self.C2 = [0, 0, 0]
        self.D2 = [0, 0, 0]
        self.E2 = [0, 0, 0]
        self.F2 = [0, 0, 0]
        self.G2 = [0, 0, 0]
        self.H2 = [0, 0, 0]
        self.I2 = [0, 0, 0]
        self.J2 = [0, 0, 0]

        self.projecao = None
        self.plano = None

        

        #self.figura = {'A': [self.A, self.A2, 'B', 'E', 'F'], 'B': [self.B, self.B2, 'C', 'D', 'G'],
        #               'C': [self.C, self.C2, 'D', 'H'], 'D': [self.D, self.D2, 'E', 'I'], 'E': [self.E, self.E2, 'J'],
        #               'F': [self.F, self.F2, 'G', 'J'], 'G': [self.G, self.G2, 'H', 'I'], 'H': [self.H, self.H2, 'I'],
        #               'I': [self.I, self.I2, 'J'], 'J': [self.J, self.J2]}

    @classmethod
    def line_breasenham(cls, x0, y0, x1, y1, canvas,z,zbuffer, color):
        dx = abs(x1-x0)
        dy = abs(y1-y0)
        d = 0
        if (dy < dx):  # x cresce mais rápido do que y
            if x0 < x1:  # esquerda->direita

                if y0 < y1:  # cima->baixo
                    # octante 1
                    y = y0
                    for x in range(x0, x1+1):
                        if zbuffer[int(x)][int(y)] < z:
                            canvas.create_line(x, y, x+1, y+1, fill=color)
                        if d < 0:
                            d += dy

                        else:
                            d += dy-dx
                            y += 1
                else:  # baixo->cima
                    # octante 8
                    y = y0
                    for x in range(x0, x1+1):
                        if zbuffer[int(x)][int(y)] < z:
                            canvas.create_line(x, y, x+1, y+1, fill=color)
                        if d < 0:
                            d += dy

                        else:
                            d += dy-dx
                            y -= 1
            else:  # direita->esquerda
                if y0 < y1:  # cima->baixo
                    # octante 4
                    y = y0

                    for x in range(x0, x1, -1):
                        if zbuffer[int(x)][int(y)] < z:
                            canvas.create_line(x, y, x+1, y+1, fill=color)
                        if d < 0:
                            d += dy

                        else:
                            d += dy-dx
                            y += 1
                else:  # baixo->cima
                    # octante 5
                    y = y0
                    for x in range(x0, x1, -1):
                        if zbuffer[int(x)][int(y)] < z:
                            canvas.create_line(x, y, x+1, y+1, fill=color)
                        if d < 0:
                            d += dy

                        else:
                            d += dy-dx
                            y -= 1

        else:  # y cresce mais rapido
            if y0 < y1:
                # cima -> baixo
                if x0 < x1:
                    # esquerda->direita
                    # octeto 2
                    x = x0
                    for y in range(y0, y1):
                        print(f'x:{x} y:{y}')
                        if zbuffer[int(x)][int(y)] < z:
                            canvas.create_line(x-1, y-1, x, y, fill=color)
                        if 0 < d:
                            d -= dx
                        else:
                            d += dy-dx
                            x += 1
                else:
                    # direita->esquerda
                    # octeto 3
                    x = x0
                    for y in range(y0, y1+1):
                        if zbuffer[int(x)][int(y)] < z:
                            canvas.create_line(x, y, x+1, y+1, fill=color)
                        if 0 < d:
                            d -= dx
                        else:
                            d += dy-dx
                            x -= 1

            else:
                if x0 < x1:
                    # esquerda->direita
                    # octeto 7
                    x = x0
                    for y in range(y0, y1, -1):
                        if zbuffer[int(x)][int(y)] < z:
                            canvas.create_line(x, y, x+1, y+1, fill=color)
                        if 0 < d:
                            d -= dx
                        else:
                            d += dy-dx
                            x += 1
                else:
                    # direita->esquerda
                    # octeto 6
                    x = x0
                    for y in range(y0, y1, -1):
                        if zbuffer[int(x)][int(y)] < z:
                            canvas.create_line(x, y, x+1, y+1, fill=color)
                        if 0 < d:
                            d -= dx
                        else:
                            d += dy-dx
                            x -= 1

    @classmethod
    def draw_circle(cls, xc, yc, x, y, canvas, zbuffer,r,colorbuffer, color='#ff00ff'):
        
        if (50-r) > zbuffer[int(xc)+int(x)][int(yc)+int(y)]:
            zbuffer[int(xc)+int(x)][int(yc)+int(y)] = 50-r
            zbuffer[int(xc)-int(x)][int(yc)+int(y)] = 50-r
            zbuffer[int(xc)+int(x)][int(yc)-int(y)] = 50-r
            zbuffer[int(xc)-int(x)][int(yc)-int(y)] = 50-r
            zbuffer[int(xc)+int(y)][int(yc)+int(x)] = 50-r
            zbuffer[int(xc)-int(y)][int(yc)+int(x)] = 50-r
            zbuffer[int(xc)+int(y)][int(yc)-int(x)] = 50-r
            zbuffer[int(xc)-int(y)][int(yc)-int(x)] = 50-r
            colorbuffer[int(xc)+int(x)][int(yc)+int(y)] = color
            colorbuffer[int(xc)-int(x)][int(yc)+int(y)] = color
            colorbuffer[int(xc)+int(x)][int(yc)-int(y)] = color
            colorbuffer[int(xc)-int(x)][int(yc)-int(y)] = color
            colorbuffer[int(xc)+int(y)][int(yc)+int(x)] = color
            colorbuffer[int(xc)-int(y)][int(yc)+int(x)] = color
            colorbuffer[int(xc)+int(y)][int(yc)-int(x)] = color
            colorbuffer[int(xc)-int(y)][int(yc)-int(x)] = color

            # canvas.create_line(xc+x-1, yc+y-1, (xc+x), (yc+y), fill=color)
            # canvas.create_line(xc-x-1, yc+y-1, (xc-x), (yc+y), fill=color)
            # canvas.create_line(xc+x-1, yc-y-1, (xc+x), (yc-y), fill=color)
            # canvas.create_line(xc-x-1, yc-y-1, (xc-x), (yc-y), fill=color)
            # canvas.create_line(xc+y-1, yc+x-1, (xc+y), (yc+x), fill=color)
            # canvas.create_line(xc-y-1, yc+x-1, (xc-y), (yc+x), fill=color)
            # canvas.create_line(xc+y-1, yc-x-1, (xc+y), (yc-x), fill=color)
            # canvas.create_line(xc-y-1, yc-x-1, (xc-y), (yc-x), fill=color)

    @classmethod
    def circunferencia(cls, xc, yc, r, canvas, zbuffer,colorbuffer, color='#ff00ff'):
        
        x = 0
        y = r
        d = 1-r
        CG.draw_circle(xc, yc, x, y, canvas, zbuffer,r,colorbuffer,color)
        CG.draw_circle(xc, yc, x+1, y, canvas, zbuffer,r,colorbuffer,color)
        
        while x < y:
            if d < 0:
                d = d+2*x+3
                x +=1
            else:
                d = d+2*(x-y)+5
                x+=1
                y-=1
            CG.draw_circle(xc, yc, x, y, canvas, zbuffer,r,colorbuffer,color)
            CG.draw_circle(xc, yc, x+1, y, canvas, zbuffer,r,colorbuffer,color)            

    @classmethod
    def scale_3D(cls, type='local'):
        pass

    @staticmethod
    def call_projecao(self, canvas):
        if self.projecao == 'cav':
            self.cavaleira(canvas)
        elif self.projecao == 'ort':
            self.ortogonal(canvas, self.plano, self.center_x, self.center_y)
        else:
            self.cabinet(canvas)

    def translacao_3D(self, eixo, deslocamento, canvas, projetar):
        if eixo == 'x':
            self.A[0] = self.A[0] + deslocamento
            self.B[0] = self.B[0] + deslocamento
            self.C[0] = self.C[0] + deslocamento
            self.D[0] = self.D[0] + deslocamento
            self.E[0] = self.E[0] + deslocamento
            self.F[0] = self.F[0] + deslocamento
            self.G[0] = self.G[0] + deslocamento
            self.H[0] = self.H[0] + deslocamento
            self.I[0] = self.I[0] + deslocamento
            self.J[0] = self.J[0] + deslocamento
        elif eixo == 'y':
            self.A[1] = self.A[1] + deslocamento
            self.B[1] = self.B[1] + deslocamento
            self.C[1] = self.C[1] + deslocamento
            self.D[1] = self.D[1] + deslocamento
            self.E[1] = self.E[1] + deslocamento
            self.F[1] = self.F[1] + deslocamento
            self.G[1] = self.G[1] + deslocamento
            self.H[1] = self.H[1] + deslocamento
            self.I[1] = self.I[1] + deslocamento
            self.J[1] = self.J[1] + deslocamento
        else:
            self.A[2] = self.A[2] + deslocamento
            self.B[2] = self.B[2] + deslocamento
            self.C[2] = self.C[2] + deslocamento
            self.D[2] = self.D[2] + deslocamento
            self.E[2] = self.E[2] + deslocamento
            self.F[2] = self.F[2] + deslocamento
            self.G[2] = self.G[2] + deslocamento
            self.H[2] = self.H[2] + deslocamento
            self.I[2] = self.I[2] + deslocamento
            self.J[2] = self.J[2] + deslocamento
        if projetar :
            CG.call_projecao(self,canvas)

    def escala_3D(self, eixo, fator, canvas):
        if eixo == 'x':
            self.A[0] = self.A[0] * fator
            self.B[0] = self.B[0] * fator
            self.C[0] = self.C[0] * fator
            self.D[0] = self.D[0] * fator
            self.E[0] = self.E[0] * fator
            self.F[0] = self.F[0] * fator
            self.G[0] = self.G[0] * fator
            self.H[0] = self.H[0] * fator
            self.I[0] = self.I[0] * fator
            self.J[0] = self.J[0] * fator
        elif eixo == 'y':
            self.A[1] = self.A[1] * fator
            self.B[1] = self.B[1] * fator
            self.C[1] = self.C[1] * fator
            self.D[1] = self.D[1] * fator
            self.E[1] = self.E[1] * fator
            self.F[1] = self.F[1] * fator
            self.G[1] = self.G[1] * fator
            self.H[1] = self.H[1] * fator
            self.I[1] = self.I[1] * fator
            self.J[1] = self.J[1] * fator
        else:
            self.A[2] = self.A[2] * fator
            self.B[2] = self.B[2] * fator
            self.C[2] = self.C[2] * fator
            self.D[2] = self.D[2] * fator
            self.E[2] = self.E[2] * fator
            self.F[2] = self.F[2] * fator
            self.G[2] = self.G[2] * fator
            self.H[2] = self.H[2] * fator
            self.I[2] = self.I[2] * fator
            self.J[2] = self.J[2] * fator
        
        CG.call_projecao(self, canvas)

    def escala_3D_global(self, canvas, factor):
        factor = float(factor)
        Ms = np.array([[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, factor]])
        array_factor = np.array([factor, factor, factor, factor])

        self.A = np.dot(np.array(self.A), Ms)
        self.B = np.dot(np.array(self.B), Ms)
        self.C = np.dot(np.array(self.C), Ms)
        self.D = np.dot(np.array(self.D), Ms)
        self.E = np.dot(np.array(self.E), Ms)
        self.F = np.dot(np.array(self.F), Ms)
        self.G = np.dot(np.array(self.G), Ms)
        self.H = np.dot(np.array(self.H), Ms)
        self.I = np.dot(np.array(self.I), Ms)
        self.J = np.dot(np.array(self.J), Ms)
        self.A = np.divide(self.A,array_factor)
        self.B = np.divide(self.B,array_factor)
        self.C = np.divide(self.C,array_factor)
        self.D = np.divide(self.D,array_factor)
        self.E = np.divide(self.E,array_factor)
        self.F = np.divide(self.F,array_factor)
        self.G = np.divide(self.G,array_factor)
        self.H = np.divide(self.H,array_factor)
        self.I = np.divide(self.I,array_factor)
        self.J = np.divide(self.J,array_factor)

        # print(self.A2)
        # print(self.B2)
        # print(self.C2)
        # print(self.D2)
        # print(self.E2)
        # print(self.F2)
        # print(self.G2)
        # print(self.H2)
        # print(self.I2)
        # print(self.J2)


        CG.call_projecao(self, canvas)

    def rotacao_3D(self, canvas, plano, graus):
        x_medio = (self.A[0]+self.B[0]+self.C[0]+self.D[0]+self.E[0]+self.F[0]+self.G[0]+self.H[0]+self.I[0]+self.J[0])/10 
        y_medio = (self.A[1]+self.B[1]+self.C[1]+self.D[1]+self.E[1]+self.F[1]+self.G[1]+self.H[1]+self.I[1]+self.J[1])/10 
        z_medio = (self.A[2]+self.B[2]+self.C[2]+self.D[2]+self.E[2]+self.F[2]+self.G[2]+self.H[2]+self.I[2]+self.J[2])/10 
        
        self.translacao_3D('x', -x_medio, canvas, False)
        self.translacao_3D('y', -y_medio, canvas, False)
        self.translacao_3D('z', -z_medio, canvas, False)

        if plano == 'z':
            Mc = np.array([[math.cos(math.radians(graus)), -math.sin(math.radians(graus)), 0, 0],
                           [math.sin(math.radians(graus)), math.cos(math.radians(graus)), 0, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]])
            print("rotação em z")
        elif plano == 'y':
            Mc = np.array([[math.cos(math.radians(graus)), 0, -math.sin(math.radians(graus)), 0],
                           [0, 1, 0, 0],
                           [math.sin(math.radians(graus)), 0, math.cos(math.radians(graus)), 0],
                           [0, 0, 0, 1]])
            print("rotação em y")
        else:
            Mc = np.array([[1, 0, 0, 0],
                           [0, math.cos(math.radians(graus)), -math.sin(math.radians(graus)), 0],
                           [0, math.sin(math.radians(graus)), math.cos(math.radians(graus)), 0],
                           [0, 0, 0, 1]])
            print("rotação em x")

        self.A = np.dot(np.array(self.A), Mc)
        self.B = np.dot(np.array(self.B), Mc)
        self.C = np.dot(np.array(self.C), Mc)
        self.D = np.dot(np.array(self.D), Mc)
        self.E = np.dot(np.array(self.E), Mc)
        self.F = np.dot(np.array(self.F), Mc)
        self.G = np.dot(np.array(self.G), Mc)
        self.H = np.dot(np.array(self.H), Mc)
        self.I = np.dot(np.array(self.I), Mc)
        self.J = np.dot(np.array(self.J), Mc)

        self.translacao_3D('x', x_medio, canvas, False)
        self.translacao_3D('y', y_medio, canvas, False)
        self.translacao_3D('z', z_medio, canvas, False)

        CG.call_projecao(self, canvas)

    def rotacao_3D_global(self, canvas, plano, graus):
        if plano == 'z':
            Mc = np.array([[math.cos(math.radians(graus)), -math.sin(math.radians(graus)), 0, 0],
                           [math.sin(math.radians(graus)), math.cos(math.radians(graus)), 0, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]])
            print("rotação em z")
        elif plano == 'y':
            Mc = np.array([[math.cos(math.radians(graus)), 0, -math.sin(math.radians(graus)), 0],
                           [0, 1, 0, 0],
                           [math.sin(math.radians(graus)), 0, math.cos(math.radians(graus)), 0],
                           [0, 0, 0, 1]])
            print("rotação em y")
        else:
            Mc = np.array([[1, 0, 0, 0],
                           [0, math.cos(math.radians(graus)), -math.sin(math.radians(graus)), 0],
                           [0, math.sin(math.radians(graus)), math.cos(math.radians(graus)), 0],
                           [0, 0, 0, 1]])
            print("rotação em x")

        self.A = np.dot(np.array(self.A), Mc)
        self.B = np.dot(np.array(self.B), Mc)
        self.C = np.dot(np.array(self.C), Mc)
        self.D = np.dot(np.array(self.D), Mc)
        self.E = np.dot(np.array(self.E), Mc)
        self.F = np.dot(np.array(self.F), Mc)
        self.G = np.dot(np.array(self.G), Mc)
        self.H = np.dot(np.array(self.H), Mc)
        self.I = np.dot(np.array(self.I), Mc)
        self.J = np.dot(np.array(self.J), Mc)

        CG.call_projecao(self, canvas)


    def cavaleira(self, canvas):
        self.projecao = 'cav'
        Mc = np.array([[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [((2)**(1/2))/2, ((2)**(1/2))/2, 0, 0],
                       [0, 0, 0, 1]])
        coord1 = 0
        coord2 = 1
        
        self.translacao_3D('x', self.center_x, canvas, False)
        self.translacao_3D('y', self.center_y, canvas, False)
        

        self.A2 = np.dot(np.array(self.A), Mc)
        self.B2 = np.dot(np.array(self.B), Mc)
        self.C2 = np.dot(np.array(self.C), Mc)
        self.D2 = np.dot(np.array(self.D), Mc)
        self.E2 = np.dot(np.array(self.E), Mc)
        self.F2 = np.dot(np.array(self.F), Mc)
        self.G2 = np.dot(np.array(self.G), Mc)
        self.H2 = np.dot(np.array(self.H), Mc)
        self.I2 = np.dot(np.array(self.I), Mc)
        self.J2 = np.dot(np.array(self.J), Mc)

        
        

        canvas.create_line(int(self.A2[coord1]), int(self.center_y*2-self.A2[coord2]), int(
            self.B2[coord1]), int(self.center_y*2-self.B2[coord2]), fill='black')
        canvas.create_line(int(self.A2[coord1]), int(self.center_y*2-self.A2[coord2]), int(
            self.E2[coord1]), int(self.center_y*2-self.E2[coord2]), fill='black')
        canvas.create_line(int(self.A2[coord1]), int(self.center_y*2-self.A2[coord2]), int(
            self.F2[coord1]), int(self.center_y*2-self.F2[coord2]), fill='black')
        canvas.create_line(int(self.B2[coord1]), int(self.center_y*2-self.B2[coord2]), int(
            self.C2[coord1]), int(self.center_y*2-self.C2[coord2]), fill='black')
        canvas.create_line(int(self.B2[coord1]), int(self.center_y*2-self.B2[coord2]), int(
            self.D2[coord1]), int(self.center_y*2-self.D2[coord2]), fill='black')
        canvas.create_line(int(self.B2[coord1]), int(self.center_y*2-self.B2[coord2]), int(
            self.G2[coord1]), int(self.center_y*2-self.G2[coord2]), fill='black')
        canvas.create_line(int(self.C2[coord1]), int(self.center_y*2-self.C2[coord2]), int(
            self.D2[coord1]), int(self.center_y*2-self.D2[coord2]), fill='black')
        canvas.create_line(int(self.C2[coord1]), int(self.center_y*2-self.C2[coord2]), int(
            self.H2[coord1]), int(self.center_y*2-self.H2[coord2]), fill='black')
        canvas.create_line(int(self.D2[coord1]), int(self.center_y*2-self.D2[coord2]), int(
            self.E2[coord1]), int(self.center_y*2-self.E2[coord2]), fill='black')
        canvas.create_line(int(self.D2[coord1]), int(self.center_y*2-self.D2[coord2]), int(
            self.I2[coord1]), int(self.center_y*2-self.I2[coord2]), fill='black')
        canvas.create_line(int(self.E2[coord1]), int(self.center_y*2-self.E2[coord2]), int(
            self.J2[coord1]), int(self.center_y*2-self.J2[coord2]), fill='black')
        canvas.create_line(int(self.F2[coord1]), int(self.center_y*2-self.F2[coord2]), int(
            self.G2[coord1]), int(self.center_y*2-self.G2[coord2]), fill='black')
        canvas.create_line(int(self.F2[coord1]), int(self.center_y*2-self.F2[coord2]), int(
            self.J2[coord1]), int(self.center_y*2-self.J2[coord2]), fill='black')
        canvas.create_line(int(self.G2[coord1]), int(self.center_y*2-self.G2[coord2]), int(
            self.H2[coord1]), int(self.center_y*2-self.H2[coord2]), fill='black')
        canvas.create_line(int(self.G2[coord1]), int(self.center_y*2-self.G2[coord2]), int(
            self.I2[coord1]), int(self.center_y*2-self.I2[coord2]), fill='black')
        canvas.create_line(int(self.H2[coord1]), int(self.center_y*2-self.H2[coord2]), int(
            self.I2[coord1]), int(self.center_y*2-self.I2[coord2]), fill='black')
        canvas.create_line(int(self.I2[coord1]), int(self.center_y*2-self.I2[coord2]), int(
            self.J2[coord1]), int(self.center_y*2-self.J2[coord2]), fill='black')


        self.translacao_3D('x', -self.center_x, canvas, False)
        self.translacao_3D('y', -self.center_y, canvas, False)

    def ortogonal(self, canvas, plano, center_x, center_y):
        self.plano = plano
        self.projecao = 'ort'
        if plano == 'z':
            Mc = np.array([[1, 0, 0, 0],
                           [0, 1, 0, 0],
                           [0, 0, 0, 0],
                           [0, 0, 0, 1]])
            coord1 = 0
            coord2 = 1
            print("z")
            self.translacao_3D('x', self.center_x, canvas, False)
            self.translacao_3D('y', self.center_y, canvas, False)

        elif plano == 'y':
            Mc = np.array([[1, 0, 0, 0],
                           [0, 0, 0, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]])
            coord1 = 0
            coord2 = 2
            print("y")
            self.translacao_3D('x', self.center_x, canvas, False)
            self.translacao_3D('z', self.center_y, canvas, False)
        else:
            Mc = np.array([[0, 0, 0, 0],
                           [0, 1, 0, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]])
            coord1 = 1
            coord2 = 2
            print("x")
            self.translacao_3D('y', self.center_x, canvas, False)
            self.translacao_3D('z', self.center_y, canvas, False)

        self.A2 = np.dot(np.array(self.A), Mc)
        self.B2 = np.dot(np.array(self.B), Mc)
        self.C2 = np.dot(np.array(self.C), Mc)
        self.D2 = np.dot(np.array(self.D), Mc)
        self.E2 = np.dot(np.array(self.E), Mc)
        self.F2 = np.dot(np.array(self.F), Mc)
        self.G2 = np.dot(np.array(self.G), Mc)
        self.H2 = np.dot(np.array(self.H), Mc)
        self.I2 = np.dot(np.array(self.I), Mc)
        self.J2 = np.dot(np.array(self.J), Mc)
        
        if plano == 'z':
            self.translacao_3D('x', -self.center_x, canvas, False)
            self.translacao_3D('y', -self.center_y, canvas, False)
        
        elif plano == 'x':
            self.translacao_3D('y', -self.center_x, canvas, False)
            self.translacao_3D('z', -self.center_y, canvas, False)
        
        elif plano == 'y':
            self.translacao_3D('x', -self.center_x, canvas, False)
            self.translacao_3D('z', -self.center_y, canvas, False)

        print(f'x1={self.A2[coord1]}y1={self.A2[coord2]}x2={self.B2[coord1]}y2{self.B2[coord2]}')

        canvas.create_line(int(self.A2[coord1]), int(self.center_y*2 - self.A2[coord2]), int(
            self.B2[coord1]), int(self.center_y*2 - self.B2[coord2]), fill='black')
        canvas.create_line(int(self.A2[coord1]), int(self.center_y*2 - self.A2[coord2]), int(
            self.E2[coord1]), int(self.center_y*2 - self.E2[coord2]), fill='black')
        canvas.create_line(int(self.A2[coord1]), int(self.center_y*2 - self.A2[coord2]), int(
            self.F2[coord1]), int(self.center_y*2 - self.F2[coord2]), fill='black')
        canvas.create_line(int(self.B2[coord1]), int(self.center_y*2 - self.B2[coord2]), int(
            self.C2[coord1]), int(self.center_y*2 - self.C2[coord2]), fill='black')
        canvas.create_line(int(self.B2[coord1]), int(self.center_y*2 - self.B2[coord2]), int(
            self.D2[coord1]), int(self.center_y*2 - self.D2[coord2]), fill='black')
        canvas.create_line(int(self.B2[coord1]), int(self.center_y*2 - self.B2[coord2]), int(
            self.G2[coord1]), int(self.center_y*2 - self.G2[coord2]), fill='black')
        canvas.create_line(int(self.C2[coord1]), int(self.center_y*2 - self.C2[coord2]), int(
            self.D2[coord1]), int(self.center_y*2 - self.D2[coord2]), fill='black')
        canvas.create_line(int(self.C2[coord1]), int(self.center_y*2 - self.C2[coord2]), int(
            self.H2[coord1]), int(self.center_y*2 - self.H2[coord2]), fill='black')
        canvas.create_line(int(self.D2[coord1]), int(self.center_y*2 - self.D2[coord2]), int(
            self.E2[coord1]), int(self.center_y*2 - self.E2[coord2]), fill='black')
        canvas.create_line(int(self.D2[coord1]), int(self.center_y*2 - self.D2[coord2]), int(
            self.I2[coord1]), int(self.center_y*2 - self.I2[coord2]), fill='black')
        canvas.create_line(int(self.E2[coord1]), int(self.center_y*2 - self.E2[coord2]), int(
            self.J2[coord1]), int(self.center_y*2 - self.J2[coord2]), fill='black')
        canvas.create_line(int(self.F2[coord1]), int(self.center_y*2 - self.F2[coord2]), int(
            self.G2[coord1]), int(self.center_y*2 - self.G2[coord2]), fill='black')
        canvas.create_line(int(self.F2[coord1]), int(self.center_y*2 - self.F2[coord2]), int(
            self.J2[coord1]), int(self.center_y*2 - self.J2[coord2]), fill='black')
        canvas.create_line(int(self.G2[coord1]), int(self.center_y*2 - self.G2[coord2]), int(
            self.H2[coord1]), int(self.center_y*2 - self.H2[coord2]), fill='black')
        canvas.create_line(int(self.G2[coord1]), int(self.center_y*2 - self.G2[coord2]), int(
            self.I2[coord1]), int(self.center_y*2 - self.I2[coord2]), fill='black')
        canvas.create_line(int(self.H2[coord1]), int(self.center_y*2 - self.H2[coord2]), int(
            self.I2[coord1]), int(self.center_y*2 - self.I2[coord2]), fill='black')
        canvas.create_line(int(self.I2[coord1]), int(self.center_y*2 - self.I2[coord2]), int(
            self.J2[coord1]), int(self.center_y*2 - self.J2[coord2]), fill='black')


    def cabinet(self, canvas):
        self.projecao = 'cab'
        Mc = np.array([[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [(math.cos(math.radians(63.4)))/2, (math.sin(math.radians(63.4)))/2, 0, 0],
                       [0, 0, 0, 1]])
        coord1 = 0
        coord2 = 1
        
        self.translacao_3D('x', self.center_x, canvas, False)
        self.translacao_3D('y', self.center_y, canvas, False)
        
        self.A2 = np.dot(np.array(self.A), Mc)
        self.B2 = np.dot(np.array(self.B), Mc)
        self.C2 = np.dot(np.array(self.C), Mc)
        self.D2 = np.dot(np.array(self.D), Mc)
        self.E2 = np.dot(np.array(self.E), Mc)
        self.F2 = np.dot(np.array(self.F), Mc)
        self.G2 = np.dot(np.array(self.G), Mc)
        self.H2 = np.dot(np.array(self.H), Mc)
        self.I2 = np.dot(np.array(self.I), Mc)
        self.J2 = np.dot(np.array(self.J), Mc)
        print(f'x1={self.A2[coord1]}y1={self.A2[coord2]}x2={self.B2[coord1]}y2{self.center_y*2 - self.B2[coord2]}')
        canvas.create_line(int(self.A2[coord1]), int(self.center_y*2 - self.A2[coord2]), int(
            self.B2[coord1]), int(self.center_y*2 - self.B2[coord2]), fill='black')
        canvas.create_line(int(self.A2[coord1]), int(self.center_y*2 - self.A2[coord2]), int(
            self.E2[coord1]), int(self.center_y*2 - self.E2[coord2]), fill='black')
        canvas.create_line(int(self.A2[coord1]), int(self.center_y*2 - self.A2[coord2]), int(
            self.F2[coord1]), int(self.center_y*2 - self.F2[coord2]), fill='black')
        canvas.create_line(int(self.B2[coord1]), int(self.center_y*2 - self.B2[coord2]), int(
            self.C2[coord1]), int(self.center_y*2 - self.C2[coord2]), fill='black')
        canvas.create_line(int(self.B2[coord1]), int(self.center_y*2 - self.B2[coord2]), int(
            self.D2[coord1]), int(self.center_y*2 - self.D2[coord2]), fill='black')
        canvas.create_line(int(self.B2[coord1]), int(self.center_y*2 - self.B2[coord2]), int(
            self.G2[coord1]), int(self.center_y*2 - self.G2[coord2]), fill='black')
        canvas.create_line(int(self.C2[coord1]), int(self.center_y*2 - self.C2[coord2]), int(
            self.D2[coord1]), int(self.center_y*2 - self.D2[coord2]), fill='black')
        canvas.create_line(int(self.C2[coord1]), int(self.center_y*2 - self.C2[coord2]), int(
            self.H2[coord1]), int(self.center_y*2 - self.H2[coord2]), fill='black')
        canvas.create_line(int(self.D2[coord1]), int(self.center_y*2 - self.D2[coord2]), int(
            self.E2[coord1]), int(self.center_y*2 - self.E2[coord2]), fill='black')
        canvas.create_line(int(self.D2[coord1]), int(self.center_y*2 - self.D2[coord2]), int(
            self.I2[coord1]), int(self.center_y*2 - self.I2[coord2]), fill='black')
        canvas.create_line(int(self.E2[coord1]), int(self.center_y*2 - self.E2[coord2]), int(
            self.J2[coord1]), int(self.center_y*2 - self.J2[coord2]), fill='black')
        canvas.create_line(int(self.F2[coord1]), int(self.center_y*2 - self.F2[coord2]), int(
            self.G2[coord1]), int(self.center_y*2 - self.G2[coord2]), fill='black')
        canvas.create_line(int(self.F2[coord1]), int(self.center_y*2 - self.F2[coord2]), int(
            self.J2[coord1]), int(self.center_y*2 - self.J2[coord2]), fill='black')
        canvas.create_line(int(self.G2[coord1]), int(self.center_y*2 - self.G2[coord2]), int(
            self.H2[coord1]), int(self.center_y*2 - self.H2[coord2]), fill='black')
        canvas.create_line(int(self.G2[coord1]), int(self.center_y*2 - self.G2[coord2]), int(
            self.I2[coord1]), int(self.center_y*2 - self.I2[coord2]), fill='black')
        canvas.create_line(int(self.H2[coord1]), int(self.center_y*2 - self.H2[coord2]), int(
            self.I2[coord1]), int(self.center_y*2 - self.I2[coord2]), fill='black')
        canvas.create_line(int(self.I2[coord1]), int(self.center_y*2 - self.I2[coord2]), int(
            self.J2[coord1]), int(self.center_y*2 - self.J2[coord2]), fill='black')
        
        self.translacao_3D('x', -self.center_x, canvas, False)
        self.translacao_3D('y', -self.center_y, canvas, False)

    def shearing_3D(self, canvas, shx=0, shy=0, shz=0):
        if shx == '':
            shx=0
        if shy == '':
            shy=0
        if shz=='':
            shz=0
        try:
            Msh = np.array([[1, float(shx), float(shx), 0],
                        [float(shy), 1, float(shy), 0],
                        [float(shz), float(shy), 1, 0],
                        [  0,   0, 0, 1]])
        except ValueError:
            messagebox.showerror('Erro', 'Ao menos um eixo deve aplicar o cisalhamento no eixo selecionado!')
        
        self.A = np.dot(np.array(self.A), Msh)
        self.B = np.dot(np.array(self.B), Msh)
        self.C = np.dot(np.array(self.C), Msh)
        self.D = np.dot(np.array(self.D), Msh)
        self.E = np.dot(np.array(self.E), Msh)
        self.F = np.dot(np.array(self.F), Msh)
        self.G = np.dot(np.array(self.G), Msh)
        self.H = np.dot(np.array(self.H), Msh)
        self.I = np.dot(np.array(self.I), Msh)
        self.J = np.dot(np.array(self.J), Msh)

        CG.call_projecao(self, canvas)


def main():
    root = Tk()
    root.title('Casinha')
    canvas = Canvas(root, width=2000, height=2000, background='#ffffff')
    canvas.grid(row=0, column=0)
    a = CG()
    #a.cavaleira(canvas)
    #a.translacao_3D('x', 300, canvas, True)
    #a.cabinet(canvas)
    #a.translacao_3D('y', 300, canvas, True)
    #a.ortogonal(canvas, 'y')
    #a.translacao_3D('x', 200, canvas, True)
    # a.ortogonal(canvas, 'z')
    # a.translacao_3D('x', 500, canvas, False)
    #a.escala_3D('x', 2, canvas)
    # a.rotacao_3D(canvas, 'y', 90)
    print(f'called')
    # a.rotacao_3D_global(canvas, 100)
    # a.escala_3D_global(canvas, 0.10)
    root.mainloop()


# main()
