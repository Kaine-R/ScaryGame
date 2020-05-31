from Block import Block


def generateMap(gameMap):
    for i in range(10):
        block = Block("roof", (i*50, 25))
        gameMap.append(block)
    for i in range(10):
        block = Block("wall", (i*50, 50))
        gameMap.append(block)
    for i in range(10):
        block = Block("tile", (i*50, 100))
        gameMap.append(block)
