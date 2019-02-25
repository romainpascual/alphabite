import sys
from servercomms.servercomms import SocketConnector
from board.board import Board

if len(sys.argv) < 3:
    raise IOError("At least 2 arguments are required (IP and port).")

ip = sys.argv[-2]
port = int(sys.argv[-1])

socket = SocketConnector(ip, port)
board = Board()

socket.set_methods(board.build, board.set_species, board.update, board.update)

socket.launch_game()
socket.start()
socket.join()
