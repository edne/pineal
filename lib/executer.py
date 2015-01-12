def load(filename):
    with open(filename) as f:
        code = f.read()
        #print(code)
        return code


def run(code):
    d = {}
    exec code in d
    return d
