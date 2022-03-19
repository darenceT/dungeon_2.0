# import pytest
from Room import Room
from Grid import Grid, GridStr


def test_room_bare_empty():
    r = Room()
    assert f"{r}" == ''.join([
        "+-----+\n",
        "|     |\n",
        "+-----+\n",
    ])


def test_grid_room():
    g = Grid(3, 4)
    assert g.room(2, 3) is g.rooms[3][2]


def test_grid_sub():
    g1 = Grid(4, 5)
    # dbg_print(f"g1...\n{g1}")
    g2 = Grid(2, 3, from_grid=g1, from_coords=(2, 1))
    # dbg_print(f"g2...\n{g2}")
    assert [g2.width, g2.height] == [2, 3]
    assert g2.room(0, 0) is g1.room(2, 1)
    assert g2.room(1, 2) is g1.room(3, 3)


def test_gridstr_1x1_empty():
    g = Grid(1, 1)
    gs = GridStr(g, style=Room.styles.coords)
    assert str(gs) == ''.join([
        "+-----+\n",
        "| 0,0 |\n",
        "+-----+\n",
    ])


def test_gridstr_1x2_empty():
    g = Grid(1, 2)
    gs = GridStr(g, style=Room.styles.coords)
    assert str(gs) == ''.join([
        "+-----+\n",
        "| 0,0 |\n",
        "+-----+\n",
        "| 0,1 |\n",
        "+-----+\n",
    ])


def test_gridstr_2x1_empty():
    g = Grid(2, 1)
    gs = GridStr(g, style=Room.styles.coords)
    assert str(gs) == ''.join([
        "+-----+-----+\n",
        "| 0,0 | 1,0 |\n",
        "+-----+-----+\n",
    ])


def test_gridstr_2x1_tomstyle():
    g = Grid(2, 1)
    gs = GridStr(g, style=Room.styles.tom)
    assert str(gs) == ''.join([
        "*************\n",
        "*     *     *\n",
        "*************\n",
    ])

# END
