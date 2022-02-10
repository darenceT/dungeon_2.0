from Maze import Maze


# obtain map, obtain entrance coords for player starting loc, create feed for mini map
m = Maze()
print(m.ingress.coords)
mini_map = m.str().replace('\n', '').strip() 
print(mini_map)

'''
map2 = ("""
+-----+-----+-----+-----+
|     |     =     | O   |
+--H--+-----+--H--+--H--+
|     =     =     =     |
+-----+-----+-----+--H--+
|     =     |     =     |
+-----+--H--+-----+--H--+
| i   =     =     =     |
+-----+-----+-----+-----+
""")
map1 = (
'+-----+-----+-----+-----+'
'|     |     =     | O   |'
'+--H--+-----+--H--+--H--+'
'|     =     =     =     |'
'+-----+-----+-----+--H--+'
'|     =     |     =     |'
'+-----+--H--+-----+--H--+'
'| i   =     =     =     |'
'+-----+-----+-----+-----+'
)
c = ''.join(map2.splitlines())  # alternate method
d = map2.replace('\n', '').strip() # preferred
created_dungeon = Maze(map_str=map2)

print(created_dungeon.ingress.coords)
print(map1 == d)
'''