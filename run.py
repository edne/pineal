from time import sleep
from pineal.eye import eye_runner
from pineal.ear import ear_runner
from pineal.coder import coder_runner


if __name__ == '__main__':
    eye = eye_runner()
    ear = ear_runner()
    coder = coder_runner()

    eye.start()
    ear.start()
    coder.start()

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print()

    eye.stop()
    ear.stop()
    coder.stop()
