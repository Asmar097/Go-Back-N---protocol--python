from socket import *
from splitter_function_demo import get_packets
from threading import Timer
import random
eps = 1

timers = [] # list of timers
file_name = "apply.txt"
packets = get_packets(file_name)  # get packets
n_packets = len(packets)  # number of packets to be transmitted

# CLIENT parameters
# port number and host name
server_port = 12500
host_name = "192.168.1.3"

# create client socket
client_socket = socket(AF_INET, SOCK_DGRAM)

# set time out
timeout = 0.1     # in second

# Window parameters
N = 3  # window size
Remaining_N = N  # empty window size
sent_pkt_index = -1  # last transmitted pkt index
window_base = 0  # first sent but not yet acknowledged pkt index


def timeout_event(index):
    global sent_pkt_index, timer
    print("Timer {} is fired..".format(index))
    # Resend the packets sent after it
    if random.randint(0, 10) > eps:
        client_socket.sendto(packets[index].encode(), (host_name, server_port))
    timer = Timer(timeout, timeout_event, args=[index])
    timer.start()
    print('pkt', str(index), ' is re - transmitted')
    for i in range(index+1, sent_pkt_index+1):
        if random.randint(0, 10) > eps:
            client_socket.sendto(packets[i].encode(), (host_name, server_port))
        print('pkt', str(i), ' is re - transmitted')


# while not all the packets are transmitted
while sent_pkt_index < n_packets - 1 or window_base < n_packets:

    # print('Number of transmitted packets', str(sent_pkt_index + 1))
    # print('Empty window size = ', str(Remaining_N))

    # while not all packets are transmitted and empty window size is available
    while Remaining_N > 0 and sent_pkt_index < n_packets - 1:
        # index of pkt to be transmitted next
        sent_pkt_index += 1
        # transmit pkt
        if random.randint(0, 10) > eps:
            client_socket.sendto(packets[sent_pkt_index].encode(), (host_name, server_port))
        # Start the timer.. For the oldest sent byt not yet acknowledged packet
        if sent_pkt_index == window_base:
            timer = Timer(timeout, timeout_event, args=[sent_pkt_index])
            timer.start()
        # change empty window size
        Remaining_N -= 1
        print('pkt', str(sent_pkt_index), ' is transmitted')
        #print('Empty window size = ', str(Remaining_N))
    # wait for ACKSs
    try:
        message, addr = client_socket.recvfrom(2048)
        # ACK received
        print('From Server:', message.decode())

        # parse ack message to get last correctly received pkt
        ack = message.decode()
        ack_id = int(message[4:])  # last correctly received pkt

        if ack_id >= window_base:
            # Remove timer
            timer.cancel()
            # change the empty window size
            Remaining_N = ack_id - window_base + 1
            # move window base
            window_base = ack_id + 1
            if window_base < n_packets:
                timer = Timer(timeout, timeout_event, args=[window_base])
                timer.start()
    except:  # timeout happened
        pass



