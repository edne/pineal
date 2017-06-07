import pyglet
import pyglet.gl as gl


def new_renderer(draw, size):
    w, h = size
    window = pyglet.window.Window(caption='(pineal renderer)',
                                  width=w,
                                  height=h,
                                  visible=False)

    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    gl.glEnable(gl.GL_LINE_SMOOTH)
    gl.glEnable(gl.GL_POLYGON_SMOOTH)
    gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_NICEST)
    gl.glHint(gl.GL_POLYGON_SMOOTH_HINT, gl.GL_NICEST)

    window.texture = None

    @window.event
    def on_draw():
        pyglet.clock.tick()
        window.clear()

        gl.glLoadIdentity()
        draw()

        buf = pyglet.image.get_buffer_manager().get_color_buffer()
        rawimage = buf.get_image_data()
        window.texture = rawimage.get_texture()

    return window
