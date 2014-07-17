import graphic, visuals, loader, analyzer, gui


def main():
    graphic.init()
    visuals.init()
    loader.init()
    analyzer.init()
    gui.init()

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
