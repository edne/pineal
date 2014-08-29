import pyglet.gl as gl


def _vec(*args):
    return (gl.GLfloat * len(args))(*args)


def ambient(amb):
    """ set ambiental light intensity """
    gl.glLightModelfv(
        gl.GL_LIGHT_MODEL_AMBIENT|gl.GL_LIGHT_MODEL_TWO_SIDE,
        _vec(amb,amb,amb, 1.0)
    )


def light(val):
    """ set light intensity """
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, _vec(val, val, val, 1.0))


def light_pos(x,y,z):
    """ set light position """
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, _vec(x,y,z, 3))
