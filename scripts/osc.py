import liblo


def check_address(addr):
    "If only port is specified send to localhost"
    splitted = str(addr).split(":")
    if splitted[1:]:
        return addr
    else:
        return ":".join(["localhost", splitted[0]])


def send(addr, path, *msg):
    """address path message
    Send message on a given path"""
    addr = check_address(addr)
    target = liblo.Address("osc.udp://" + addr + "/")
    liblo.send(target, path, *msg)
