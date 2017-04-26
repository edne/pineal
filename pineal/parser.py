import logging
from tools import apply_effects, group
from tools import polygon, scale
from pineal.tree_parser import make_tree

log = logging.getLogger(__name__)


class ParserError(Exception):
    pass


# TODO: check in namespace or in a symbol table
_primitives = {'polygon': polygon}
_effects = {'scale': scale}


def make_effect(branch, namespace):
    name, leaf = branch
    arg = eval(leaf)
    effect = _effects[name](arg)
    return effect


def make_group(tree, namespace):
    log.debug('Group tree: {}'.format(tree))
    entities = [make_entity(branch, namespace)
                for branch in tree]
    return group(entities)


def make_entity(tree, namespace):
    log.debug(tree)
    name, body = tree

    effects = [make_effect(branch, namespace)
               for branch in body
               if branch[0] in _effects]

    body = [(key, value)
            for (key, value) in body
            if key not in _effects]

    if name in _primitives:
        kwargs = {key: eval(value)
                  for (key, value) in body}

        entity = _primitives[name](**kwargs)

    elif name == 'group':
        # TODO: named groups
        entity = make_group(body, namespace)

    else:
        # TODO: layers
        raise ParserError('Invalid entity')

    return apply_effects(entity, effects)


def parse_draw(tree, namespace):
    entities = [make_entity(branch, namespace)
                for branch in tree]

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

    for head, body in tree:
        if head == 'draw':
            parse_draw(body, namespace)


def parse(code, namespace):
    tree = make_tree(code)
    log.debug(tree)

    parse_top_level(tree, namespace)
