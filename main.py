import sys
from servercomms import SocketConnector
from board import PlayingBoard
from ia import IA

if len(sys.argv) < 3:
    raise IOError("At least 2 arguments are required (IP and port).")

ip = sys.argv[-2]
port = int(sys.argv[-1])
if len(sys.argv) > 3:
    name = sys.argv[-3]
else:
    name = 'AlphaBite'

socket = SocketConnector(ip, port, name)
board = PlayingBoard()
ia = IA(board)

socket.set_methods(board.build, board.set_species, board.update, board.update)
ia.set_send_mov(socket.send_mov)


ia.event = socket.event

socket.launch_game()
ia.set_species(board.species)

socket.start()
ia.start()

socket.join()
ia.turn_off()
