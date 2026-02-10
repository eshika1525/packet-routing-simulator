class Packet:
    def __init__(self, message_id, seq_num, total_parts, source, destination, content):
        self.message_id = message_id          # Unique ID for the full message
        self.seq_num = seq_num                # Sequence number of this packet
        self.total_parts = total_parts        # Total number of packets in the message
        self.source = source                  # Source router name or IP
        self.destination = destination        # Destination router name or IP
        self.content = content                # Actual content of this part
        self.path = []                        # The path taken by this packet (filled later)

    def __repr__(self):
        return (f"Packet(msg_id={self.message_id}, seq={self.seq_num}/{self.total_parts}, "
                f"from={self.source} to={self.destination}, content='{self.content}')")
