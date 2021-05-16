# receiver
from socket import *
# UDP Parameters
buffer_size = 2048
server_port = 12500

# UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', server_port))

expected_id = 0
packets_data = []
while True:
    msg, client_address = serverSocket.recvfrom(buffer_size)
    received_packet = msg.decode()
    parsed_packet = received_packet.split('\r\n', 1)
    packet_id = int(parsed_packet[0])
    if packet_id == expected_id :
            
        if packet_id == 0:
            num_of_packets = int(parsed_packet[1])
        else:
            packets_data.append(parsed_packet[1])
        expected_id +=1
        if expected_id > num_of_packets:
            break
        serverSocket.sendto(("ACK-{}".format(expected_id)).encode(), client_address)
    else:
        serverSocket.sendto(("ACK-{}".format(expected_id)).encode(), client_address)


serverSocket.close()

print(packets_data)



