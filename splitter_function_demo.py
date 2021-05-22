import os
from fsplit.filesplit import Filesplit


def get_packets(file_path, mss=50, output_dir="split_files"):
    """""
    This function reads a relatively large file to split it to multiple of files according to
    the maximum segment size (MSS) and then generate a list of packets structure to be sent in GBN protocol
    @ params:
        file_path: The path (name) of the file to be split
        mss : The maximum segment size in bytes
        output_dir: The intermediate directory to save the split files in
    @ Returns:
        packets_list: The list of GBN structured packets (strings) to be sent
    """
    # Create a directory to save the split files
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    # Get the size of the file to be split
    file_size = os.path.getsize(file_path)
    # File Splitting
    Filesplit().split(file=file_path, split_size=mss, output_dir=output_dir)
    # Calculate the number of packets to be sent
    num_packets = file_size // mss + 1
    # Initialize the packets list with the first packet to be sent
    packets_list = ["0\r\n{}".format(num_packets)]
    # Get and append the successive packets
    for n in range(1, num_packets+1):
        file = open("./{}/{}_{}.txt".format(output_dir, file_path[0:-4], n))
        line = file.read()
        file.close()
        packets_list.append(str(n) + "\r\n" + line)
    return packets_list


#file_name = "apply.txt"
#packet_list = get_packets(file_name)
#print(packet_list)
