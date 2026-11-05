class Graph:
    def __init__(self, n, m, r, s, t):
        self.V = int[n]
        self.E = int[m]
        self.R = int[r]
        self.s = s
        self.t = t

class Vertex:
    def __init__(self, name, isRed)