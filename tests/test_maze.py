# import pytest
from Room import Room
from Maze import Maze

g_dbg_enabled = False


def dbg_print(*args, **kwargs):
    if g_dbg_enabled:
        print(*args, **kwargs)


def test_maze_default():
    # Default 4x4 grid, no doors yet
    dbg_print(f"\nDefault 4x4 maze...")
    m = Maze(width=4, height=4)
    # Maze auto-generates by default, so nuke that.
    # Thus, every potential interior wall becomes a door.
    m.empty()
    dbg_print(m)
    assert m.str(style=Room.styles.coords) == """
+-----+-----+-----+-----+
| 0,0 = 1,0 = 2,0 = 3,0 |
+--H--+--H--+--H--+--H--+
| 0,1 = 1,1 = 2,1 = 3,1 |
+--H--+--H--+--H--+--H--+
| 0,2 = 1,2 = 2,2 = 3,2 |
+--H--+--H--+--H--+--H--+
| 0,3 = 1,3 = 2,3 = 3,3 |
+-----+-----+-----+-----+
""".lstrip()


def test_maze_measure():
    # Custom maze, only measure dimensions
    dbg_print(f"\nCustom 2x2, measure only...")
    map_str = """
# This is my 2x2 dungeon
+-----+-----+
| E   =     |
+-----+--H--+
|     | O   |
+-----+-----+
""".lstrip()
    dbg_print(map_str)
    width, height = Maze.parse_map(map_str)
    dbg_print(f"maze width={width} height={height}")
    assert [width, height] == [2, 2]


def test_maze_parse():
    # Full init from canned maze
    dbg_print(f"\nCustom 3x2, full load...")
    map_str = """
# This is my 3x2 dungeon
+-----+-----+-----+
| E   |     = O   |
+--H--+--H--+-----+
|     =     =     |
+-----+-----+-----+
""".lstrip()
    dbg_print(map_str)
    m = Maze(map_str=map_str)
    dbg_print(f"maze width={m.width} height={m.height}")
    assert [m.width, m.height] == [3, 2]
    dbg_print(f"maze (formatted)...\n{m}")
    assert str(m) == """
+-----+-----+-----+
| E   |     = O   |
+--H--+--H--+-----+
|     =     =     |
+-----+-----+-----+
""".lstrip()


if __name__ == '__main__':
    print("Run pytest, you fool!")

# END
