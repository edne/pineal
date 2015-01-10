from lib.graphic import Polygon
import lib.audio as audio

amp = audio.source("AMP")
pol = Polygon(4)


def draw():
    pol.fill = [1,1,1, 0.5]
    pol.draw()
