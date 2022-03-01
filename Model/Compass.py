from Direction import Direction


class Compass:
    dirs: list[Direction] = [
        Direction('N', 'North', (0, 1)),
        Direction('S', 'South', (0, -1)),
        Direction('E', 'East', (1, 0)),
        Direction('W', 'West', (-1, 0)),
        Direction('NE', 'Northeast', (1, 1)),
        Direction('SE', 'Southeast', (1, -1)),
        Direction('NW', 'Northwest', (-1, 1)),
        Direction('SW', 'Southwest', (-1, -1)) ]

    def __getitem__(self, item):
        if isinstance(item, str):
            if len(item) == 1 or len(item) == 2:
                item = item.upper()
                for d in Compass.dirs:
                    if item == d.abbr:
                        return d
            elif len(item) > 2:
                item = item.capitalize()
                for d in Compass.dirs:
                    if item == d.name:
                        return d
        return None


if __name__ == '__main__':
    def example():
        x: Compass = Compass()
        for s in ('N n north North NORTH NoRtH foo'.split(' ')):
            d = x[s]
            print(f"{s} -> {repr(d)}")

    example()

# END
