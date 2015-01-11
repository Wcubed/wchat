__author__ = 'wybe'


import struct


ENCODING = "utf-8"  # Text encoding to use


form = struct.Struct('!I')


def recvall(sock, length):
    data = b''

    while len(data) < length:
        more = sock.recv(length - len(data))

        if not more:
            return 0

        data += more

    return data


def get(sock):
    lendata = recvall(sock, form.size)
    if lendata == 0:
        return 0
    (length,) = form.unpack(lendata)
    message = recvall(sock, length)
    return message.decode(ENCODING)


def put(sock, message):
    message = message.encode(ENCODING)
    sock.send(form.pack(len(message)) + message)