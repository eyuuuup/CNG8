import socket, sys

class ResourceRecord:
    def __init__(self, NAME, TYPE, CLASS, TTL, RDLENGTH, RDATA):
        self.NAME = NAME
        self.TYPE = TYPE
        self.CLASS = CLASS
        self.TTL = TTL
        self.RDLENGTH = RDLENGTH
        self.RDATA = RDATA

    def print(self):
        listToPrint = [self.NAME, self.TYPE, self.CLASS, self.TTL, self.RDLENGTH, self.RDATA]
        print(listToPrint)
        
    def __repr__(self):
        return '{name:'+ str(self.NAME)+', RDATA:'+ str(self.RDATA)+ '}'

    def len(self):
        return len(ResourceRecord)
    


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

"""
4.1.1. Header section format

The header contains the following fields:

                                    1  1  1  1  1  1
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      ID                       |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    QDCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ANCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    NSCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ARCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

"""
def buildHeader():

    #A 16 bit identifier assigned by the program that generates any kind of query.
    ID = b"\x00\x01"
    #print(ID)

    #A one bit field that specifies whether this message is a query (0), or a response (1).
    QR = "0"
    #print(QR)

    """
    A four bit field that specifies kind of query in this
    message.  This value is set by the originator of a query
    and copied into the response.  The values are:

    0               a standard query (QUERY)

    1               an inverse query (IQUERY)

    2               a server status request (STATUS)

    3-15            reserved for future use
    """
    OPCODE = "0000"
    #print(OPCODE)

    """
    Authoritative Answer - this bit is valid in responses,
    and specifies that the responding name server is an
    authority for the domain name in question section.
    """
    AA = "0"
    #print(AA)


    """
    TrunCation - specifies that this message was truncated
    due to length greater than that permitted on the
    transmission channel.
    """
    TC = "0"
    #print(TC)

    """
    Recursion Desired - this bit may be set in a query and
    is copied into the response.  If RD is set, it directs
    the name server to pursue the query recursively.
    """
    RD = "0"
    #print(RD)

    """
    Recursion Available - this be is set or cleared in a
    response, and denotes whether recursive query support is
    available in the name server.
    """
    RA = "0"
    #print(RA)

    #Reserved for future use.  Must be zero in all queriesand responses.
    Z = "000"
    #print(Z)

    #Response code - this 4 bit field is set as part of responses.
    RCODE = "0000"
    #print(RCODE)

    """
    An unsigned 16 bit integer specifying the number of
    entries in the question section.
    """
    QDCOUNT = b"\x00\x01"
    #print(QDCOUNT)

    """
    An unsigned 16 bit integer specifying the number of 
    resource records in the answer section.
    """
    ANCOUNT = b"\x00\x00"
    #print(ANCOUNT)

    """
    An unsigned 16 bit integer specifying the number of name 
    server resource records in the authority record section.
    """
    NSCOUNT = b"\x00\x00"
    #print(NSCOUNT)

    """
    An unsigned 16 bit integer specifying the number of
    resource records in the additional records section.
    """
    ARCOUNT = b"\x00\x00"
    #print(ARCOUNT)

    dnsHeader = ID + int(QR + OPCODE + AA + TC + RD, 2).to_bytes(1, byteorder="big") + int(RA + Z + RCODE, 2).to_bytes(1, byteorder="big")+ QDCOUNT + ANCOUNT + NSCOUNT + ARCOUNT
    #print(dnsHeader)
    #print(len(dnsHeader))
    return dnsHeader

"""
4.1.2. Question section format

The question section is used to carry the "question" in most queries,
i.e., the parameters that define what is being asked.  The section
contains QDCOUNT (usually 1) entries, each of the following format:

                                    1  1  1  1  1  1
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                                               |
    /                     QNAME                     /
    /                                               /
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     QTYPE                     |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     QCLASS                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
"""

def buildQuestion():
    """
    A domain name represented as a sequence of labels, where
    each label consists of a length octet followed by that
    number of octets.  The domain name terminates with the
    zero length octet for the null label of the root. 
    """
    #example.com
    QNAME = b"\x07\x65\x78\x61\x6d\x70\x6c\x65\x03\x63\x6f\x6d\x00"

    """
    A two octet code which specifies the type of the query.
    The values for this field include all codes valid for a
    TYPE field, together with some more general codes which
    can match more than one type of RR.
    """    
    QTYPE = b"\x00\x01"

    """
    A two octet code that specifies the class of the query.
    For example, the QCLASS field is IN for the Internet.
    """
    QCLASS = b"\x00\x01"

    dnsBody = QNAME + QTYPE + QCLASS
    #print(dnsBody)
    return dnsBody

def extractName(bodyData):
    #Extraction of NAME
    lookUp = True
    lengthLookup = True
    pointer = 0
    length = 0
    QNAMEList = []
    QNAME = b""
    currentHex = b""

    while lookUp:
        currentHex = bodyData[pointer:pointer+1]

        if(int.from_bytes(currentHex, byteorder="big") == 0):
            lookUp = False
            break

        if(lengthLookup):
            length = int.from_bytes(currentHex, byteorder="big")
            lengthLookup = False
        else:
            QNAME += currentHex
            length -= 1

        if(length == 0):
            lengthLookup = True
            QNAMEList.append(QNAME)
            QNAME = b""

        pointer += 1
    return QNAMEList, pointer

def parseRecords(bodyData, res, QNAMEList):
    
    pointer = int.from_bytes(bodyData[1:2], byteorder="big")
    #print(bodyData)
    #print(hex(pointer))
    NAME, _ = extractName(res[pointer:])
    #print(res[pointer+4:])
    #test, _ = extractName(res[pointer+4:])
    #print(test)
    #print(NAME)

    TYPE = bodyData[2:4]
    #print(TYPE)
    CLASS = bodyData[4:6]
    #print(CLASS)
    TTL = bodyData[6:10]
    #print(TTL)
    RDLENGTH = bodyData[10:12]
    acLength = int.from_bytes(RDLENGTH, byteorder="big")

    #print(RDLENGTH)
    #print(acLength+12)

    RDATA = b''
    for x in range(0, acLength):
        currentHex = bodyData[x+12:x+13]
        #print(currentHex)
        if(currentHex == b'\xc0' and TYPE == b'\x00\x02'):
            pointer = int.from_bytes(bodyData[x+13:x+14], byteorder="big")
            RNAME, _ = extractName(res[pointer:])
            #print(NAME)
            RNAME.insert(0, RDATA)
            RDATA = RNAME
            break
        else:
            RDATA += currentHex

    #print(RDATA)

    RDATAIP = '.'.join(f'{c}' for c in RDATA)
    #https://stackoverflow.com/questions/46342941/convert-a-bytearray-in-hex-to-an-ip-address-python
    if(TYPE == b'\x00\x01'):
        RDATA = RDATAIP

    firstRecord = ResourceRecord(NAME, TYPE, CLASS, TTL, RDLENGTH, RDATA)
    

    bodyData = bodyData[12+acLength:]

    if(TYPE == b'\x00\x1c'):
        #print("IPV6")
        return bodyData, []
    else:
        firstRecord.print()
        #print(bodyData)
        #print("END")
        return bodyData, firstRecord

def parseResponse(res):
    headerData = res[0:12]

    ID = headerData[0:2]
    #print(ID)

    secondLine = headerData[2:4]
    #print(secondLine)

    hexDecimal = int.from_bytes(secondLine, byteorder="big")
    binform = "{0:b}".format(hexDecimal)
    #print(binform)

    QR = binform[0] 
    #print(QR)

    OPCODE = binform[1:5]
    #print(OPCODE)

    AA = binform[5]
    #print(AA)
    
    TC = binform[6]
    #print(TC)

    RD = binform[7]
    #print(RD)

    RA = binform[8]
    #print(RA)

    Z = binform[9:12]
    #print(Z)

    RCODE = binform[12:16]
    #print(RCODE)

    QDCOUNT = headerData[4:6]
    #print(QDCOUNT)

    ANCOUNT = headerData[6:8]
    #print(ANCOUNT)

    NSCOUNT = headerData[8:10]
    #print(NSCOUNT)

    ARCOUNT = headerData[10:12]
    #print(ARCOUNT)

    """
    QUESTION PART START

    """

    bodyData = res[12:]
    #print(bodyData)

    QNAMEList, pointer = extractName(bodyData)

    #Reset bodydata position
    bodyData = bodyData[pointer+1:]
    #print(pointer)
    #print(bodyData)

    QTYPE = bodyData[0:2]
    #print(TYPE)

    QCLASS = bodyData[2:4]
    #print(CLASS)

    """
    QUESTION PART END

    """
    #Reset bodydata position
    bodyData = bodyData[4:]
    #print(bodyData)
    #print(res)
    recordList = []
    while (len(bodyData) != 0):
        bodyData, record = parseRecords(bodyData, res, QNAMEList)
        recordList.append(record)
        #print(bodyData)
        #print(len(bodyData))
    
    #print(recordList)

    dnsHeader = ID + int(QR + OPCODE + AA + TC + RD, 2).to_bytes(1, byteorder="big") + int(RA + Z + RCODE, 2).to_bytes(1, byteorder="big")+ QDCOUNT + ANCOUNT + NSCOUNT + ARCOUNT
    print(dnsHeader)
    QTYPE = [QTYPE]
    QCLASS = [QCLASS]
    dnsQuestion = QNAMEList + QTYPE + QCLASS
    print(dnsQuestion)
    dnsRecords = recordList

    return dnsHeader, dnsQuestion, dnsRecords

dnsHeader = buildHeader()

dnsBody = buildQuestion()
sock.sendto(dnsHeader + dnsBody, ("198.41.0.4", 53))
res, addr = sock.recvfrom(512)
parsedRes = parseResponse(res)
#print(res)