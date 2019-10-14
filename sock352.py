import binascii
import socket as syssock
import struct
import sys
import random



# these functions are global to the class and
# define the UDP ports all messages are sent
# and received from



receivept = 0
sendpt = 0

def init(UDPportTx, UDPportRx):  # initialize your UDP socket here

    if UDPportTx == '':
        UDPportTx = '10000'
    elif UDPportTx == '0':
        UDPportTx = 10000

    if UDPportRx is None:
        UDPportRx = '10000'
    elif UDPportRx == '0':
        UDPportRx = '10000'

    global receivept
    receivept = UDPportRx

    global sendpt
    sendpt = UDPportTx

    pass


class socket:

    def __init__(self):  # fill in your code here

        self.socket = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)

        self.connectindex = False

        self.sequenceNo = 0;

        self.settimeout(0.2)

        return

    def bind(self, address):
        self.socket.bind(address[0], receivept)
        return

    def connect(self, address):  # fill in your code here

        if self.connectindex == True:
            print('The client was connected before!')
            return

        self.bind((address[0], receivept))

        sequence_no = random.randint(1, 99999);

        self.sequenceNo = sequence_no

        #do we need to check connection???
        packet_fmt = '!BBBBHHLLQQLL'
        udpPkt_hdr_data = struct.Struct(packet_fmt)

        hearder_len = struct.calcsize(packet_fmt)

        flags = 0x1
        ack_no = 0x0
        payload_len = 0x0
        header = udpPkt_hdr_data.pack(0x1, flags, 0x0, 0x0, hearder_len, 0x0, 0x0, 0x0, sequence_no, ack_no,
                                      0x0, payload_len)

        #need self.socket.sendto?
        self.sendto(header, (address[0], sendpt))

        receiveIndex = False

        while receiveIndex is False:
            try:
                #calculate the size?
                data, addr = self.recvfrom(hearder_len)
                serverRespond = udpPkt_hdr_data.unpack(data)

                if serverRespond[1] == 0x01 and serverRespond[9] == sequence_no + 1:
                    receiveIndex = True
                elif serverRespond[1] == 0x04 and serverRespond[9] == sequence_no + 1:
                    receiveIndex = True
                elif serverRespond[1] == 0x08 and serverRespond[9] == sequence_no + 1:
                    receiveIndex = False
                    print('Reset the connection.')
                    return

            except syssock.timeout:
                self.sendto(header, (address[0], sendpt))

        ackOfClient = serverRespond[8] + 1
        sequence_no = sequence_no + 1
        replyHeader = udpPkt_hdr_data.pack(0x1, 0x04, 0x0, 0x0, hearder_len, 0x0, 0x0, 0x0, sequence_no, ackOfClient, 0x0, payload_len)
        self.sendto(replyHeader, (address[0], sendpt))
        self.sequenceNo = sequence_no
        self.connectindex = True

        print('The client has been successfully connected. Wait for the server...')

        return

    def listen(self, backlog):
        return

    def createPacket(self, flags=0x0, header_len=0x0, sequence_no=0x0, ack_no=0x0, payload_len=0x0):
        return

    def accept(self):

        if self.connectindex == True:
            print('The server was connected before!')
            return

        sequence_no_server = random.randint(1,99999)
        self.sequenceNo = sequence_no_server

        packet_fmt = '!BBBBHHLLQQLL'
        udpPkt_hdr_data = struct.Struct(packet_fmt)

        hearder_len = struct.calcsize(packet_fmt)
        receiveIndex = False
        ack_no = 0
        while receiveIndex is False:
            try:
                #calculate the size?
                data, addr = self.recvfrom(hearder_len)
                serverRespond = udpPkt_hdr_data.unpack(data)

                ack_no = serverRespond[9] + 1
                receiveIndex = True

            except syssock.timeout:
                pass

        replyHeader = 

        (clientsocket, address) = (1, 1)  # change this to your code

        return (clientsocket, address)

    def close(self):  # fill in your code here
        return

    def send(self, buffer):
        bytessent = 0  # fill in your code here
        return bytesent

    def recv(self, nbytes):
        bytesreceived = 0  # fill in your code here
        return bytesreceived
