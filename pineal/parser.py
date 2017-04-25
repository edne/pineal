import logging
import yaml
from tools import polygon

log = logging.getLogger(__name__)


class ParserError(Exception):
    pass


primitives = {'polygon': polygon}


def get_entities(tree):
    entities = []

    # tree: [{'polygon': {'sides': 4, ...}}, ...]
    for branch in tree:
        # branc.items(): [('polygon', {...})]
        name, kwargs = branch.items()[0]

        if name in primitives:
            # TODO: check in namespace or in a symbol table
            entity = primitives[name](**kwargs)
            entities.append(entity)

    return entities


def parse_draw(tree, namespace):
    if not isinstance(tree, list):
        raise ParserError('Draw should take a list of items')

    entities = get_entities(tree)

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
