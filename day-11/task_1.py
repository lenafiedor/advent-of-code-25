FILENAME = 'input.txt'


def parse_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        graph = {}

        for line in lines:
            input = line.split(':')[0]
            outputs = line.split(':')[1].split()
            graph[input] = outputs
    
    return graph


def construct_paths(graph, start, goal):
    paths = []

    def dfs(u, path):
        if u == goal:
            paths.append(path.copy())
        for v in graph.get(u, []):
            dfs(v, path + [v])
    
    dfs(start, [start])
    return paths


if __name__ == '__main__':
    graph = parse_input(FILENAME)
    paths = construct_paths(graph, "svr", "out")

    for p in paths:
        print(" -> ".join(p))
    print("count:", len(paths)) # 788
