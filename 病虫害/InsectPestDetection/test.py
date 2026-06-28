import heapq


def dijkstra(graph, start, end):
    # 初始化距离字典（存储到各点的最短距离）
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    # 初始化优先队列（存储(距离, 节点)元组）
    priority_queue = [(0, start)]

    # 初始化路径字典（存储最短路径中每个节点的前驱节点）
    previous_nodes = {node: None for node in graph}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # 如果找到终点，提前退出
        if current_node == end:
            break

        # 遍历相邻节点
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            # 如果找到更短路径
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    # 回溯构建最短路径
    path = []
    current = end
    while previous_nodes[current] is not None:
        path.insert(0, current)
        current = previous_nodes[current]
    path.insert(0, start)

    return path, distances[end]


# 示例图（有向图）
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

# 测试路径查找
start_node = 'A'
end_node = 'D'

path, distance = dijkstra(graph, start_node, end_node)

print(f"最短路径从 {start_node} 到 {end_node}:")
print("路径:", " → ".join(path))
print("总距离:", distance)