# Audio backend used by pyo
# http://ajaxsoundstudio.com/pyodoc/api/classes/server.html
BACKEND = 'portaudio'  #  multiplatform
#BACKEND = 'jack'       # Linux and Mac, if you know what you are doing
#BACKEND = 'coreaudio'  # Mac only, untested


# OSC adresses
OSC_EYE = ('localhost', 1420)
OSC_EAR = ('localhost', 1422)


# Size of the rendering window
RENDER_SIZE = (800, 800)
