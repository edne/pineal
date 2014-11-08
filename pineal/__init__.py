from sys import argv
from pineal.parser import parse
import pineal.config
from pineal.config import MODULES


def main():
    pineal.config.__dict__.update(parse())

    m = [p for p in MODULES if '--'+p.lower() in argv][0]

    try:
        __import__(m.lower(), globals(), locals(), [m], -1).__dict__[m]().run()
    except KeyboardInterrupt:
        pass
