import math
from collections import defaultdict

class Vec3:
    def __init__(self, x, y, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def GetSqrMag(self):
        return self.x * self.x + self.y * self.y + self.z * self.z

    def GetMag(self):
        return math.sqrt(self.GetSqrMag())

    def Normalize(self):
        mag = self.GetMag()
        if mag > 0:
            self.x /= mag
            self.y /= mag
            self.z /= mag

    def SqrDistTo(self, other):
        return (other - self).GetSqrMag()

    def DistTo(self, other):
        return (other - self).GetMag()

    def DirTo(self, other):
        return (other - self).Normalized()

    def Normalized(self):
        vec = Vec3(self.x, self.y, self.z)
        vec.Normalize()
        return vec

    def AlmostEq(self, other, margin = 0.001):
        return abs(self.x - other.x) < margin and abs(self.y - other.y) < margin and (self.z - other.z) < margin 

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __truediv__(self, scalar):
        return self * (1 / scalar)

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(repr(self))

inf = math.inf

class PathConnection:
    def __init__(self, node, cost = 1):
        self.node = node
        self.cost = cost

class PathNode:
    def __init__(self, pos, connections = []):
        self.pos = pos
        self.connections = connections.copy()

def CreateNodes(emap, wallChar):
    nodes = []
    for y in range(len(emap)):
        for x in range(len(emap[0])):
            if emap[y][x] != wallChar:
                node = PathNode(Vec3(x,y))
                neighbors = []
                if y > 0 and emap[y - 1][x] == 0:
                    neighbors.append(PathNode(Vec3(x,y-1)))
                if y < len(emap) - 1 and emap[y + 1][x] == 0:
                    neighbors.append(PathNode(Vec3(x,y+1)))
                if x > 0 and emap[y][x-1] == 0:
                    neighbors.append(PathNode(Vec3(x-1,y)))
                if x < len(emap[0]) - 1 and emap[y][x+1] == 0:
                    neighbors.append(PathNode(Vec3(x+1,y)))
                for neighbor in neighbors:
                    for n in nodes:
                        if n.pos == neighbor.pos:    
                            node.connections.append(PathConnection(n))
                            n.connections.append(PathConnection(node))
                            break
                nodes.append(node)
    return nodes

def DefaultHeuristic(start, end):
    return start.pos.SqrDistTo(end.pos)

def AStar(startNode, goalNode, heuristic = DefaultHeuristic):
    openSet = {startNode}
    cameFrom = dict()
    def ReturnInf():
        return inf
    gScore = defaultdict(ReturnInf)
    gScore[startNode] = 0

    fScore = defaultdict(ReturnInf)
    fScore[startNode] = heuristic(startNode, goalNode)

    while len(openSet) > 0:
        minVal = inf
        current = None
        for node in openSet:
            if fScore[node] <= minVal:
                minVal = fScore[node]
                current = node
        if current == goalNode:
            path = [current]
            while current in cameFrom.keys():
                current = cameFrom[current]
                path.append(current)
            path.reverse()
            return [[x.pos for x in path], minVal]
        openSet.remove(current)
        for connection in current.connections:
            score = gScore[current] + connection.cost
            neighbor = connection.node
            if score < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = score
                fScore[neighbor] = score + heuristic(neighbor, goalNode)
                openSet.add(neighbor)
    return []

class Range:
    def __init__(self, start = inf, end = -inf):
        self.start = start
        self.end = end
        
    def __eq__(self, other):
        return self.start == other.start and self.end == other.end
        
    def IsValid(self):
        return self.start <= self.end
    
    def Intersects(self, other):
        return self.ContainsValue(other.start) or self.ContainsValue(other.end)
    
    def Contains(self, other):
        return other.start >= self.start and other.end <= self.end

    def ContainsValue(self, value):
        return value >= self.start and value <= self.end

    def Inverted(self):
        if not self.IsValid():
            return [Range(-inf, inf)]
        return [Range(-inf, self.start), Range(self.end, inf)]

    def GetUnion(self, other):
        if (not other.IsValid()) or self.Contains(other):
            return [self]
        
        if (not self.IsValid()) or other.Contains(self):
            return [other]

        if self.start < other.start:
            first = self
            second = other
        else:
            first = other
            second = self
            
        if self.Intersects(other):
            return [Range(first.start, second.end)]

        return [Range(first.start, first.end), Range(second.start, second.end)]
        
    def GetIntersection(self, other):
        if not self.Intersects(other):
            return Range()
        
        return Range(max(self.start, other.start), min(self.end, other.end))

    def Remove(self, other):
        if not self.Intersects(other):
            return [self]

        intersection = self.GetIntersection(other)
        l = Range(self.start, intersection.start - 1)
        r = Range(intersection.end + 1, self.end)
        
        results = []
        if l.IsValid():
            results.append(l)
        if r.IsValid() or len(results) == 0:
            results.append(r)
        return results