from collections import defaultdict, deque
from functools import lru_cache

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


def reverse_graph(graph):
    rev = defaultdict(list)
    for u, vs in graph.items():
        for v in vs:
            rev[v].append(u)
    return rev


def reachable_to_target(graph, target: str):
    """Nodes that can reach target (reverse BFS)."""
    rev = reverse_graph(graph)
    can = set([target])
    q = deque([target])
    while q:
        x = q.popleft()
        for p in rev.get(x, []):
            if p not in can:
                can.add(p)
                q.append(p)
    return can


def detect_cycle_in_subgraph(graph, nodes_subset):
    """Cycle detection in induced subgraph."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {u: WHITE for u in nodes_subset}

    def dfs(u):
        color[u] = GRAY
        for v in graph.get(u, []):
            if v not in nodes_subset:
                continue
            if color[v] == GRAY:
                return True
            if color[v] == WHITE and dfs(v):
                return True
        color[u] = BLACK
        return False

    for u in nodes_subset:
        if color[u] == WHITE:
            if dfs(u):
                return True
    return False


def count_paths_with_fft_and_dac(graph, start="svr", goal="out", req1="fft", req2="dac"):
    can_reach_goal = reachable_to_target(graph, goal)
    if start not in can_reach_goal:
        return 0

    can_reach_fft = reachable_to_target(graph, req1)
    can_reach_dac = reachable_to_target(graph, req2)

    reachable_from_start = set()
    q = deque([start])
    reachable_from_start.add(start)
    while q:
        u = q.popleft()
        for v in graph.get(u, []):
            if v in can_reach_goal and v not in reachable_from_start:
                reachable_from_start.add(v)
                q.append(v)
    relevant = reachable_from_start

    if detect_cycle_in_subgraph(graph, relevant):
        raise ValueError('Graph contains a cycle on the svr→out relevant subgraph; path counting is ill-defined or expensive.')

    def bit_for(node):
        if node == req1:
            return 1
        if node == req2:
            return 2
        return 0

    @lru_cache(None)
    def dp(u, mask):
        if u == goal:
            return 1 if (mask == 3) else 0
        total = 0
        for v in graph.get(u, []):
            if v not in relevant:
                continue
            if (mask & 1) == 0 and v not in can_reach_fft:
                continue
            if (mask & 2) == 0 and v not in can_reach_dac:
                continue
            total += dp(v, mask | bit_for(v))
        return total

    start_mask = bit_for(start)
    return dp(start, start_mask)

if __name__ == '__main__':
    graph = parse_input(FILENAME)
    path_count = count_paths_with_fft_and_dac(graph, start='svr', goal='out', req1='fft', req2='dac')
    print(f'Count: {path_count}') # 316291887968000
