#!/ usr/bin/python -tt
# -*- coding: utf-8 -*-
# Ronny Conde at Monkey from the Future
# Edited by Santos Bringas Tejero

import laberinto as lab
from evaluacion_politica import evaluacion 
from operator import itemgetter

def clave_mayor_valor(diccionario):
    """ Dado un diccionario, devuelve la clave con el mayor valor asociado.
    E.g. clave_mayor_valor({'a': 1.0, 'b': 2.0, 'c': 1.5}) devolvera 'b'
    """
    return max(diccionario.iteritems(), key=itemgetter(1))[0]

def valor_estado_accion(valores_estados, estado, accion):
    """ Dada la evaluacion de una politica (valores_estados), devolvera la suma
    de las recompensas esperadas (hasta finalizar el episodio) tras seleccionar
    accion desde estado si, a partir de ese momento, el agente siguiera la
    politica evaluada y teniendo en cuenta el factor de descuento gamma.
    
    Se calculara como la suma de la recompensa por abandonar estado y la media
    ponderada de los valores de cada posible estado destino teniendo en cuenta
    la probabilidad de acabar en dicho estado.
    
    E.g. valor_estado_accion(valores_estados, (0, 0), 'E') devolvera un flotante
    que sera calculado como lab.recompensa((0, 0), 'E') + 0.8 *
    valores_estados[(0, 1)] + 0.1 * valores_estados[(1, 0)] + 0.1 *
    valores_estados[(0, 0)].
    """
    val = lab.recompensa(estado, accion)
    for (est, prob) in lab.posibles_transiciones(estado, accion):
        val += prob * valores_estados[est]
        
    return val

def extraccion_accion(valores_estados, estado):
    """ Dada la evaluacion de una politica (valores_estados), devolvera la
    accion optima desde estado teniendo en cuenta que a partir de ese momento el
    agente seguira la politica evaluada. En caso de que estado sea terminal
    siempre devolvera 'EXIT'.

    E.g. extraccion_accion(valores_estados, (0, 0)) puede devolver 'E';
    extraccion_accion(valores_estados, (1, 3)) devolvera 'EXIT'
    """
    mejor_accion = None
    mejor_val = -float("inf")
    if lab.es_terminal(estado):
        mejor_accion =  'EXIT'
    else:
        for accion in lab.acciones_disponibles(estado):
            sig_estado = lab.siguiente_estado(estado, accion)
            if valores_estados[sig_estado] > mejor_val:
                mejor_accion = accion
                mejor_val = valores_estados[sig_estado]

    return mejor_accion

def extraccion_politica(valores_estados):
    """ Dada la evaluacion de una politica (valores_estados), devolvera un
    diccionario que almacenara la accion optima asociada a cada estado asumiendo
    que tras seleccionar dicha accion el agente va a seguir la politica
    evaluada. Cuando un estado sea terminal la accion asociada sera siempre
    'EXIT'.

    E.g. extraccion_politica(valores_estados) puede devolver {(0, 1): 'E', (1,
    2): 'N', (0, 0): 'E', (2, 1): 'E', (2, 0): 'N', (1, 3): 'EXIT', (2, 3): 'W',
    (2, 2): 'N', (1, 0): 'N', (0, 3): 'EXIT', (0, 2): 'E'}
    """
    politica = dict()
    for estado in valores_estados:
        politica[estado] = extraccion_accion(valores_estados, estado)

    return politica

def main():
    gamma = 0.9
    politica = {s: 'N' if s != (0, 3) and s != (1, 3) else 'EXIT' for s in lab.posibles_estados()}
   
    N = 4
    # Bucle para iterar la politica (evaluar y extraer) N veces.  E.g. a
    # partir de la segunda iteracion el resultado tiene que ser: {(0, 1): 'E',
    # (1, 2): 'N', (0, 0): 'E', (2, 1): 'W', (2, 0): 'N', (1, 3): 'EXIT', (2,
    # 3): 'W', (2, 2): 'N', (1, 0): 'N', (0, 3): 'EXIT', (0, 2): 'E'}
    valores_estados = evaluacion(politica, gamma)
    for i in range(N):
        politica = extraccion_politica(valores_estados)
        valores_estados = evaluacion(politica, gamma)

    # Imprime la politica resultante
    print politica
    
if __name__ == "__main__":
  main()
