def obj_repr(obj):
    """
    Custom `__repr__()` for objects.
    Unlike built-in `repr()`, attribute names are listed.
    For each private attribute (one whose name has leading underscores),
    the munging prefixed to its key in `<object>.__dict__` is stripped.
    That prefix is always of the form `_<classname>` where `<classname>`
    is normalized such that exactly one leading underscore is present,
    e.g. attribute `__foo` of class `__Bar` is munged to `_Bar__foo`.
    """
    cls = obj.__class__
    nam = cls.__name__
    mro = cls.__mro__
    ign = ('object', 'list', 'set', 'dict')
    pfx = [f"_{c.__name__.lstrip('_')}" for c in mro if c.__name__ not in ign]
    attrs = {}
    k: str
    for k, v in obj.__dict__.items():
        for p in pfx:
            if not k.startswith('_'):
                break
            k = k.removeprefix(p)
        attrs[k] = v
    return f"({nam}){attrs}"


def __example():

    class Example0:
        def __init__(self):
            self.__f0 = "a"

        def __repr__(self):
            return obj_repr(self)

    class _Example1(Example0):
        def __init__(self):
            super().__init__()
            self.__f1 = "b"

    class __Example2(_Example1):
        def __init__(self):
            super().__init__()
            self.__f2 = "c"

    o = __Example2()
    print(f"{o}")
    o = _Example1()
    print(f"{o}")
    o = Example0()
    print(f"{o}")


if __name__ == '__main__':
    __example()

# END
