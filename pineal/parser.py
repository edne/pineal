import logging
from tools import apply_effects, group
from tools import polygon, scale
from tools import default_colors
from pineal.tree_parser import make_tree

log = logging.getLogger(__name__)


class ParserError(Exception):
    pass


# TODO: check in namespace or in a symbol table
_primitives = {'polygon': polygon}
_effects = {'scale': scale}


def make_effect(branch, ns):
    name, leaf = branch
    arg = eval(leaf, ns)
    effect = _effects[name](arg)
    return effect


def make_group(tree, ns):
    log.debug('Group tree: {}'.format(tree))
    entities = [make_entity(branch, ns)
                for branch in tree]
    return group(entities)


def make_entity(tree, ns):
    log.debug(tree)
    name, body = tree

    effects = [make_effect(branch, ns)
               for branch in body
               if branch[0] in _effects]

    body = [(key, value)
            for (key, value) in body
            if key not in _effects]

    if name in _primitives:
        kwargs = {key: eval(value, ns)
                  for (key, value) in body}

        entity = _primitives[name](**kwargs)

    elif name == 'group':
        # TODO: named groups
        entity = make_group(body, ns)

    else:
        # TODO: layers
        raise ParserError('Invalid entity')

    return apply_effects(entity, effects)


def parse_draw(tree, ns):
    entities = [make_entity(branch, ns)
                for branch in tree]

    def draw():
        for entity in entities:
            entity()

    ns['draw'] = draw


def parse_top_level(tree, ns):
    # TODO:
    # module
    # osc-in
    # palette
    # parse_definitions(tree, ns)  # layer, group

    ns.update(default_colors)

    for head, body in tree:
        if head == 'draw':
            parse_draw(body, ns)


def parse(code, ns):
    tree = make_tree(code)
    log.debug(tree)

    parse_top_level(tree, ns)
