from random import randint

vertices = range(1, 11)
petersenEdges = [(1, 2), (1, 5), (1, 7), (2, 8), (2, 3), (3, 9), (3, 4), (4, 10), (4, 5), (5, 6), (6, 9), (6, 8),
                 (7, 9), (7, 10), (8, 10)]
circleEdges = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (2, 10), (2, 3), (3, 4), (4, 5),
               (5, 6),
               (6, 7), (7, 8), (8, 9), (9, 10)]

N = [[0, 10, 10, 10, 10, 10, 10, 10, 10, 10],
     [10, 0, 10, 10, 10, 10, 10, 10, 10, 10],
     [10, 10, 0, 10, 10, 10, 10, 10, 10, 10],
     [10, 10, 10, 0, 10, 10, 10, 10, 10, 10],
     [10, 10, 10, 10, 0, 10, 10, 10, 10, 10],
     [10, 10, 10, 10, 10, 0, 10, 10, 10, 10],
     [10, 10, 10, 10, 10, 10, 0, 10, 10, 10],
     [10, 10, 10, 10, 10, 10, 10, 0, 10, 10],
     [10, 10, 10, 10, 10, 10, 10, 10, 0, 10],
     [10, 10, 10, 10, 10, 10, 10, 10, 10, 0]
     ]

cP = 64000
cIn = 90240
cOut = 13440

cPetersen = [[[1, 2], cP], [[1, 5], cP], [[1, 7], cP], [[2, 8], cP], [[2, 3], cP], [[3, 9], cP], [[3, 4], cP],
             [[4, 10], cP], [[4, 5], cP], [[5, 6], cP], [[6, 9], cP], [[6, 8], cP], [[7, 9], cP], [[7, 10], cP],
             [[8, 10], cP]]
cCircle = [[[1, 2], cIn], [[1, 3], cIn], [[1, 4], cIn], [[1, 5], cIn], [[1, 6], cIn], [[1, 7], cIn], [[1, 8], cIn],
           [[1, 9], cIn], [[1, 10], cIn], [[2, 10], cOut], [[2, 3], cOut], [[3, 4], cOut], [[4, 5], cOut],
           [[5, 6], cOut], [[6, 7], cOut], [[7, 8], cOut], [[8, 9], cOut], [[9, 10], cOut]]


class Edge:
    def __init__(self, v1, v2):
        self.vertices = [v1, v2]
        self.packets = 0


class Graph:
    def __init__(self, V, E, type):
        self.id = type
        self.vertices = []
        self.edges = []
        self.tempPaths = []
        self.paths = {}
        for v in V:
            self.vertices += [v]
        for e in E:
            self.edges += [Edge(e[0], e[1])]
        self.shortestPaths()
        self.addPackets()

    def shortestPaths(self):
        self.paths = {}
        for v in self.vertices:
            for w in self.vertices:
                if v != w:
                    s = min(v, w)
                    b = max(v, w)
                    name = str(s) + 'to' + str(b)
                    if name not in self.paths:
                        self.paths[str(s) + 'to' + str(b)] = self.shortestPath(v, w)

    def shortestPath(self, v, w):
        self.tempPaths = []
        for e in self.edges:
            if v in e.vertices:
                if w in e.vertices:
                    return [e]
                self.tempPaths += [[[v, [x for x in e.vertices if x != v][0]], [e]]]
        return self.shortestPathX(w)

    def shortestPathX(self, w):
        paths = list(self.tempPaths)
        self.tempPaths = []
        if len(paths) == 0:
            return None
        for p in paths:
            for e in self.edges:
                v = p[0][len(p[0]) - 1]
                if v in e.vertices:
                    if w in e.vertices:
                        return p[1] + [e]
                    u = [x for x in e.vertices if x != v]
                    if u[0] not in p[0]:
                        self.tempPaths += [[p[0] + u, p[1] + [e]]]
        return self.shortestPathX(w)

    def addPackets(self):
        for i in range(0, 10):
            for j in range(0, 10):
                if i != j:
                    s = min(i, j)
                    b = max(i, j)
                    for e in self.paths[str(s + 1) + 'to' + str(b + 1)]:
                        e.packets += N[i][j]


petersen = Graph(vertices, petersenEdges, 'p')
circle = Graph(vertices, circleEdges, 'c')

def avgDelayPetersen():
    G = 0
    SUM_e = 0
    m = 64

    for i in N:
        for j in i:
            G += j

    for e in petersen.edges:
        for c in cPetersen:
            if e.vertices == c[0]:
                SUM_e += e.packets / (c[1] / m - e.packets)

    return (1 / G) * SUM_e

def avgDelayCircle():
    G = 0
    SUM_e = 0
    m = 64

    for i in N:
        for j in i:
            G += j

    for e in circle.edges:
        for c in cCircle:
            if e.vertices == c[0]:
                SUM_e += e.packets / (c[1] / m - e.packets)

    return (1 / G) * SUM_e


T_MAX = 0.75
p = 0.5

def checkIntegrity(graph, cycles):
    global T_MAX
    def cycle():
        global p
        for i in range(0, len(graph.edges)):
            if randint(1, 100) / 100 > p:
                graph.edges[i] = False
        graph.edges = [x for x in graph.edges if x!= False]
    for i in range(0, cycles):
        cycle()
    graph.shortestPaths()
    for p in graph.paths:
        if graph.paths[p] == None:
            return False
    if graph.id == 'p':
        if avgDelayPetersen() > T_MAX:
            return False
    if graph.id == 'c':
        if avgDelayCircle() > T_MAX:
            return False
    return True

resultPetersen = ''
resultCircle = ''

def checkIntegrityS():
    circleIntegrity = 0
    petersenIntegrity = 0
    for i in range(0, 1000):
        petersen = Graph(vertices, petersenEdges, 'p')
        circle = Graph(vertices, circleEdges, 'c')
        if checkIntegrity(petersen, 1): petersenIntegrity+=1
        if checkIntegrity(circle, 1): circleIntegrity+=1
    return [str(petersenIntegrity/10), str(circleIntegrity/10)]

for i in range(2, 10):
    p = 0.8
    T_MAX = i/100
    res = checkIntegrityS()
    resultPetersen += str(T_MAX) + ',' + res[0] + '\n'
    resultCircle += str(T_MAX) + ',' + res[1]+ '\n'

print(resultPetersen)
print(resultCircle)