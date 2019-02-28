import sys
from servercomms import SocketConnector
from board import Board
from ia import IA

if len(sys.argv) < 3:
    raise IOError("At least 2 arguments are required (IP and port).")

ip = sys.argv[-2]
port = int(sys.argv[-1])

socket = SocketConnector(ip, port)
board = Board()
ia = IA(board)

socket.set_methods(board.build, board.set_species, board.update, board.update)
ia.set_send_mov(socket.send_mov)

ia.event = socket.event

socket.launch_game()

socket.start()
ia.start()

socket.join()
ia.turn_off()
