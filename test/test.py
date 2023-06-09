from mcpi.minecraft import Minecraft
import mcpi.block as block
import time



def checkHit(mc, treasure_x, treasure_y, treasure_z, exit_x, exit_y, exit_z):
    events = mc.events.pollBlockHits()
    for e in events:
        p = e.pos
        if p.x == treasure_x and p.y == treasure_y and p.z == treasure_z:
            mc.postToChat("Exit is open")
            mc.setBlock(treasure_x, treasure_y, treasure_z, block.AIR.id)
            mc.setBlock(exit_x, exit_y, exit_z, exit_x, exit_y + 2, exit_z, block.AIR.id)


#  подготовка переменных
mc = Minecraft.create()
pos = mc.player.getTitePos()
score = 50


#  переменные с материалами блоков
GAP = block.AIR.id
WALL = block.GOLD_BLOCK.id
FLOOR = block.GRASS.id
TREASURE = block.DIAMOND_BLOCK.id




#  координаты начала зоны с лабиринтом
x1 = pos.x + 1
y = pos.y
z1 = pos.z +1

#  открытие файла с лабиринтом
FILENAME = "maze.csv"
f = open(FILENAME, "r")


#  строительство лабиринта
z = z1
for line in f.readlines():
    data = line.split(",")
    x = x1
    for cell in data:
        a = FLOOR
        b = GAP
        if  cell == "0":
            b = GAP
        elif cell == "9":
            start_x = x
            start_z = z
        elif cell == "2":
            treasure_x = x
            treasure_y = y
            treasure_z = z
            b = GAP
        elif cell == "3":
            exit_x = x
            exit_y = y
            exit_z = z
            b = WALL
            a = FLOOR
        else:
            b = WALL
        mc.setBlock(x, y, z, b)
        mc.setBlock(x, y + 1, z, b)
        mc.setBlock(x, y - 1, z, a)
        x += 1
    z += 1
z2 = z
x2 = x

mc.setBlock(treasure_x, treasure_y, treasure_z, block.DIAMOND_BLOCK.id)
mc.player.setPos(start_x, y, start_z)

# основной цикл
while score != 0:
    time.sleep(1)
    checkHit(mc, treasure_x, treasure_y, treasure_z, exit_x, exit_y, exit_z)
    pos = mc.player.getTitePos()
    if pos.x >= x1 and pos.x <= x2 and pos.z >= z1 and pos.z <= z2:
        score -= 1
        mc.postToChat("score = " + str(score))
    else:
        mc.postToChat("WE WIN")
        break
mc.postToChat("GAME OVER")


