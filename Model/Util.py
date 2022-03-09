from collections import namedtuple


def seq_repr(obj, **kw):
    return ', '.join([f'{obj_repr(i, **kw)}' for i in obj])


def map_repr(obj, **kw):
    bare_str = False
    if 'bare_str' in kw:
        bare_str = kw.pop('bare_str')
    return ', '.join([f'{obj_repr(k, **kw, bare_str=bare_str)}: {obj_repr(v, **kw)}' for k, v in obj.items()])


def obj_repr(obj, seen: set = None, show_ids: bool = False, bare_str: bool = False):
    """
    Custom `__repr__()` for objects.
    Unlike built-in `repr()`, attribute names are listed.
    For each private attribute (one whose name has leading underscores),
    the munging prefixed to its key in `<object>.__dict__` is stripped.
    That prefix is always of the form `_<classname>` where `<classname>`
    is normalized such that exactly one leading underscore is present,
    e.g. attribute `__foo` of class `__Bar` is munged to `_Bar__foo`.
    """
    _nobj = obj  # temp var, workaround to warning about no None.__class__
    if _nobj is None:
        return 'None'
    if isinstance(obj, str) and bare_str:
        return obj
    if isinstance(obj, (bool, int, float, str, bytes, bytearray)):
        return repr(obj)
    if isinstance(obj, type):
        return obj.__name__
    cls = obj.__class__
    # print(f'Seen: {id(obj)} {cls.__name__}')

    if seen is None:
        seen = set()
    seen.add(id(obj))
    # Omit bare_str from kw, so resets to default when recursing
    kw = {'seen': seen, 'show_ids': show_ids}
    oid = ''
    if show_ids:
        oid = f'{id(obj)} '

    wrap = {tuple: '()', list: '[]', set: '{}', dict: '{}'}
    if cls in (tuple, list, set):
        return f'{wrap[cls][0]}{oid}{seq_repr(obj, **kw)}{wrap[cls][1]}'
    elif cls is dict:
        return f'{wrap[cls][0]}{oid}{map_repr(obj, **kw)}{wrap[cls][1]}'

    nam = cls.__name__
    # namedtuple is weird: Ostensibly a subclass of tuple, but not a class
    # in its own right, and cannot do isinstance(obj, namedtuple).
    # Only way I see to discern them is presence of the several additional
    # methods and attributes. Attribute _asdict is particularly useful,
    # given that namedtuple does not have attribute __dict__.
    if isinstance(obj, tuple) and getattr(obj, '_asdict'):
        d = obj._asdict()
        return f'{nam}({oid}{map_repr(d, **kw, bare_str=True)})'

    mro = cls.__mro__
    ign = ('object', 'tuple', 'list', 'set', 'dict')
    pfx = [f"_{c.__name__.lstrip('_')}" for c in mro if c.__name__ not in ign]
    attrs = {}
    k: str
    for k, v in obj.__dict__.items():
        for p in pfx:
            if not k.startswith('_'):
                break
            k = k.removeprefix(p)
        if id(v) in seen:
            attrs[k] = f'<ID:{id(v)}>'
        else:
            attrs[k] = v
    return f'{nam}({oid}{map_repr(attrs, **kw, bare_str=True)})'


if __name__ == '__main__':
    def example():
        class Example0:
            def __init__(self):
                self.__f0 = "a"
                self.also = None

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
        print(o)
        o = _Example1()
        print(o)
        o = Example0()
        print(o)
        print(obj_repr(o, show_ids=True))

        # Woohoo, crisscross!
        o2 = Example0()
        print(o2)
        print(obj_repr(o2, show_ids=True))
        print("add some cross-links...")
        o.also = o2
        o2.also = o
        print(obj_repr(o))
        print(obj_repr(o2))
        print(obj_repr(o, show_ids=True))
        print(obj_repr(o2, show_ids=True))

    example()

# END
