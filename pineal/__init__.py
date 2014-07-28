from visuals import Visuals
from graphic import Graphic
from loader import Loader
from analyzer import Analyzer
from gui import Gui

analyzer = None  # used only by pineal.livecoding.audio


def main():
    visuals = Visuals()
    graphic = Graphic(visuals)
    loader = Loader(visuals)
    global analyzer
    analyzer = Analyzer(visuals)
    gui = Gui(visuals)

    loader.start()
    analyzer.start()

    try:
        while True:
            gui.update()
            graphic.update()
    except KeyboardInterrupt:
        None

    loader.stop()
    analyzer.stop()
