import matplotlib.pyplot as plt
import networkx as nx

# Enable interactive mode for live updates
plt.ion()

def show_graph_animation(network, path, dest, delay=0.8):
    # Use static figure and axis to avoid multiple windows
    if not hasattr(show_graph_animation, "fig"):
        show_graph_animation.fig, show_graph_animation.ax = plt.subplots(figsize=(8, 6))
    
    fig = show_graph_animation.fig
    ax = show_graph_animation.ax
    ax.clear()

    # Create a NetworkX graph from router connections
    G = nx.Graph()
    for router in network.routers.values():
        for neighbor, cost in router.neighbors.items():
            G.add_edge(router.name, neighbor, weight=cost)

    # Graph layout for consistent positioning
    pos = nx.spring_layout(G, seed=42)

    # Labels with both name and IP address
    labels = {
        router.name: f"{router.name}\n{router.ip_address}"
        for router in network.routers.values()
    }

    # Draw the full network
    nx.draw(G, pos, ax=ax, node_color='lightblue', node_size=1200)
    nx.draw_networkx_labels(G, pos, labels, ax=ax, font_size=9)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

    # Animate packet movement edge by edge
    for i in range(len(path) - 1):
        edge = [(path[i], path[i + 1])]
        nx.draw_networkx_edges(G, pos, edgelist=edge, edge_color='red', width=3, ax=ax)
        ax.set_title(f"Packet hopping: {path[i]} → {path[i + 1]}")
        fig.canvas.draw_idle()
        plt.pause(delay)

    # Highlight the destination node
    nx.draw_networkx_nodes(G, pos, nodelist=[dest], node_color='green', node_size=1400, ax=ax)
    ax.set_title(f"Packet reached destination: {dest}")
    fig.canvas.draw_idle()
    plt.pause(delay * 2)
