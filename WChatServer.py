__author__ = 'wybe'

import socket
import select

from protocol import *


PORT = 25565  # Default port

connections = []


def main():
    server = socket.socket()
    server.bind(('', PORT))
    server.setblocking(0)
    server.listen(10)

    while True:
        # Check for messages
        read, write, error = select.select(connections, (), (), 0)
        for s in read:
            message = get(s)
            if message == 0:
                print(s.getpeername(), "disconnected")
                s.close()
                connections.remove(s)
            else:
                print(s.getpeername(), ":", message)
                for con in connections:
                    if con is not s:
                        put(con, message)

        # Check for new incoming connections
        read, write, error = select.select((server,), (), (), 0)
        for s in read:
            conn, addr = s.accept()
            connections.append(conn)
            print(addr, "connected")
    return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Closing connections")
        for con in connections:
            con.close()
        print("Exiting")