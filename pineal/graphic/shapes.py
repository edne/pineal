from math import pi, sin, cos
from pyglet.graphics import vertex_list


def wired_polygon(n: int):
    'Make the pyglet.vertex_list for a wireframe polygon.'
    def vertex(n, i):
        theta = i * 2*pi / n
        return cos(theta), sin(theta)

    vertexes = [vertex(n, i)
                for i in range(n)]
    vertexes = [coord
                for v in vertexes
                for coord in v]

    return vertex_list(n,
                       ('v2f/static', vertexes),
                       ('c4f/stream', [1] * 4*n))


def solid_polygon(n: int):
    'Make the pyglet.vertex_list for a solid color polygon'
    def vertex(i, n):
        dtheta = 2*pi / n
        theta0 = i * dtheta
        theta1 = theta0 + dtheta
        return [0, 0,
                cos(theta0), sin(theta0),
                cos(theta1), sin(theta1)]

    vertexes = [vertex(i, n)
                for i in range(n)]
    vertexes = [coord
                for v in vertexes
                for coord in v]

    return vertex_list(n*3,
                       ('v2f/static', vertexes),
                       ('c4f/stream', [1] * 4 * 3*n))
