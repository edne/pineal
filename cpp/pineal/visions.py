import logging
import hy

from pineal.utils import watch_file
from pineal.hy_utils import run_hy_code


def load(file_name):
    "Load a DSL file and keep watching on it"
    logger = logging.getLogger(file_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    ns = {}  # execution namespace
    history = []  # history of file changes

    def run_code():
        "Run last code in the history, if available"
        if history:
            try:
                run_hy_code(history[-1], ns)
            except Exception as e:
                logger.info("Error evaluating code")
                logger.error(e)
                history.pop()
                run_code()
        else:
            logger.error("Empty history, there is no valid code")

    def update_file():
        "Update running code, saving in the history"
        logger.info("Updating file")

        with open(file_name) as f:
            code = f.read()

        history.append(code)
        run_code()

    update_file()
    watcher = watch_file(file_name, update_file)

    class Vision:
        def loop(self):
            "Main iteration, handel errors"
            try:
                ns["loop"]()
            except Exception as e:
                logger.error(e)
                history.pop()
                run_code()

        def stop(self):
            "Ask watcher to stop"
            watcher.stop()

        def join(self):
            "Join watcher thread"
            watcher.join()

    return Vision()
