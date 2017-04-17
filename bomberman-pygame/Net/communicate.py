from .errors import *
try:    import pickle as pickle
except: import pickle as pickle
import zlib

def EncodeData(data,compress):
    print(data)
    data = data.encode("utf-8")
    # if compress != False:
    #     data = zlib.compress(data,compress)
    print(str(data) + "sending data")
    length = str(len(data))
    length = ("0"*(8-len(length)))+length
    return length,data
def DecodeData(data):
    try:
        data = data.decode("utf-8")
    except:
        data = pickle.loads(zlib.decompress(data))
    return data
def SendData(sock,data,compress,includelength=False,address=None):
    length,data = EncodeData(data,compress)
    '''data = pickle.loads(data)
    print("decoded: %r"%data)
    if includelength: data = length + data
    print("withlength: %r"%data)
    data = data.encode("utf-8")
    print("encoded: %r"%data)'''
    if len(data) > 1024: print("Warning: packets are big.")
    try:
        if address != None:
            sock.sendto(data,address)
        else:
            sock.send(data)
    except:
        sock.close()
        raise SocketError("Connection is broken; data could not be sent!")
def ReceiveData(sock):
    try:
        print(sock.recv(8))
        # length = int(sock.recv(8).decode())
        # data = pickle.loads(sock.recv(1000))
        data = sock.recv(1000)
        print(data)
    except:
        sock.close()
        raise SocketError("Connection is broken; data could not be received!")
    data = DecodeData(data)
    print(str(data) + "after decode")
    return data
def ReceiveDataUDP(sock,size=1024):
    try:
        data, address = sock.recvfrom(size)
    except:
        sock.close()
        raise SocketError("Connection is broken; data could not be received!")
    data = DecodeData(data)
    return data, address
