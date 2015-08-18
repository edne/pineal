from ctypes import byref
import pyglet.gl as gl
from pyglet.image import Texture


def buffer_texture(width, height):
    _id = gl.GLuint()
    gl.glGenTextures(1, byref(_id))

    gl.glPushAttrib(gl.GL_ENABLE_BIT | gl.GL_TEXTURE_BIT)
    gl.glActiveTexture(gl.GL_TEXTURE0)
    gl.glEnable(gl.GL_TEXTURE_2D)

    gl.glBindTexture(gl.GL_TEXTURE_2D, _id)

    gl.glTexParameteri(gl.GL_TEXTURE_2D,
                       gl.GL_TEXTURE_MIN_FILTER,
                       gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D,
                       gl.GL_TEXTURE_MAG_FILTER,
                       gl.GL_LINEAR)
    gl.glTexImage2D(
        gl.GL_TEXTURE_2D, 0, gl.GL_RGBA,
        width, height,
        0,
        gl.GL_RGBA, gl.GL_UNSIGNED_BYTE,
        (gl.GLubyte * (width*height * 4))(),
    )
    gl.glFlush()

    gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
    gl.glPopAttrib()

    return _id


class Framebuffer(object):
    def draw(self):
        pass

    def __init__(self, width, height):
        if not gl.gl_info.have_extension('GL_EXT_framebuffer_object'):
            raise Exception('framebuffer object extension not available')

        texture_id = buffer_texture(width, height)
        self.texture = Texture(width, height, gl.GL_TEXTURE_2D, texture_id)

        framebuffer_id = gl.GLuint()
        gl.glGenFramebuffersEXT(1, byref(framebuffer_id))
        self.id = framebuffer_id.value

        with self:
            gl.glFramebufferTexture2DEXT(gl.GL_FRAMEBUFFER_EXT,
                                         gl.GL_COLOR_ATTACHMENT0_EXT + 0,
                                         gl.GL_TEXTURE_2D,
                                         texture_id,
                                         0)

    def __enter__(self):
        gl.glBindFramebufferEXT(gl.GL_FRAMEBUFFER_EXT, gl.GLuint(self.id))

    def __exit__(self, *args, **kwargs):
        gl.glBindFramebufferEXT(gl.GL_FRAMEBUFFER_EXT, 0)
