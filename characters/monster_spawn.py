import sqlite3
from monster_factory import *

"""Get random row number - done"""
"""Get monster type"""
"""use monster.create to create monster"""
#TODO: Convert query to dictionary. Assign mtype value to mtype variable. Call monstername.create

def monster_spawn():
    conn = sqlite3.connect("monster.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM monsterstats ORDER BY RANDOM() LIMIT 1")
    monster_data = cur.fetchone()
    print(monster_data.keys())
    print(monster_data['name'])
    print(monster_data['mtype'])
    MonsterFactory.create_monster(mtype=monster_data['mtype'],name=monster_data['name'],
                                  hit_points=monster_data['hit_points'], attack_speed = monster_data['attack_speed'],
                                  chance_to_hit = monster_data['chance_to_hit'],
                                  minimum_damage = monster_data['minimum_damage'],
                                  maximum_damage=monster_data['maximum_damage'],
                                  chance_to_heal = monster_data['chance_to_heal'],
                                  minimum_heal_points = monster_data['minimum_heal_points'],
                                  maximum_heal_points = monster_data['maximum_heal_points'])


    # for row in monster_data:
     #   print(row)
    # conn.close()
    # name = row[0]
    # mtype = row[1]
    # def dict_from_row(row):
    #     return dict(zip(row.keys(), row))
    # monster_data = dict_from_row(row)
    # MonsterFactory.create_monster(mtype,monster_data)

monster_spawn()
