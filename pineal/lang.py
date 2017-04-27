import logging
from tools import polygon, scale
from tools import default_colors, palette
from tools import osc_in
from pineal.parser import parse

log = logging.getLogger(__name__)


# TODO: check in namespace or in a symbol table
_primitives = {'polygon': polygon}
_effects = {'scale': scale}


def apply_effect(entity, effect):
    def new_entity():
        effect(entity)

    return new_entity


def apply_effects(entity, effects):
    log.debug(effects)

    for effect in effects:
        entity = apply_effect(entity, effect)

    return entity


def eval_leaf(leaf, ns):
    "Leaf should be a python expression"
    # TODO: return a funcion
    return eval(leaf, ns)


def make_effect(tree, ns):
    name, leaf = tree
    arg = eval_leaf(leaf, ns)
    effect = _effects[name](arg)
    return effect


def make_entity(tree, ns):
    name, body = tree

    effects = [make_effect(branch, ns)
               for branch in body
               if branch[0] in _effects]

    body = [(key, value)
            for (key, value) in body
            if key not in _effects]

    if name in _primitives:
        kwargs = {key: eval_leaf(value, ns)
                  for (key, value) in body}

        entity = _primitives[name](**kwargs)

    else:
        # TODO: layers
        raise Exception('Invalid entity')

    return apply_effects(entity, effects)


def eval_draw(tree, ns):
    def draw():
        entities = [make_entity(branch, ns)
                    for branch in tree]

        for entity in entities:
            entity()

    ns['draw'] = draw


def eval_top_level(tree, ns):
    # TODO:
    # module
    # osc-in
    # eval_definitions(tree, ns)  # layer, group

    ns.update(default_colors)

    for head, body in tree:
        if head.startswith('source '):
            name = head.split()[1]
            ns.update({
                name: osc_in(eval_leaf(body, ns))
            })

        if head.startswith('palette '):
            name = head.split()[1]
            ns.update({
                name: palette(eval_leaf(body, ns))
            })

        elif head == 'draw':
            eval_draw(body, ns)


def pineal_eval(code, ns):
    tree = parse(code)
    log.debug(tree)

    eval_top_level(tree, ns)
