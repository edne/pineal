from __future__ import print_function
import sys
import logging
import tokenize as tkn
from io import BytesIO

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class ParserError(Exception):
    'Error in parsing'


def to_tokens(code):
    bytes_stream = BytesIO(code.encode('utf-8'))
    if sys.version_info > (3, 0):
        g = tkn.tokenize(bytes_stream.readline)
    else:
        g = tkn.generate_tokens(bytes_stream.readline)

    return [(n, v) for (n, v, _, _, _) in g]


def is_newline(t):
    toknum, _ = t
    return toknum == tkn.NEWLINE or toknum == tkn.NL


def split_lines(tokens):
    current_line = []
    for t in tokens:
        if t[0] == 59:  # ENCODING
            pass

        elif is_newline(t):
            if current_line:
                yield current_line
                current_line = []

        else:
            if t[0] in (tkn.INDENT, tkn.DEDENT):
                if current_line:
                    yield current_line
                    current_line = []

                yield t[0]

            else:
                current_line.append(t[1])


def make_blocks(lines):
    nesting = 0

    for i, line in enumerate(lines):
        if line == tkn.INDENT:
            if nesting == 0:
                yield list(make_blocks(lines[i+1:]))
            nesting += 1

        elif line == tkn.DEDENT:
            if nesting == 0:
                return
            else:
                nesting -= 1

        else:
            if nesting == 0:
                yield line


def join_blocks(blocks):
    for i, block in enumerate(blocks):
        if ':' in block:
            colon_index = block.index(':')

            head = ' '.join(block[:colon_index])
            leaf = ' '.join(block[colon_index+1:])

            if leaf:
                yield [head, leaf]
            else:
                yield [head, list(join_blocks(blocks[i+1]))]


def parse(code):
    tokens = to_tokens(code)

    lines = list(split_lines(tokens))
    blocks = list(make_blocks(lines))
    tree = list(join_blocks(blocks))

    return tree
