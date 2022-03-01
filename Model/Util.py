def obj_repr(self):
    cls = self.__class__.__name__
    pfx = f"_{cls}__"
    attrs = dict([(k.removeprefix(pfx), v) for k, v in self.__dict__.items()])
    return f"({self.__class__.__name__}){attrs}"

# END
