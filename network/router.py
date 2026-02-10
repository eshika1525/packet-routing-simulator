from protocol.linkstate import LinkState

class Router:
    def __init__(self, name, ip_address=None):
        self.name = name
        self.ip_address = ip_address or f"192.168.1.{ord(name) - 64}"  # A->1, B->2 ...
        self.neighbors = {}  # {neighbor_name: cost}
        self.routing_table = {}  # {destination: (next_hop, cost)}

    def add_neighbor(self, neighbor_name, cost):
        self.neighbors[neighbor_name] = cost

    def update_routing_table(self, routers):
        link_state = LinkState()
        new_table = link_state.compute_routing_table(self.name, routers)
        updated = new_table != self.routing_table
        self.routing_table = new_table
        return updated
