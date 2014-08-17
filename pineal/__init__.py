from pineal.config import CLASSES, MODULES


def main():
    procs = [Cl() for Cl in CLASSES if Cl.__name__.lower() in MODULES]

    for p in procs:
        p.start()

    try:
        for p in procs:
            p.join()
    except KeyboardInterrupt:
        print
        procs.reverse()
        for p in procs:
            p.stop()
            p.join()
