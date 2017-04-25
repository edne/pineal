import logging
import yaml
from tools import polygon

log = logging.getLogger(__name__)


class ParserError(Exception):
    pass


# TODO: check in namespace or in a symbol table
primitives = {'polygon': polygon}


def make_entity(tree):
    # tree: {'polygon': {'sides': 4, ...}}
    # tree.items(): [('polygon', {...})]
    name, params = tree.items()[0]

    if name in primitives:
        entity = primitives[name](**params)
    else:
        # TODO: make groups and layers
        raise ParserError('Invalid entity')

    return entity


def parse_draw(tree, namespace):
    if not isinstance(tree, list):
        raise ParserError('Draw should take a list of items')

    entities = [make_entity(branch) for branch in tree]

    def draw():
        for entity in entities:
            entity()

    namespace['draw'] = draw


def parse_top_level(tree, namespace):
    # TODO:
    # module
    # osc-in
    # palette
    # parse_definitions(tree, namespace)  # layer, group

    if 'draw' not in tree:
        raise ParserError('Missing draw entry')
    else:
        parse_draw(tree['draw'], namespace)


def parse(code, namespace):
    tree = yaml.load(code)
    log.debug(tree)

    parse_top_level(tree, namespace)
