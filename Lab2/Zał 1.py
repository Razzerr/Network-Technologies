from random import randint


def check(interval, vertices, edges):
    def cycle():
        for edge in edges:
            if randint(1, 100) / 100 > edge[3]: edge[2] = False

    for i in range(0, interval): cycle()

    def connectivity(checked, toCheck):
        if len(toCheck) != 0:
            for edge in edges:
                if (edge[0] == toCheck[0]) and edge[2] and (edge[1] not in checked) and (edge[1] not in toCheck):
                    toCheck += [edge[1]]
                elif (edge[1] == toCheck[0]) and edge[2] and (edge[0] not in checked) and (edge[0] not in toCheck):
                    toCheck += [edge[0]]
            checked += [toCheck[0]]
            toCheck.remove(toCheck[0])
            return connectivity(checked, toCheck)
        else:
            if len(checked) == len(vertices):
                return True
            return False

    return connectivity([], [vertices[0]])


def main_a(interval, h):
    vertices = []
    for i in range(0, 20):
        vertices += ['v' + str(i)]
    edges = []
    for i in range(0, 19):
        edges += [[vertices[i], vertices[i + 1], True, h]]

    connected = 0
    for i in range(0, 100000):
        for edge in edges: edge[2] = True
        if check(interval, vertices, edges): connected += 1
    print("\nFor " + str(interval) + " intervals, probability of problem a is: " + str(connected / 100000))


def main_b(interval, h):
    vertices = []
    for i in range(0, 20):
        vertices += ['v' + str(i)]
    edges = []
    for i in range(0, 19):
        edges += [[vertices[i], vertices[i + 1], True, h]]
    edges += [[vertices[19], vertices[0], True, h]]

    connected = 0
    for i in range(0, 100000):
        for edge in edges: edge[2] = True
        if check(interval, vertices, edges): connected += 1
    print("\nFor " + str(interval) + " intervals, probability of problem b is: " + str(connected / 100000))


def main_c(interval, h):
    vertices = []
    for i in range(0, 20):
        vertices += ['v' + str(i)]
    edges = []
    for i in range(0, 19):
        edges += [[vertices[i], vertices[i + 1], True, h]]
    edges += [[vertices[19], vertices[0], True, h]]
    edges += [[vertices[0], vertices[9], True, 0.8]]
    edges += [[vertices[4], vertices[14], True, 0.7]]

    connected = 0
    for i in range(0, 100000):
        for edge in edges: edge[2] = True
        if check(interval, vertices, edges): connected += 1
    print("\nFor " + str(interval) + " intervals, probability of problem c is: " + str(connected / 100000))


def main_d(interval, h):
    vertices = []
    for i in range(0, 20):
        vertices += ['v' + str(i)]
    edges = []
    for i in range(0, 19):
        edges += [[vertices[i], vertices[i + 1], True, h]]
    edges += [[vertices[19], vertices[0], True, h]]
    edges += [[vertices[0], vertices[9], True, 0.8]]
    edges += [[vertices[4], vertices[14], True, 0.7]]

    while len(edges)<26:
        i = randint(0,19)
        j = randint(0,19)
        if i != j:
            edges += [[vertices[i], vertices[j], True, 0.4]]

    connected = 0
    for i in range(0, 100000):
        for edge in edges: edge[2] = True
        if check(interval, vertices, edges): connected += 1
    print("\nFor " + str(interval) + " intervals, probability of problem d is: " + str(connected / 100000))


main_a(1, 0.95)
main_b(1, 0.95)
main_c(1, 0.95)
main_d(1, 0.95)

