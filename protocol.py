__author__ = 'wybe'


import struct


ENCODING = "utf-8"  # Text encoding to use


form = struct.Struct('!I')


def recvall(sock, length):
    data = b''
    try:
        while len(data) < length:
            more = sock.recv(length - len(data))
            if not more:
                return 0
            data += more
    except ConnectionResetError:
        return 0

    return data


def get(sock):
    lendata = recvall(sock, form.size)
    if lendata == 0:  # Connection is closed
        return 0
    elif lendata == b'\x00\x00\x00\x00':  # End of message
        return '\x00\x00\x00\x00'
    (length,) = form.unpack(lendata)
    message = recvall(sock, length)
    return message.decode(ENCODING)


def put(sock, message):
    message = message.encode(ENCODING)
    sock.send(form.pack(len(message)) + message)


def put_tuple(sock, message):
    for part in message:
        put(sock, part)
    put(sock, '')
    return