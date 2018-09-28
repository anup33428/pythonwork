from socket import *
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8

def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0
    while count < countTo:
        thisVal = ord(string[count+1]) * 256 + ord(string[count])
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2
    if countTo < len(string):
        csum = csum + ord(string[len(string)-1])
        csum = csum & 0xffffffff
    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout
    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []: # Timeout
            return "Request timed out."
        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)
        icmpHeader = recPacket[20:28]
        hType, code, hChecksum, packetId, sequence = struct.unpack("bbHHh", icmpHeader)
        responsDetails = recPacket[:20]
        version, dType, length, id, flags, ttl, protocol, dChecksum, srcIp, destIp = struct.unpack("!BBHHHBBHII", responsDetails)
        if packetId == ID:
            bytes = struct.calcsize("d")
            timeSent = struct.unpack("d", recPacket[28:28 + bytes])[0]
            delay = (timeReceived  - timeSent) * 1000
            return delay
            #return { "delay" : delay, "ttl": ttl, "sequence": sequence }

        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return "Request timed out."

def sendOnePing(mySocket, destAddr, ID, packetSize):
    myChecksum = 0
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packetSize = packetSize - 8
    bytes = struct.calcsize("d")
    data = (packetSize - bytes) * "A"
    data = struct.pack("d", time.time()) + data
    myChecksum = checksum(str(header + data))
    if sys.platform == 'darwin':
        myChecksum = htons(myChecksum) & 0xffff
    else :
        myChecksum = htons(myChecksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data
    mySocket.sendto(packet, (destAddr, 1))

def doOnePing(destAddr, timeout, packetSize):
    icmp = getprotobyname("icmp")
    mySocket = socket(AF_INET, SOCK_RAW, icmp)
    myID = os.getpid() & 0xFFFF
    sendOnePing(mySocket, destAddr, myID, packetSize)
    response = receiveOnePing(mySocket, myID, timeout, destAddr)
    mySocket.close()
    return response


def ping(destAddr, timeout = 1, countTo = 5, packetSize = 64):
    count = 1
    recvCount = 0
    delayTotal = 0
    delayMin = 100
    delayMax = 0
    destIp = gethostbyname(destAddr)
    print "PING %s (%s) %s bytes of data." % (destAddr, destIp, packetSize)
    startTime = time.time()
    while count <= countTo:
        delay  =  doOnePing(destAddr, timeout, packetSize)
        if (delay == "Request timed out."):
            print delay
        else:
            print "%i bytes from %s (%s): icmp_seq= %i ttl= %i time=%0.3fms" % (packetSize, destAddr, destIp, count, 64 , delay)
            delayTotal = delayTotal + delay
            recvCount = recvCount + 1
            if delay < delayMin:
                delayMin = delay
            if delay > delayMax:
                delayMax = delay
        count = count + 1
        time.sleep(1)
    finishTime = time.time()
    totalTimeElapsed = (finishTime - startTime) * 1000
    pLoss = ((countTo - recvCount) * 100 ) / countTo
    delayAvg = delayTotal / countTo
    if delayMin == 100:
        delayMin = 0
    print("\n\n--------- %s ping statistics --------" %(sys.argv[1]))
    print("%d packets transmitted, %d packets received, %d%% packet loss, time %0.3f ms" %(countTo, recvCount, pLoss, totalTimeElapsed ))
    print("rtt min/avg/max = %0.4f/%0.4f/%0.4f" %(delayMin, delayAvg, delayMax))
    print

ping(sys.argv[1]);
