from time import sleep
from threading import Thread
from pineal.eye import eye
from pineal.ear import ear
from pineal.coder import coder


def run_thread(f):
    t = Thread(target=f)
    t.daemon = True
    t.start()


if __name__ == '__main__':
    run_thread(eye)
    run_thread(ear)
    run_thread(coder)

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print()
