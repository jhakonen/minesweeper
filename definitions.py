# enum declaration from http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
def enum(**enums):
    return type('Enum', (), enums)

Difficulty = enum(EASY=1, MEDIUM=2, HARD=3)

MouseButton = enum(LEFT=1, RIGHT=3)
