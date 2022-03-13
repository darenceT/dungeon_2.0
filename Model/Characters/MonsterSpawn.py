import sqlite3
from .MonsterFactory import MonsterFactory

class MonsterSpawn:

    def __init__(self):
        self.create_database()

    @staticmethod
    def make(monster_type):
        conn = sqlite3.connect("monster.db")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM monsterstats ORDER BY RANDOM() LIMIT 1")
        monster_data = cur.fetchone()
        return MonsterFactory.create_monster(mtype=monster_type,name=monster_data['name'],
                                    hit_points=monster_data['hit_points'], attack_speed = monster_data['attack_speed'],
                                    chance_to_hit = monster_data['chance_to_hit'],
                                    minimum_damage = monster_data['minimum_damage'],
                                    maximum_damage=monster_data['maximum_damage'],
                                    chance_to_heal = monster_data['chance_to_heal'],
                                    minimum_heal_points = monster_data['minimum_heal_points'],
                                    maximum_heal_points = monster_data['maximum_heal_points'])

    @staticmethod
    def create_database():
            connection = sqlite3.connect("monster.db")
            cursor = connection.cursor()

            cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='monsterstats' ''')
            
            if cursor.fetchone()[0] == 1: 
                print('MonsterStats table already exists, skipping database creation')
            else :
                reference = {
                    '"Skeleton"': {
                        "names": ('"Henry Morgan"', '"Bjorn Ironside"', '"William Kid"', '"Edward Teach"', '"John Rackam"'),
                        "stats": "100, 3, 0.8, 30, 50, 0.3, 30, 50",
                    },
                    '"Gremlin"': {
                        "names": ('"Inglebrat Cumberbund"', '"Bendintine Camberbert"', '"Cumberland Inglesmerch"', '"Anglebracket Candlearbra"', '"Crumblebun Bennington"'),
                        "stats": "70, 5, 0.8, 15, 30, 0.4, 20, 40",
                    },
                    '"Ogre"': {
                        "names": ('"Durag"', '"Vrorob"', '"Wukur"', '"Blozug"', '"Nakorg"'),
                        "stats": "200, 2, 0.6, 30, 60, 0.1, 30, 60",
                    },
                    '"MeanGirl"': {
                        "names": ('"Anna Wintour"', '"Regina George"', '"Joan Crawford"', '"Heather Duke"', '"Paris Geller"'),
                        "stats": "100, 7, 0.9, 10, 30, 0.6, 10, 30",
                    },                
                }
                cursor.execute("CREATE TABLE monsterstats (name TEXT, mtype TEXT, hit_points INTEGER, attack_speed INTEGER, "
                            "chance_to_hit DECIMAL,  minimum_damage INTEGER, maximum_damage INTEGER, chance_to_heal DECIMAL, "
                            "minimum_heal_points INTEGER, maximum_heal_points INTEGER)")

                for mtype, data in reference.items():
                    for name in data["names"]:
                        cursor.execute(f"INSERT INTO monsterstats VALUES ({name}, {mtype}, {data['stats']})")

                connection.commit()
                connection.close()
                print("New MonsterStats table created.")

if __name__ == '__main__':
    print("Greetings from Monster Spawn!\n\n")

    print('Test to create new table (make sure monsterdb does not exist, otherwise it way say DB exists\n')
    m = MonsterSpawn()

    print('\nNow to make specific monsters')
    print(m.make('ogre'))
    print('Ogre object should be created')

    print(m.make('mgirl'))
    print('MeanGirl object should be created')