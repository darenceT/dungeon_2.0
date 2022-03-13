import sqlite3

class MonsterDB:

    """
    Creates Sqlite3 database (if it does not already exist) and creates monsterstats table. Inserts initial
    stats for each type of monster into monsterstats table. If table already exists, drops table and then recreates it 
    for a new game.
    """
    @staticmethod
    def create_database():
        connection = sqlite3.connect("monster.db")

        cursor = connection.cursor()
        dropstatement = "DROP TABLE IF EXISTS monsterstats"
        cursor.execute(dropstatement)
        cursor.execute("CREATE TABLE monsterstats (name TEXT, mtype TEXT, hit_points INTEGER, attack_speed INTEGER, "
                    "chance_to_hit DECIMAL,  minimum_damage INTEGER, maximum_damage INTEGER, chance_to_heal DECIMAL, "
                    "minimum_heal_points INTEGER, maximum_heal_points INTEGER)")
        cursor.execute("INSERT INTO monsterstats VALUES ('Henry Morgan', 'Skeleton', 100, 3, 0.8, 30, 50, 0.3, 30, 50)")
        cursor.execute("INSERT INTO monsterstats VALUES ('Bjorn Ironside', 'Skeleton', 100, 3, 0.8, 30, 50, 0.3, 30, 50)")
        cursor.execute("INSERT INTO monsterstats VALUES ('William Kid', 'Skeleton', 100, 3, 0.8, 30, 50, 0.3, 30, 50)")
        cursor.execute("INSERT INTO monsterstats VALUES ('Edward Teach', 'Skeleton', 100, 3, 0.8, 30, 50, 0.3, 30, 50)")
        cursor.execute("INSERT INTO monsterstats VALUES ('John Rackam', 'Skeleton', 100, 3, 0.8, 30, 50, 0.3, 30, 50)")
        cursor.execute("INSERT INTO monsterstats VALUES ('Inglebrat Cumberbund', 'Gremlin', 70, 5, 0.8, 15, 30, 0.4, 20, 40)")
        cursor.execute("INSERT INTO monsterstats VALUES ('Bendintine Camberbert', 'Gremlin', 70, 5, 0.8, 15, 30, 0.4, 20, 40)")
        cursor.execute("INSERT INTO monsterstats VALUES ('Cumberland Inglesmerch', 'Gremlin', 70, 5, 0.8, 15, 30, 0.4, 20, 40)")
        cursor.execute("INSERT INTO monsterstats VALUES ('Anglebracket Candlearbra', 'Gremlin', 70, 5, 0.8, 15, 30, 0.4, 20, 40)")
        cursor.execute("INSERT INTO monsterstats VALUES ('Crumblebun Bennington', 'Gremlin', 70, 5, 0.8, 15, 30, 0.4, 20, 40)")
        cursor.execute("INSERT INTO monsterstats VALUES ('Durag', 'Ogre', 200, 2, 0.6, 30, 60, 0.1, 30, 60)")
        cursor.execute("INSERT INTO monsterstats VALUES ('Vrorob', 'Ogre', 200, 2, 0.6, 30, 60, 0.1, 30, 60)")
        cursor.execute("INSERT INTO monsterstats VALUES ('Wukur', 'Ogre', 200, 2, 0.6, 30, 60, 0.1, 30, 60)")
        cursor.execute("INSERT INTO monsterstats VALUES ('Blozug', 'Ogre', 200, 2, 0.6, 30, 60, 0.1, 30, 60)")
        cursor.execute("INSERT INTO monsterstats VALUES ('Nakorg', 'Ogre', 200, 2, 0.6, 30, 60, 0.1, 30, 60)")
        cursor.execute("INSERT INTO monsterstats VALUES ('Anna Wintour', 'MeanGirl', 100, 7, 0.9, 10, 30, 0.6, 10, 30)")
        cursor.execute("INSERT INTO monsterstats VALUES ('Regina George', 'MeanGirl', 100, 7, 0.9, 10, 30, 0.6, 10, 30)")
        cursor.execute("INSERT INTO monsterstats VALUES ('Joan Crawford', 'MeanGirl', 100, 7, 0.9, 10, 30, 0.6, 10, 30)")
        cursor.execute("INSERT INTO monsterstats VALUES ('Heather Duke', 'MeanGirl', 100, 7, 0.9, 10, 30, 0.6, 10, 30)")
        cursor.execute("INSERT INTO monsterstats VALUES ('Paris Geller', 'MeanGirl', 100, 7, 0.9, 10, 30, 0.6, 10, 30)")
        connection.commit()
        connection.close()

# def monster_spawn():
    #data = cursor.execute("SELECT * FROM monsterstats ORDER BY RANDOM() LIMIT 1")
    #print(data.fetchall())

#monster_spawn()

if __name__ == '__main__':
    m = MonsterDB()
