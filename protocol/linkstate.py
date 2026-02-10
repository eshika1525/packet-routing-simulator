import heapq

class LinkState:
    def compute_routing_table(self, start, routers):
        distances = {r: float('inf') for r in routers}
        previous = {}
        distances[start] = 0
        pq = [(0, start)]

        while pq:
            curr_dist, current = heapq.heappop(pq)
            if curr_dist > distances[current]:
                continue  # Skip outdated entry

            for neighbor, cost in routers[current].neighbors.items():
                distance = curr_dist + cost
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current
                    heapq.heappush(pq, (distance, neighbor))

        table = {}
        for dest in routers:
            if dest == start:
                continue
            path = []
            at = dest
            while at in previous:
                path.append(at)
                at = previous[at]
            if at == start:
                path.append(start)
                path.reverse()
                # next hop is the second node in path
                table[dest] = (path[1], distances[dest])
        return table
