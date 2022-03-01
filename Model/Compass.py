from Direction import Direction

North = Direction('N', 'North', (0, 1))
South = Direction('S', 'South', (0, -1))
East = Direction('E', 'East', (1, 0))
West = Direction('W', 'West', (-1, 0))
Northeast = Direction('NE', 'Northeast', (1, 1))
Southeast = Direction('SE', 'Southeast', (1, -1))
Northwest = Direction('NW', 'Northwest', (-1, 1))
Southwest = Direction('SW', 'Southwest', (-1, -1))


class Compass:
    dirs: list[Direction] = [
        North, South, East, West,
        Northeast, Southeast, Northwest, Southwest,
    ]

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
            print(f"{s} -> {d}")

    example()

# END
