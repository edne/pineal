import logging
import yaml
from tools import apply_effects
from tools import polygon, scale

log = logging.getLogger(__name__)


class ParserError(Exception):
    pass


# TODO: check in namespace or in a symbol table
_primitives = {'polygon': polygon}
_effects = {'scale': scale}


def make_effect(name, leaf):
    # TODO: multiple arguments
    arg = leaf
    effect = _effects[name](arg)
    return effect


def make_entity(tree):
    # tree: {'polygon': {'sides': 4, ...}}
    # tree.items(): [('polygon', {...})]
    name, params = tree.items()[0]

    effects = [make_effect(k, params[k])
               for k in params
               if k in _effects]

    params = {key: value
              for (key, value) in params.items()
              if key not in _effects}

    if name in _primitives:
        entity = _primitives[name](**params)
    else:
        # TODO: make groups and layers
        raise ParserError('Invalid entity')

    return apply_effects(entity, effects)


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
