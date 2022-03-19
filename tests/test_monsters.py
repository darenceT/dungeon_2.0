from Model.Characters.DungeonCharacter import DungeonCharacter
from Model.Characters.Monster import Monster
from Model.Characters.Healable import Healable
from Model.Characters.Ogre import Ogre
from Model.Characters.Gremlin import Gremlin
from Model.Characters.Skeleton import Skeleton
from Model.Characters.MeanGirl import MeanGirl
from Model.Characters.MonsterSpawn import MonsterSpawn

 

# Ogre

def test_monster_spawning_ogre():
    ms = MonsterSpawn()
    m = ms.make('ogre')
    assert isinstance(m, Ogre)

def test_create_ogre_object():
    m = Ogre('ogre', 'joe')
    assert isinstance(m, Ogre)

def test_validate_ogre_inherit_monster():
    m = Ogre('ogre', 'joe')
    assert isinstance(m, Monster)

def test_validate_ogre_inherit_DungeonCharacter():
    m = Ogre('ogre', 'joe')
    assert isinstance(m, DungeonCharacter)

def test_validate_ogre_inherit_Healable():
    m = Ogre('ogre', 'joe')
    assert isinstance(m, Healable)

def test_assign_name_ogre():
    m = Ogre('ogre', 'Meek')
    assert m.name == 'Meek'

def test_ogre_not_alive():
    m = Ogre('ogre', 'joe')
    m.hit_points = 0
    assert m.is_alive == False

# Gremlin

def test_monster_spawning_gremlin():
    ms = MonsterSpawn()
    m = ms.make('gremlin')
    assert isinstance(m, Gremlin)

def test_create_gremlin_object():
    m = Gremlin('gremlin', 'gitty')
    assert isinstance(m, Gremlin)

def test_validate_gremlin_inherit_monster():
    m = Gremlin('gremlin', 'gitty')
    assert isinstance(m, Monster)

def test_validate_gremlin_inherit_DungeonCharacter():
    m = Gremlin('gremlin', 'gitty')
    assert isinstance(m, DungeonCharacter)

def test_validate_gremlin_inherit_Healable():
    m = Gremlin('gremlin', 'gitty')
    assert isinstance(m, Healable)

def test_assign_name_gremlin():
    m = Gremlin('gremlin', 'Gity')
    assert m.name == 'Gity'

def test_gremlin_not_alive():
    m = Gremlin('gremlin', 'gitty')
    m.hit_points = 0
    assert m.is_alive == False

# Skeleton

def test_monster_spawning_skeleton():
    ms = MonsterSpawn()
    m = ms.make('skeleton')
    assert isinstance(m, Skeleton)

def test_create_skeleton_object():
    m = Skeleton('skeleton', 'Bonezy')
    assert isinstance(m, Skeleton)

def test_validate_skeleton_inherit_monster():
    m = Skeleton('skeleton', 'Bonezy')
    assert isinstance(m, Monster)

def test_validate_skeleton_inherit_DungeonCharacter():
    m = Skeleton('skeleton', 'Bonezy')
    assert isinstance(m, DungeonCharacter)

def test_validate_skeleton_inherit_Healable():
    m = Skeleton('skeleton', 'Bonezy')
    assert isinstance(m, Healable)

def test_assign_name_skeleton():
    m = Skeleton('skeleton', 'Skiletor')
    assert m.name == 'Skiletor'

def test_skeleton_not_alive():
    m = Skeleton('skeleton', 'gitty')
    m.hit_points = 0
    assert m.is_alive == False

# Mean Girl

def test_monster_spawning_mgirl():
    ms = MonsterSpawn()
    m = ms.make('mgirl')
    assert isinstance(m, MeanGirl)

def test_create_mgirl_object():
    m = MeanGirl('mgirl', 'Jacky')
    assert isinstance(m, MeanGirl)

def test_validate_mgirl_inherit_monster():
    m = MeanGirl('mgirl', 'Jacky')
    assert isinstance(m, Monster)

def test_validate_mgirl_inherit_DungeonCharacter():
    m = MeanGirl('mgirl', 'Jacky')
    assert isinstance(m, DungeonCharacter)

def test_validate_mgirl_inherit_Healable():
    m = MeanGirl('mgirl', 'Jacky')
    assert isinstance(m, Healable)

def test_assign_name_mgirl():
    m = MeanGirl('mgirl', 'Jeebus')
    assert m.name == 'Jeebus'

def test_mgirl_not_alive():
    m = MeanGirl('mgirl', 'Jacky')
    m.hit_points = 0
    assert m.is_alive == False