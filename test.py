from AOC_Helpers import *
import math

def Test(equation):
    print("Ok!" if equation else "Fail!")
    if not equation:
        raise Exception("fail")

vec = Vec3(0, 4)
Test(vec.GetMag() == 4)
Test(Vec3(10,0).Normalized() == Vec3(1.0, 0.0))
Test(Vec3(10,10).Normalized().AlmostEq(Vec3(1, 1) * math.sqrt(0.5)))
Test(Vec3(12, 4) / 4 == Vec3(3,1))
Test(Vec3(123, 0).DistTo(Vec3(3,0)) == 120)
Test(Vec3(10, 0).DirTo(Vec3(3,0)) == Vec3(-1,0))

def PathTest():
    emap = [[0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 1, 0], [0, 1, 1, 1, 1, 0, 0, 0, 1, 0], [0, 0, 0, 0, 1, 0, 0, 0, 1, 0], [0, 1, 1, 0, 1, 1, 1, 0, 1, 0], [0, 1, 0, 0, 0, 0, 0, 0, 1, 0], [0, 1, 0, 0, 0, 0, 0, 0, 1, 0], [0, 1, 0, 0, 0, 0, 0, 0, 1, 0], [0, 1, 0, 0, 0, 0, 0, 0, 1, 0], [0, 1, 0, 0, 0, 0, 0, 0, 1, 0]]
    nodes = CreateNodes(emap, 1)
    result = AStar(nodes[0], nodes[len(nodes) - 1])
    path = result[0]
    cost = result[1]
    validResult = [Vec3(0, 0), Vec3(0, 1), Vec3(0, 2), Vec3(0, 3), Vec3(1, 3), Vec3(2, 3), Vec3(3, 3), Vec3(3, 4), Vec3(3, 5), Vec3(4, 5), Vec3(5, 5), Vec3(6, 5), Vec3(7, 5), Vec3(7, 4), Vec3(7, 3), Vec3(7, 2), Vec3(7, 1), Vec3(7, 0),	Vec3(8, 0),	Vec3(9, 0),	Vec3(9, 1),	Vec3(9, 2),	Vec3(9, 3),	Vec3(9, 4),	Vec3(9, 5), Vec3(9, 6),	Vec3(9, 7),	Vec3(9, 8),	Vec3(9, 9)]
    Test((len(path) - 1) == cost)
    Test(len(path) == len(validResult))
    for i in range(len(path)):
        Test(path[i] == validResult[i])
    
PathTest()

print()
print("All good!")