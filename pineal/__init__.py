from sys import argv
from pineal.parser import parse
import pineal.config


def main():
    pineal.config.__dict__.update(parse())

    MODULES = ['Core', 'Audio', 'Gui']
    m = [p for p in MODULES if '--'+p.lower() in argv][0]

    try:
        __import__(m.lower(), globals(), locals(), [m], -1).__dict__[m]().run()
    except KeyboardInterrupt:
        pass
