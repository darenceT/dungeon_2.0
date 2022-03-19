from Model.Room import Room
from Model.Cell import Cell
from Model.Box import Box
from Model.Item import *
from Model.Characters.Ogre import Ogre

# room creation
def test_create_room_object():
    r = Room()
    assert isinstance(r, Room)

def test_validate_room_as_cell_type():
    r = Room()
    assert isinstance(r, Cell)

def test_validate_room_as_box_type():
    r = Room()
    assert isinstance(r, Box)

# add objects to room
def test_room_is_empty():
    r = Room()
    assert len(r.contents) == 0
    assert len(r.occupants) == 0

def test_add_single_items_to_room():
    r = Room()
    r.add(Pit)
    assert r.has(Pit) == True
    assert len(r.contents) == 1
    r.add(HealthPotion)
    assert r.has(HealthPotion) == True 
    assert len(r.contents) == 2
    assert r.has(Pillar) == False

def test_add_multiple_items_to_room():
    r = Room()
    r.add(Pit, HealthPotion, VisionPotion)
    assert r.has(Pit) is True
    assert r.has(HealthPotion) is True
    assert r.has(VisionPotion) is True
    assert r.has(Pillar) is False
    assert r.has(Bomb) is False

def test_remove_one_item_from_room():
    r = Room()
    p = VisionPotion()
    r.add(p)
    r.pop(p)
    assert r.has(VisionPotion) is False
    # TODO unit test in progress
    # assert len(r.contents) == 0
    # r.add(HealthPotion)
    # r.pop(HealthPotion)
    # assert r.has(HealthPotion) == False
    # assert len(r.contents) == 0 

def test_add_monster_to_room():
    r = Room()
    m = Ogre('ogre', "Boo")
    # TODO unit test in progress
    # assert r.has(Ogre) is True
