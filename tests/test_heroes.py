from Model.Characters.DungeonCharacter import DungeonCharacter
from Model.Characters.Healable import Healable
from Model.Characters.Thief import Thief
from Model.Characters.Priestess import Priestess
from Model.Characters.Warrior import Warrior
from Model.Characters.Hero import Hero

# Thief

def test_create_thief_object():
    t = Thief()
    assert isinstance(t, Thief)

def test_validate_thief_inherit_hero():
    t = Thief()
    assert isinstance(t, Hero)

def test_validate_thief_inherit_DungeonCharacter():
    t = Thief()
    assert isinstance(t, DungeonCharacter)

def test_validate_thief_guild():
    t = Thief()
    assert t.guild == 'Thief'

def test_assign_name_thief():
    t = Thief(name="Jack")
    assert t.name == 'Jack'

def test_thief_special_skill():
    t = Thief()
    results = t.special_skill()
    expected = (80, 'Your Surprise Attack: Triple Daggers!')
    assert (results == expected)

def test_thief_not_alive():
    t = Thief()
    t.hit_points = 0
    assert t.is_alive == False

# Priestess

def test_create_priestess_object():
    t = Priestess()
    assert isinstance(t, Priestess)

def test_validate_priestess_inherit_hero():
    t = Priestess()
    assert isinstance(t, Hero)

def test_validate_priestess_inherit_DungeonCharacter():
    t = Priestess()
    assert isinstance(t, DungeonCharacter)

def test_validate_priestess_inherit_Healable():
    t = Priestess()
    assert isinstance(t, Healable)

def test_validate_priestess_guild():
    t = Priestess()
    assert t.guild == 'Priestess'

def test_assign_name_priestess():
    t = Priestess(name="Jill")
    assert t.name == 'Jill'

def test_priestess_special_skill_message():
    t = Priestess()
    results = t.special_skill()
    expected = (0, 'You healed yourself by 20 points!')
    assert (results == expected)

def test_priestess_special_skill_heal():
    t = Priestess()
    t.hit_points = 10
    t.special_skill()
    assert (t.hit_points == 30)

def test_priestess_not_alive():
    t = Priestess()
    t.hit_points = 0
    assert t.is_alive == False


# Warrior

def test_create_warrior_object():
    t = Warrior()
    assert isinstance(t, Warrior)

def test_validate_warrior_inherit_hero():
    t = Warrior()
    assert isinstance(t, Hero)

def test_validate_warrior_inherit_DungeonCharacter():
    t = Warrior()
    assert isinstance(t, DungeonCharacter)

def test_validate_warrior_guild():
    t = Warrior()
    assert t.guild == 'Warrior'

def test_assign_name_warrior():
    t = Warrior(name="Bill")
    assert t.name == 'Bill'

def test_warrior_special_skill():
    t = Warrior()
    results = t.special_skill()
    expected = (100, 'Aiyaaaaaaaa, Crushing Blow!')
    assert (results == expected)

def test_warrior_not_alive():
    t = Warrior()
    t.hit_points = 0
    assert t.is_alive == False
