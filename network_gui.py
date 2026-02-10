import tkinter as tk
from tkinter import ttk, messagebox
from network.network import Network
from visual.graph import show_graph_animation


class NetworkSimulatorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Network Routing Simulator")
        self.network = Network()
        self.running = True  # Check if GUI is active

        self.build_gui()
        self.setup_sample_topology()

        self.master.protocol("WM_DELETE_WINDOW", self.on_close)  # handle close properly

    def build_gui(self):
        input_frame = ttk.Frame(self.master, padding="10")
        input_frame.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(input_frame, text="Source:").pack(side=tk.LEFT)
        self.source_entry = ttk.Entry(input_frame, width=5)
        self.source_entry.pack(side=tk.LEFT, padx=5)

        ttk.Label(input_frame, text="Destination:").pack(side=tk.LEFT)
        self.dest_entry = ttk.Entry(input_frame, width=5)
        self.dest_entry.pack(side=tk.LEFT, padx=5)

        ttk.Label(input_frame, text="Message:").pack(side=tk.LEFT)
        self.msg_entry = ttk.Entry(input_frame, width=20)
        self.msg_entry.pack(side=tk.LEFT, padx=5)

        send_btn = ttk.Button(input_frame, text="Send Message", command=self.send_packet)
        send_btn.pack(side=tk.LEFT, padx=10)

        show_table_btn = ttk.Button(input_frame, text="Show Routing Tables", command=self.show_routing_tables)
        show_table_btn.pack(side=tk.LEFT, padx=5)

        self.output = tk.Text(self.master, height=200, width=800)
        self.output.pack(padx=10, pady=10)

    def setup_sample_topology(self):
        for name in ['A', 'B', 'C', 'D', 'E']:
            self.network.add_router(name)
        self.network.add_link('A', 'B', 1)
        self.network.add_link('B', 'C', 2)
        self.network.add_link('C', 'D', 1)
        self.network.add_link('D', 'E', 3)
        self.network.add_link('A', 'E', 10)
        self.network.add_link('B', 'D', 4)
        self.network.propagate_updates()

    def send_packet(self):
        source = self.source_entry.get().strip().upper()
        dest = self.dest_entry.get().strip().upper()
        message = self.msg_entry.get().strip()

        if source not in self.network.routers or dest not in self.network.routers:
            self.safe_output("❌ Error: Invalid source or destination.\n")
            return

        self.run_simulation(source, dest, message)

    def run_simulation(self, source, dest, message):
        self.safe_output(f"\n--- Sending Message from {source} to {dest} ---\n")
        packets = self.network.simulate_message(source, dest, message)

        received_content = {}  # key = seq_num, value = content

        for packet in packets:
            if not self.running:
                return
            self.safe_output(f"📦 Sending {packet} via path: {' -> '.join(packet.path)}\n")
            show_graph_animation(self.network, packet.path, dest)
            received_content[packet.seq_num] = packet.content

        # Reassemble message in order
        reassembled = ''.join(received_content[i] for i in sorted(received_content.keys()))
        self.safe_output(f"\n✅ Reassembled Message at {dest}: \"{reassembled}\"\n")
        self.safe_output(f"✅ Message (ID: {packets[0].message_id}) sent in {len(packets)} packets.\n")


    def show_routing_tables(self):
        if not self.running:
            return
        self.safe_output("\n=== 📡 Routing Tables ===\n")
        for router in self.network.routers.values():
            self.safe_output(f"\nRouter {router.name} ({router.ip_address}):\n")
            for dest, (next_hop, cost) in router.routing_table.items():
                self.safe_output(f"  To {dest} via {next_hop} | Cost: {cost}\n")

    def safe_output(self, text):
        try:
            if self.output and self.output.winfo_exists():
                self.output.insert(tk.END, text)
                self.output.see(tk.END)
        except tk.TclError:
            pass  # GUI was likely closed during animation

    def on_close(self):
        self.running = False
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkSimulatorApp(root)
    root.mainloop()
