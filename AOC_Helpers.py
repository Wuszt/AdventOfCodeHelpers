import math
from collections import defaultdict
import heapq

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
        return hash((self.x, self.y, self.z))

inf = math.inf

class PathConnection:
    def __init__(self, node, cost = 1):
        self.node = node
        self.cost = cost

class PathNode:
    def __init__(self, pos, connections = [], userData = None, enabled = True):
        self.pos = pos
        self.connections = connections.copy()
        self.userData = userData
        self.enabled = enabled
        
class QueueNode():
    def __init__(self, score, node):
        self.score = score
        self.node = node
        self.valid = True

    def __lt__(self, other):
        return self.score < other.score

def CreateNodes(emap, wallChar):
    nodes = dict()
    for y in range(len(emap)):
        for x in range(len(emap[0])):
            if emap[y][x] != wallChar:
                node = PathNode(Vec3(x,y))
                neighbors = []
                if y > 0 and emap[y - 1][x] != wallChar:
                    neighbors.append(PathNode(Vec3(x,y-1)))
                if y < len(emap) - 1 and emap[y + 1][x] != wallChar:
                    neighbors.append(PathNode(Vec3(x,y+1)))
                if x > 0 and emap[y][x-1] != wallChar:
                    neighbors.append(PathNode(Vec3(x-1,y)))
                if x < len(emap[0]) - 1 and emap[y][x+1] != wallChar:
                    neighbors.append(PathNode(Vec3(x+1,y)))
                for neighbor in neighbors:
                    if neighbor.pos in nodes:
                        n = nodes[neighbor.pos] 
                        node.connections.append(PathConnection(n))
                        n.connections.append(PathConnection(node))
                nodes[node.pos] = node
    return list(nodes.values())

def EuclideanHeuristic(start, end):
    return start.pos.SqrDistTo(end.pos)

def ManhattanHeuristic(start, end):
    return abs(start.pos.x - end.pos.x) + abs(start.pos.y - end.pos.y)

class PathFindingResult:
    def __init__(self, path, cost):
        self.poses = [x.pos for x in path]
        self.cost = cost
        self.nodes = path
        
    def IsValid(self):
        return len(self.poses) > 0

def PrintGrid(grid, path : PathFindingResult = PathFindingResult([], inf)):
    for y in range(len(grid)):
        line = []
        for x in range(len(grid[y])):
            if Vec3(x,y) in path.poses:
                line.append('X')
            else:
                line.append(grid[y][x])
        print(''.join(line))

def AStar(startNode, goalNode, heuristic = ManhattanHeuristic, maxLength = inf):
    cameFrom = dict()
    def ReturnInf():
        return inf
    gScore = defaultdict(ReturnInf)
    gScore[startNode] = 0

    fScore = defaultdict(ReturnInf)
    fScore[startNode] = heuristic(startNode, goalNode)
    
    openQueue = [QueueNode(fScore[startNode], startNode)]
    openSet = dict()
    openSet[startNode] = openQueue[0]

    while len(openSet) > 0:
        queueNode = heapq.heappop(openQueue)
        while len(openQueue) > 0 and not queueNode.valid:
            queueNode = heapq.heappop(openQueue)

        current = queueNode.node
        minVal = queueNode.score
        if current == goalNode:
            path = [current]
            while current in cameFrom.keys():
                current = cameFrom[current]
                path.append(current)
            path.reverse()
            return PathFindingResult(path, minVal)
        del openSet[current]
        for connection in current.connections:
            if connection.node.enabled:
                score = gScore[current] + connection.cost
                if score <= maxLength:
                    neighbor = connection.node
                    if score < gScore[neighbor]:
                        cameFrom[neighbor] = current
                        gScore[neighbor] = score
                        fScore[neighbor] = score + heuristic(neighbor, goalNode)
                        
                        if neighbor in openSet:
                            openSet[neighbor].valid = False
                        newNode = QueueNode(fScore[neighbor], neighbor)
                        openSet[neighbor] = newNode
                        heapq.heappush(openQueue, newNode)
                        
    return PathFindingResult([],inf)

class DijkstraResult:
    def __init__(self, dists, prevs):
        self.dists = dists
        self.prevs = prevs

    def GetPathTo(self, end):
        path = []
        cost = self.dists[end]
        while end in self.prevs:
            path.append(end)
            end = self.prevs[end]
            if self.dists[end] == 0:
                path.append(end)
                path.reverse()
                return PathFindingResult(path, cost)

        return PathFindingResult([], inf)

def Dijkstra(nodes, start):
    def ReturnInf():
        return inf

    prevs = dict()
    dists = defaultdict(ReturnInf)
    openQueue = []
    openSet = dict()

    dists[start] = 0
    
    for node in nodes:
        queueNode = QueueNode(inf, node)
        openQueue.append(queueNode)
        openSet[node] = queueNode
    
    while len(openSet) > 0:        
        queueNode = heapq.heappop(openQueue)
        while len(openQueue) > 0 and not queueNode.valid:
            queueNode = heapq.heappop(openQueue)

        current = queueNode.node
        minVal = queueNode.score
        del openSet[current]
        
        for connection in current.connections:
            if not connection.node in openSet:
                continue
            alt = dists[current] + connection.cost
            if alt < dists[connection.node]:
                dists[connection.node] = alt
                openSet[connection.node].valid = False
                newNode = QueueNode(alt, connection.node)
                heapq.heappush(openQueue, newNode)
                openSet[connection.node] = newNode
                prevs[connection.node] = current
    return DijkstraResult(dists, prevs)
                

class Range:
    def __init__(self, start = inf, end = -inf):
        self.start = start
        self.end = end
        
    def __eq__(self, other):
        return self.start == other.start and self.end == other.end
    
    def __str__(self):
        if not self.IsValid():
            return "<invalid>"
        return "<" + str(self.start) + "," + str(self.end) + ">"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(repr(self))
        
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