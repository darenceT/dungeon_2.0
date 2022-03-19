from Model.Item import *

# pit(trap)
def test_create_pit_object():
    t = Pit()
    assert isinstance(t, Pit)

def test_validate_pit_as_item_type():
    t = Pit()
    assert isinstance(t, Item)

def test_obtain_pit_damage():
    t = Pit()
    assert t.damage == 10

# bomb (not yet implemented in GUI)
def test_create_bomb_object():
    b = Bomb()
    assert isinstance(b, Bomb)

def test_validate_bomb_as_item_type():
    b = Bomb()
    assert isinstance(b, Item)

# vision potion
def test_create_vision_potion_object():
    v = VisionPotion()
    assert isinstance(v, VisionPotion)

def test_validate_vision_potion_as_potion_type():
    v = VisionPotion()
    assert isinstance(v, Potion)

def test_validate_vision_potion_as_item_type():
    v = VisionPotion()
    assert isinstance(v, Item)

def test_vision_potion_get_radius():
    v = VisionPotion()
    assert v.radius == 1

# health potion
def test_create_health_potion_object():
    h = HealthPotion()
    assert isinstance(h, HealthPotion)

def test_validate_health_potion_as_potion_type():
    h = HealthPotion()
    assert isinstance(h, Potion)

def test_validate_health_potion_as_item_type():
    h = HealthPotion()
    assert isinstance(h, Item)

def test_health_potion_get_points():
    h = HealthPotion()
    assert h.points == 10

# pillars
def test_obtain_abstraction_pillar():
    for p in Pillars:
        if p.name == "Abstraction":
            a = p
    assert a.name == 'Abstraction'
    assert a.abbr == 'A'

def test_validate_abstraction_pillar_as_pillar_type():
    for p in Pillars:
        if p.name == "Abstraction":
            a = p
    assert isinstance(a, Pillar)

def test_validate_abstraction_pillar_as_item_type():
    for p in Pillars:
        if p.name == "Abstraction":
            a = p
    assert isinstance(a, Item)

def test_obtain_encapsulation_pillar():
    for p in Pillars:
        if p.name == "Encapsulation":
            e = p
    assert e.name == 'Encapsulation'
    assert e.abbr == 'E'

def test_validate_encapsulation_pillar_as_pillar_type():
    for p in Pillars:
        if p.name == "Encapsulation":
            e = p
    assert isinstance(e, Pillar)

def test_validate_encapsulation_pillar_as_item_type():
    for p in Pillars:
        if p.name == "Encapsulation":
            e = p
    assert isinstance(e, Item)

def test_obtain_inheritance_pillar():
    for p in Pillars:
        if p.name == "Inheritance":
            i = p
    assert i.name == 'Inheritance'
    assert i.abbr == 'I'

def test_validate_inheritance_pillar_as_pillar_type():
    for p in Pillars:
        if p.name == "Inheritance":
            i = p
    assert isinstance(i, Pillar)

def test_validate_inheritance_pillar_as_item_type():
    for p in Pillars:
        if p.name == "Inheritance":
            poly = p
    assert isinstance(poly, Item) 

def test_obtain_polymorphism_pillar():
    for p in Pillars:
        if p.name == "Polymorphism":
            poly = p
    assert poly.name == 'Polymorphism'
    assert poly.abbr == 'P'

def test_validate_polymorphism_pillar_as_pillar_type():
    for p in Pillars:
        if p.name == "Polymorphism":
            poly = p
    assert isinstance(poly, Pillar)

def test_validate_polymorphism_pillar_as_item_type():
    for p in Pillars:
        if p.name == "Polymorphism":
            poly = p
    assert isinstance(poly, Item)

def test_obtain_invalid_pillar():
    v = None
    for p in Pillars:
        if p.name == 'Validationism':
            v = p
    assert v is None