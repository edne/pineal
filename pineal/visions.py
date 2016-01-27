import logging
import liblo
import hy

from pineal.utils import watch_file
from pineal.hy_utils import eval_hy_code


def load(file_name):
    "Load a DSL file and keep watching on it"
    logger = logging.getLogger(file_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    ns = {}  # execution namespace
    history = []  # history of file changes

    server = liblo.ServerThread(7172)
    server.start()
    ns["__server__"] = server
    ns["__values__"] = {}

    def eval_code():
        "Run last code in the history, if available"
        if history:
            try:
                logger.debug("Running:\n{}".format(history[-1]))
                eval_hy_code(history[-1], ns)
            except Exception as e:
                logger.info("Error evaluating code")
                logger.error(e)
                history.pop()
                eval_code()
        else:
            logger.error("Empty history, there is no valid code")

    def update_file():
        "Update running code, saving in the history"
        logger.info("Updating %s" % file_name)

        with open(file_name) as f:
            code = f.read()

        code = "(require pineal.dsl) (loop [] {})".format(code)

        history.append(code)
        eval_code()

    update_file()
    watcher = watch_file(file_name, update_file)

    class Vision(object):
        "Represent a dsl file and wrap the watcher"

        @staticmethod
        def loop():
            "Main iteration, handel errors"
            try:
                return ns["__loop__"]()
            except Exception as e:
                logger.error(e)
                history.pop()
                eval_code()

        @staticmethod
        def stop():
            "Ask watcher to stop"
            watcher.stop()
            server.stop()

        @staticmethod
        def join():
            "Join watcher thread"
            watcher.join()

    return Vision()
