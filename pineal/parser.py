import logging
import yaml
from tools import polygon

log = logging.getLogger(__name__)

primitives = {'polygon': polygon}


def parse(code, namespace):
    tree = yaml.load(code)
    log.debug(tree)

    def draw():
        for branch in tree:
            if branch in primitives:
                kwargs = tree[branch]
                entity = primitives[branch](**kwargs)
                entity()

    namespace['draw'] = draw
