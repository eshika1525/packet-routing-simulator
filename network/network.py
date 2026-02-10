from network.router import Router
import time
from network.packet import Packet

class Network:
    def __init__(self):
        self.routers = {}

    def add_router(self, name, ip_address=None):
        if name not in self.routers:
            if ip_address is None:
                ip_address = f"192.168.1.{len(self.routers) + 1}"
            self.routers[name] = Router(name, ip_address)

    def add_link(self, r1, r2, cost):
        self.routers[r1].add_neighbor(r2, cost)
        self.routers[r2].add_neighbor(r1, cost)

    def propagate_updates(self):
        for router in self.routers.values():
            router.update_routing_table(self.routers)

    def simulate_packet(self, src, dst):
        path = []
        current = src
        while current != dst:
            path.append(current)
            next_hop = self.routers[current].routing_table.get(dst, (None,))[0]
            if not next_hop:
                break
            current = next_hop
        path.append(dst)
        return type("Packet", (), {"path": path})()

    def simulate_message(self, source, dest, message, part_size=5):
        parts = [message[i:i+part_size] for i in range(0, len(message), part_size)]
        message_id = int(time.time())
        packets = []
        for i, part in enumerate(parts):
            packet = Packet(message_id, i + 1, len(parts), source, dest, part)
            packet.path = self.simulate_packet(source, dest).path
            packets.append(packet)
        return packets

    def route_packet(self, src, dst):
        path = []
        current = src
        while current != dst:
            path.append(current)
            next_hop = self.routers[current].routing_table.get(dst, (None,))[0]
            if not next_hop:
                break
            current = next_hop
        path.append(dst)
        return path
