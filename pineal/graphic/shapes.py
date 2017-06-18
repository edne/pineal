from math import pi, sin, cos


def vertex(n, i):
    theta = i * 2*pi / n
    return cos(theta), sin(theta)


def face(n, i):
    return [(0, 0),
            vertex(n, i),
            vertex(n, i+1)]


def wired_polygon(n):
    'Make the pyglet.vertex_list for a wireframe polygon.'
    vertexes = [vertex(n, i)
                for i in range(n)]
    coords = [coord
              for v in vertexes
              for coord in v]

    return coords


def solid_polygon(n):
    'Make the pyglet.vertex_list for a solid color polygon.'
    faces = [face(n, i)
             for i in range(n)]
    coords = [coord
              for face in faces
              for point in face
              for coord in point]

    return coords
