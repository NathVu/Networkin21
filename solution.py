from socket import *
import socket
import os
import sys
import struct
import time
import select
import binascii

# use mac or linux terminal to run code using sudo Python testing.py
ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 2


# The packet that we shall send to each router along the path is the ICMP echo
# request packet, which is exactly what we had used in the ICMP ping exercise.
# We shall use the same packet that we built in the Ping exercise

def checksum(string):
# In this function we make the checksum of our packet
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0

    while count < countTo:
        thisVal = (string[count + 1]) * 256 + (string[count])
        csum += thisVal
        csum &= 0xffffffff
        count += 2

    if countTo < len(string):
        csum += (string[len(string) - 1])
        csum &= 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def build_packet():
    # In the sendOnePing() method of the ICMP Ping exercise ,firstly the header of our
    # packet to be sent was made, secondly the checksum was appended to the header and
    # then finally the complete packet was sent to the destination.

    # Make the header in a similar way to the ping exercise.
    myChecksum = 0
    myID = os.getpid() & 0xFFFF

    # Make a dummy header with a 0 checksum.
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, myID, 1)
    # header = struct.pack("!HHHHH", ICMP_ECHO_REQUEST, 0, myChecksum, pid, 1)
    data = struct.pack("d", time.time())

    # Calculate the checksum on the data and the dummy header.
    # Append checksum to the header.
    myChecksum = checksum(header + data)
    if sys.platform == 'darwin':
        myChecksum = socket.htons(myChecksum) & 0xffff
        # Convert 16-bit integers from host to network byte order.
    else:
        myChecksum = htons(myChecksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, myID, 1)
    packet = header + data
    return packet


def get_route(hostname):
    timeLeft = TIMEOUT
    tracelist1 = [] #This is your list to use when iterating through each trace
    tracelist2 = [] #This is your list to contain all traces

    for ttl in range(1, MAX_HOPS):
        for tries in range(TRIES):
            destAddr = socket.gethostbyname(hostname)

            # Fill in start
            # Make a raw socket named mySocket
            icmp = socket.getprotobyname("icmp")
            mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
            # Fill in end

            mySocket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, struct.pack('I', ttl))
            mySocket.settimeout(TIMEOUT)
            try:
                d = build_packet()
                mySocket.sendto(d, (hostname, 0))
                t = time.time()
                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                howLongInSelect = (time.time() - startedSelect)

                if whatReady[0] == []:  # Timeout
                    tracelist1.append("*    *    * Request timed out.")
                    tracelist2.append("%d   %s %s" % (ttl, "*", "Request timed out"))
                    print("%d   %s %s" % (ttl, "*", "Request timed out"))
                recvPacket, addr = mySocket.recvfrom(1024)
                timeReceived = time.time()
                timeLeft = timeLeft - howLongInSelect

                if timeLeft <= 0:
                    tracelist1.append("*    *    * Request timed out.")
                    tracelist2.append("%d   %s %s" % (ttl, "*", "Request timed out"))
                    print("%d   %s %s" % (ttl, "*", "Request timed out"))
            except socket.timeout:
                continue

            else:
                icmpHeader = recvPacket[20:28]
                request_type, code, checksum, packetID, sequence = struct.unpack("bbHHh", icmpHeader)
                try:  # try to fetch the hostname
                    new_hostname = socket.gethostbyaddr(addr[0])[0]
                except herror:  # if the host does not provide a hostname
                    new_hostname = "hostname not returnable"

                if request_type == 11:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print("%d   rtt=%.0f ms %s %s" % (ttl, (timeReceived - t) * 1000, addr[0], new_hostname))
                    tracelist2.append("%d   rtt=%.0f ms %s %s" % (ttl, (timeReceived - t) * 1000, addr[0], new_hostname))
                elif request_type == 3:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print("%d   rtt=%.0f ms %s %s" % (ttl, (timeReceived - t) * 1000, addr[0], new_hostname))
                    tracelist2.append("%d   rtt=%.0f ms %s %s" % (ttl, (timeReceived - t) * 1000, addr[0], new_hostname))
                elif request_type == 0:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print("%d   rtt=%.0f ms %s %s" % (ttl, (timeReceived - t) * 1000, addr[0], new_hostname))
                    tracelist2.append("%d   rtt=%.0f ms %s %s" % (ttl, (timeReceived - t) * 1000, addr[0], new_hostname))
                    return tracelist2
                else:
                    print("error")
                    break
            finally:
                mySocket.close()
get_route("www.bing.com")