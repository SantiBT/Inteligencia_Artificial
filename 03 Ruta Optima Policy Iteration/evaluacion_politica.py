#!/ usr/bin/python -tt
# -*- coding: utf-8 -*-
# Ronny Conde at Monkey from the Future

import copy
import laberinto as lab

def actualizar_valor_estado(estado, politica, valores_estados, gamma):
    """ Devuelve el valor del estado tras aplicar un paso de Policy Evaluation.
    Se utilizara politica para saber la accion a seleccionar y valores_estados
    para saber el valor de los estados destino. El parametro gamma es el factor
    de descuento.
    E.g. actualizar_valor_estado((0, 0), politica, valores_estados, 0.9) puede
    devolver 0.06574
    """
    accion = politica[estado]
    valor = 0.0
    for (estado_, prob) in lab.posibles_transiciones(estado, accion):
        if estado_ != None:
            valor += prob * (lab.recompensa(estado, accion) + gamma * valores_estados[estado_])
        else:
            valor += prob * lab.recompensa(estado, accion)
    return valor

def paso(politica, valores_estados, gamma):
    """ Devuelve la version actualizada de valores_estados tras ejecutar un paso
    de Policy Evaluation. El parametro gamma es el factor de descuento.
    """
    valores_estados_ = copy.copy(valores_estados)
    for s in lab.posibles_estados():
        valores_estados_[s] = actualizar_valor_estado(s, politica, valores_estados, gamma)
    return valores_estados_

def evaluacion(politica, gamma):
    """ Devuelve la evaluacion de politica (100 iteraciones de la funcion paso). """
    N = 100
    valores_estados = {s: 0.0 for s in lab.posibles_estados()}
    for _ in range(100):
        valores_estados = paso(politica, valores_estados, gamma)
    
    return valores_estados
