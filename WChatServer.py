__author__ = 'kukemfly'

import socket
import select

import protocol as prot


# Keywords
# "Online", list of names: A way to broadcast the names of all online clients
# "Name", name: Tells the server the name of the client
# "Mess", message: is an incoming message
# "Mess", name, message: Is an outgoing message

# Ask for desired port
portset = 0
while portset == 0:
    getport = input("Please enter port (default 25565): ")
    if getport == "":
        getport = 25565 # Use default if blank
        break
    try:
        val = int(getport)
    except ValueError: # Check if input is a number
        print("Please enter a number")
        continue
    if int(getport) > 65535: # Check if number is a valid port
        print("Invalid port. Please enter a number between 1024 and 65535")
        continue
    if int(getport) < 1024: # Check if input is not a system port
        print("System ports are unsafe. Please enter a number between 1024 and 65535")
        continue
    break
PORT = int(getport)
print("Starting server on port ", PORT)

connections = []
messbufs = {}
names = {}


def parse(message, s):
    if message[0] == "Name":
        names[s] = message[1]
        print(s.getpeername(), "is now called:", names[s])
        broadcast("Online")
        broadcast_tuple(names.values())
    elif message[0] == "Mess":
        if message[1] is None:
            message = ("Mess", '')
        print(s.getpeername(), names[s], ":", message[1])
        for conn in connections:
            if conn != s:
                prot.put_tuple(conn, ("Mess", names[s], message[1]))
    return


def broadcast(message):
    for conn in connections:
        prot.put(conn, message)


def broadcast_tuple(message):
    for conn in connections:
        prot.put_tuple(conn, message)


def connect(s):
    conn, addr = s.accept()
    connections.append(conn)
    messbufs[conn] = []
    names[conn] = ''
    print(addr, "connected")


def disconnect(s):
    print(s.getpeername(), "disconnected")
    del messbufs[s]
    del names[s]
    s.close()
    connections.remove(s)
    broadcast("Online")
    broadcast_tuple(names.values())


def main():
    server = socket.socket()
    server.bind(('', PORT))
    server.setblocking(0)
    server.listen(10)

    while True:
        # Check for messages
        read, write, error = select.select(connections, (), (), 0)
        for s in read:
            message = prot.get(s)
            if message == 0:  # Connection is closed
                disconnect(s)
            elif message == '\x00\x00\x00\x00':  # End of message
                parse(messbufs[s], s)
                messbufs[s] = []
            else:  # Just a normal string
                messbufs[s].append(message)

        # Check for new incoming connections
        read, write, error = select.select((server,), (), (), 0)
        for s in read:
            connect(s)
    return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Closing connections")
        for con in connections:
            con.close()
        print("Exiting")