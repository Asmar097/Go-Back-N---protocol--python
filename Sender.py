from socket import *
from splitter_function_demo import get_packets

file_name = "apply.txt"
packets = get_packets(file_name) #get packets
n_packets = len(packets) #number of packets to be transmitted
print('Number of packets to be transmitted = ',str(n_packets))

# CLIENT parameters
#port number and host name
server_port = 12000
host_name= "10.20.100.119"

#create client socket
client_socket = socket(AF_INET,SOCK_DGRAM)

#set time out
timeout = 1  # in second
client_socket.settimeout(timeout)

#Window parameters
N = 3 #window size
Remaining_N = 3 #empty window size
sent_pkt_index = -1 #last transimetted pkt index
window_base = 0 #first sent but not yet acknowledged pkt index

#while not all the pkts are transmitted
while sent_pkt_index < n_packets: 

    print('Number of transmitted packets',str(sent_pkt_index+1))
    print('Empty window size = ',str(Remaining_N))
    
    #while not all pkts are transmitted and empty window size is available
    while Remaining_N > 0 and sent_pkt_index < n_packets -1: 

        #index of pkt to be transmitted next
        sent_pkt_index +=1 

        #transmit pkt
        client_socket.sendto(packets[sent_pkt_index].encode(),(host_name,server_port)) #encode the message and send # we need to specify the adress
        
        #change empty window size 
        Remaining_N -=1

        print('pkt',str(sent_pkt_index),' is transmitted')
        print('Empty window size = ',str(Remaining_N))
    
    #wait for ACKSs
    try:
        message, addr = client_socket.recvfrom(2048)
        #ACK recieved
        print('From Server:',message.decode())
        
        #parse ack message to get last correctly received pkt
        ack = message.decode()
        ack_id = int(message[4:]) #last correctly recieved pkt
        
        if ack_id >= window_base:
            #change the empty window size
            Remaining_N =  ack_id - window_base + 1
            #move window base
            window_base = ack_id + 1
    
    except: #timeout happend
        print('Time out')

        #re-transmit pkts
        for i in range(N):
            if window_base+i < n_packets:
                client_socket.sendto(packets[window_base+i].encode(),(host_name,server_port))
                print('pkt',str(window_base+i),' is re - transmitted')



