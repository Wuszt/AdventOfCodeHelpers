from AOC_Helpers import *
import math

counter = 0

def Test(equation):
    print("Ok!" if equation else "Fail!")
    if not equation:
        raise Exception("fail")
    global counter
    counter += 1

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

Test(not Range(10, 2).IsValid())

Test(Range(0, 2).ContainsValue(0))
Test(Range(0, 2).ContainsValue(1))
Test(Range(0, 2).ContainsValue(2))
Test(not Range(0, 2).ContainsValue(5))

Test(Range(0, 5).Contains(Range(0, 0)))
Test(Range(0, 5).Contains(Range(1, 4)))
Test(Range(0, 5).Contains(Range(5, 5)))
Test(not Range(0, 5).Contains(Range(3, 6)))

Test(Range(0, 5).Intersects(Range(0, 0)))
Test(Range(0, 5).Intersects(Range(1, 4)))
Test(Range(0, 5).Intersects(Range(5, 5)))
Test(Range(0, 5).Intersects(Range(3, 10)))
Test(not Range(0, 5).Intersects(Range(6, 10)))
Test(not Range().Intersects(Range()))

Test(Range(0, 5).GetIntersection(Range(0, 0)) == Range(0,0))
Test(Range(0, 5).GetIntersection(Range(1, 4)) == Range(1,4))
Test(Range(0, 5).GetIntersection(Range(5, 5)) == Range(5,5))
Test(Range(0, 5).GetIntersection(Range(3, 10)) == Range(3,5))
Test(not Range(0, 5).GetIntersection(Range(6, 10)).IsValid())
Test(not Range().GetIntersection(Range()).IsValid())

Test(len(Range(0, 5).GetUnion(Range(0, 5))) == 1)
Test(Range(0, 5).GetUnion(Range(0, 5))[0] == Range(0, 5))

Test(len(Range(0, 5).GetUnion(Range(0, 5))) == 1)
Test(Range(0, 5).GetUnion(Range(5, 5))[0] == Range(0, 5))

Test(len(Range(0, 5).GetUnion(Range(5, 10))) == 1)
Test(Range(0, 5).GetUnion(Range(5, 10))[0] == Range(0, 10))

Test(len(Range(0, 5).GetUnion(Range(8, 10))) == 2)
Test(Range(0, 5).GetUnion(Range(8, 10))[0] == Range(0, 5))
Test(Range(0, 5).GetUnion(Range(8, 10))[1] == Range(8, 10))

Test(len(Range().GetUnion(Range())) == 1)
Test(not Range().GetUnion(Range())[0].IsValid())

Test(len(Range(0, 5).Remove(Range(0, 5))) == 1)
Test(not Range(0, 5).Remove(Range(0, 5))[0].IsValid())

Test(len(Range(0, 5).Remove(Range(0, 5))) == 1)
Test(Range(0, 5).Remove(Range(5, 5))[0] == Range(0, 4))

Test(len(Range(0, 5).Remove(Range(5, 10))) == 1)
Test(Range(0, 5).Remove(Range(5, 10))[0] == Range(0, 4))

Test(len(Range(0, 5).Remove(Range(6, 10))) == 1)
Test(not Range(0, 5).Remove(Range(6, 10))[0] == Range(0.5))

Test(len(Range(0, 5).Remove(Range(2, 2))) == 2)
Test(Range(0, 5).Remove(Range(2, 2))[0] == Range(0, 1))
Test(Range(0, 5).Remove(Range(2, 2))[1] == Range(3, 5))

print()
print("All " + str(counter) + " tests succeeded!")