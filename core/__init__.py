class PinealObject:
    memo = {}

    def create(self):
        pass

    def connect(self, other):
        other.draw()

    def draw(self):
        pass

    def ouput(self, other):
        other.draw()

    # ^  hackable  ^
    # -            -
    # v  magic     v

    def __init__(self, *args, **kwargs):
        self.create(*args, **kwargs)

    def __or__(self, other):
        class New(PinealObject):
            def draw(new_self):
                self.draw()
                self.connect(self, other)

            def connect(new_self, next_other):
                # the new object encapsulates the right-side connect method
                other.connect(next_other)

    def __rshift__(self, target):
        target.output(self)
