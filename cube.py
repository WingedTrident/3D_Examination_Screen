#cubes hitboxes
hitboxes = {
    "blue": [[1,1,1],[1,1,-1],[-1,1,-1],[-1,1,1]],
    "yellow": [[1,1,1],[1,-1,1],[1,1,-1],[1,-1,-1]],
    "green": [[-1,1,1],[-1,-1,1],[-1,1,-1],[-1,-1,-1]],
    "teal": [[-1,1,1],[1,1,1],[-1,-1,1],[1,-1,1]],
    "red": [[-1,-1,1],[1,-1,1],[-1,-1,-1],[1,-1,-1]],
    "pink": [[-1,1,-1],[1,1,-1],[1,-1,-1],[-1,-1,-1]],
}

#cubes vertices
vertices= (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

#cubes edges
edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

#cubes colors values
colors = (
    (1,0,0,1),
    (0,.5,0,1),
    (0,0,1,1),
    (1,1,0,1),
    (0,1,1,1),
    (1,0,1,1),
    )

#cubes surfaces
surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )