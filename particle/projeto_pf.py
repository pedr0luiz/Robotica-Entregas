#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Esta classe deve conter todas as suas implementações relevantes para seu filtro de partículas
"""

from pf import Particle, create_particles, draw_random_sample
import numpy as np
import inspercles # necessário para o a função nb_lidar que simula o laser
import math
from scipy.stats import norm



largura = 775 # largura do mapa
altura = 748  # altura do mapa

# Robo
robot = Particle(largura/2, altura/2, math.pi/4, 1.0)

# Nuvem de particulas
particulas = []

num_particulas = 300


# Os angulos em que o robo simulado vai ter sensores
angles = np.linspace(0.0, 2*math.pi, num=8, endpoint=False)

# Lista mais longa
movimentos_longos = [[-10, -10, 0], [-10, 10, 0], [-10,0,0], [-10, 0, 0],
              [0,0,math.pi/12.0], [0, 0, math.pi/12.0], [0, 0, math.pi/12],[0,0,-math.pi/4],
              [-5, 0, 0],[-5,0,0], [-5,0,0], [-10,0,0],[-10,0,0], [-10,0,0],[-10,0,0],[-10,0,0],[-15,0,0],
              [0,0,-math.pi/4],[0, 10, 0], [0,10,0], [0, 10, 0], [0,10,0], [0,0,math.pi/8], [0,10,0], [0,10,0], 
              [0,10,0], [0,10,0], [0,10,0],[0,10,0],
              [0,0,-math.radians(90)],
              [math.cos(math.pi/3)*10, math.sin(math.pi/3),0],[math.cos(math.pi/3)*10, math.sin(math.pi/3),0],[math.cos(math.pi/3)*10, math.sin(math.pi/3),0],
              [math.cos(math.pi/3)*10, math.sin(math.pi/3),0]]

# Lista curta
movimentos_curtos = [[-10, -10, 0], [-10, 10, 0], [-10,0,0], [-10, 0, 0]]

movimentos_relativos = [[0, -math.pi/3],[10, 0],[10, 0], [10, 0], [10, 0],[15, 0],[15, 0],[15, 0],[0, -math.pi/2],[10, 0],
                       [10,0], [10, 0], [10, 0], [10, 0], [10, 0], [10, 0],
                       [10,0], [10, 0], [10, 0], [10, 0], [10, 0], [10, 0],
                       [10,0], [10, 0], [10, 0], [10, 0], [10, 0], [10, 0],
                       [0, -math.pi/2], 
                       [10,0], [10, 0], [10, 0], [10, 0], [10, 0], [10, 0],
                       [10,0], [10, 0], [10, 0], [10, 0], [10, 0], [10, 0],
                       [10,0], [10, 0], [10, 0], [10, 0], [10, 0], [10, 0],
                       [10,0], [10, 0], [10, 0], [10, 0], [10, 0], [10, 0],
                       [0, -math.pi/2], 
                       [10,0], [0, -math.pi/4], [10,0], [10,0], [10,0],
                       [10,0], [10, 0], [10, 0], [10, 0], [10, 0], [10, 0],
                       [10,0], [10, 0], [10, 0], [10, 0], [10, 0], [10, 0]]



movimentos = movimentos_relativos



def cria_particulas(minx=0, miny=0, maxx=largura, maxy=altura, n_particulas=num_particulas):
    """
        Cria uma lista de partículas distribuídas de forma uniforme entre minx, miny, maxx e maxy
    """

    particulas = []

    for i in range(num_particulas):
        x = np.random.uniform(minx, maxx)
        y = np.random.uniform(miny, maxy)
        theta = np.random.uniform(0, 2*math.pi)
        p = Particle(x, y, theta, w=1.0) 
        particulas.append(p)

    return particulas
    
def move_particulas(particulas, movimento):
    """
        Recebe um movimento na forma [deslocamento, theta]  e o aplica a todas as partículas
        Assumindo um desvio padrão para cada um dos valores
        Esta função não precisa devolver nada, e sim alterar as partículas recebidas.
        
        Sugestão: aplicar move_relative(movimento) a cada partícula
        
        Você não precisa mover o robô. O código fornecido pelos professores fará isso
        
    """

    for particula in particulas:
        movimento[0] = norm.rvs(movimento[0], 1)
        movimento[1] = norm.rvs(movimento[1], math.radians(1))
        particula.move_relative(movimento)

    
def leituras_laser_evidencias(robot, particulas):
    """
        Realiza leituras simuladas do laser para o robo e as particulas
        Depois incorpora a evidência calculando
        P(H|D) para todas as particulas
        Lembre-se de que a formula $P(z_t | x_t) = \alpha \prod_{j}^M{e^{\frac{-(z_j - \hat{z_j})}{2\sigma^2}}}$ 
        responde somente P(D|Hi), em que H é a hi
        
        Esta função não precisa retornar nada, mas as partículas precisa ter o seu w recalculado. 
        
        Você vai precisar calcular para o robo
        
    """
    
    leitura_robo = inspercles.nb_lidar(robot, angles)

    w_total = 0

    for i in range(len(particulas)):
        soma = 0
        leitura_real = inspercles.nb_lidar(particulas[i],angles)
        for j in range(len(angles)):
            soma += norm.pdf(leitura_robo[angles[j]], loc=leitura_real[angles[j]],scale=7)
        particulas[i].w = soma
        w_total += soma

    for i in range(len(particulas)):
        particulas[i].w /=w_total
    
    # Voce vai precisar calcular a leitura para cada particula usando inspercles.nb_lidar e depois atualizar as probabilidades

    
def reamostrar(particulas, n_particulas = num_particulas):
    """
        Reamostra as partículas devolvendo novas particulas sorteadas
        de acordo com a probabilidade e deslocadas de acordo com uma variação normal    
        
        O notebook como_sortear tem dicas que podem ser úteis
        
        Depois de reamostradas todas as partículas precisam novamente ser deixadas com probabilidade igual
        
        Use 1/n ou 1, não importa desde que seja a mesma
    """

    particulas_pesos = [p.w for p in particulas]

    novas_particulas = draw_random_sample(particulas, particulas_pesos, len(particulas))

    for p in novas_particulas:
        p.x += norm.rvs(0, 6)
        p.y += norm.rvs(0, 6)
        p.theta += norm.rvs(0, math.radians(10))
        p.w = 1

    return novas_particulas