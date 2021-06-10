# receiver
from socket import *
import matplotlib.pyplot as plt
import numpy as np

# UDP Parameters
buffer_size = 2048
server_port = 12501

# UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', server_port))

Last_correctly_received_id = -1
packets_data = []
received_IDs = []
while True:
    msg, client_address = serverSocket.recvfrom(buffer_size)
    received_packet = msg.decode()
    parsed_packet = received_packet.split('\r\n', 1)
    packet_id = int(parsed_packet[0])
    received_IDs.append(packet_id)

    if packet_id == Last_correctly_received_id + 1:

        if packet_id == 0:
            num_of_packets = int(parsed_packet[1])
        else:
            packets_data.append(parsed_packet[1])
        Last_correctly_received_id = packet_id

        serverSocket.sendto(("ACK-{}".format(Last_correctly_received_id)).encode(), client_address)
        if Last_correctly_received_id >= num_of_packets:
            break
    else:
        serverSocket.sendto(("ACK-{}".format(Last_correctly_received_id)).encode(), client_address)

serverSocket.close()

output_file = open('rx_file.txt', 'w')
output_file.write(''.join(packets_data))
output_file.close()

# Plot the received packets IDs
plt.step(np.arange(len(received_IDs)), received_IDs)
plt.title('Received packet ID versus time index')
plt.xlabel('time index')
plt.ylabel('received packet ID')
plt.show()
