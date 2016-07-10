#!/ usr/bin/python -tt
# -*- coding: utf-8 -*-
# Ronny Conde at Monkey from the Future

def posibles_desplazamientos(accion):
    """ Devuelve una lista de tuplas con los posibles desplazamientos y su
    probabilidad tras seleccionar accion (En esta funcion no puede ser 'EXIT'). 
    
    E.g. posibles_desplazamientos('W') devolvera [('W', 0.8), ('N', 0.1), ('S',
    0.1)]
    """
    rueda = ['W', 'N', 'E', 'S'] #Sentido agujas del reloj.
    indice_principal = rueda.index(accion) #Indice desplazamiento principal.
    desplazamientos = [(accion, 0.8)] #Inicializamos desplazamientos.
    for offset in [-1, +1]: #Desviaciones del desplazamiento principal.
        if indice_principal + offset == len(rueda):
            desp_ = rueda[0] #Siguiente desplaz con desv.
        else:
            desp_ = rueda[indice_principal + offset] #Siguiente desplaz con desv.
        desplazamientos.append((desp_, 0.1))
    return desplazamientos

def siguiente_estado(estado, desplazamiento):
    """ Devuelve la celda en la que acabara el agente tras el desplazamiento
    desde estado. Los desplazamientos son deterministas. La componente
    estocastica se tuvo en cuenta en la funcion
    posibles_desplazamientos(accion). Hay que tener en cuenta el comportamiento
    ante los obstaculos y limites del laberinto.
    
    E.g. siguiente_estado((0, 1), 'E') devolvera (0, 2)
    """
    tabla_desp = {'W': (0, -1), 'N': (-1, 0), 'E': (0, 1), 'S': (1, 0)}
    (fil, col) = estado
    fil_ = fil + tabla_desp[desplazamiento][0]
    col_ = col + tabla_desp[desplazamiento][1]
    if (col_ > 3 or fil_ > 2 or col_ < 0 or fil_ < 0 or (fil_, col_) == (1, 1)):
        return estado
    else:
        return (fil_, col_)

def posibles_transiciones(estado, accion):
    """ Devuelve una lista de tuplas con los posibles estados tras seleccionar
    accion desde estado y sus probabilidades correspondientes. Si la accion es
    'EXIT' devolvera [(None, 1.0)].
    
    E.g. posibles_transiciones((0,0), 'W') devolvera [((0,0), 0.9), ((1,0),
    0.1)]
    """
    if accion == 'EXIT':
        return [(None, 1.0)]
    else:    
        transiciones = []
        for (desp, prob) in posibles_desplazamientos(accion):
            estado_ = siguiente_estado(estado, desp)
            indice_coincidencia = None
            for i in range(len(transiciones)):
                (s, p) = transiciones[i]
                if estado_ == s: indice_coincidencia = i
            if indice_coincidencia != None:
                transiciones[indice_coincidencia] = (transiciones[indice_coincidencia][0],
                                                    transiciones[indice_coincidencia][1] + prob)
            else:
                transiciones.append((estado_, prob))
        return transiciones

def recompensa(estado, accion):
    """ Devuelve la recompensa que se recibira al abandonar estado tras
    seleccionar accion.
    
    E.g. recompensa((0,0), 'E') devolvera 0.0; recompensa((0,3), 'EXIT')
    devolvera 1.0
    """
    if accion == 'EXIT' and estado == (0, 3):
        return 1.0
    elif accion == 'EXIT' and estado == (1, 3):
        return -1.0
    else:
        return 0.0

def acciones_disponibles(estado):
    """ Devuelve una lista con las posibles acciones que el agente puede
    seleccionar desde estado.
    
    E.g. acciones_disponibles((0,0)) devolvera ['W', 'N', 'E', 'S'];
    acciones_disponibles((1,3)) devolvera ['EXIT']
    """
    if estado == (0, 3) or estado == (1, 3):
        return ['EXIT']
    else:
        return ['W', 'N', 'E', 'S']
