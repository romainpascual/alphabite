import sys
from servercomms.servercomms import SocketConnector

if len(sys.argv) < 3:
    raise IOError("At least 2 arguments are required (IP and port).")

ip = sys.argv[-2]
port = int(sys.argv[-1])

socket = SocketConnector(ip, port)

socket.board_set = lambda n, m: print("Grid size : {}x{}".format(n, m))
socket.board_map = lambda upd: print("Map:", upd)
socket.board_upd = lambda upd: print("UPD:", upd)

socket.start()
socket.join()
