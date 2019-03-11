import socket
from threading import Thread, Event
import struct


class SocketConnector(Thread):
    def __init__(self, ip, port, name='AlphaBite'):
        Thread.__init__(self)
        self.name = name
        self.server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_connection.connect((ip, port))
        print('Connected')
        self.active_connection = True

        # Functions
        self.__board_set = None
        self.__board_hme = None
        self.__board_map = None
        self.__board_upd = None

        self.__sendEvent = Event()

        self.__homeX = None
        self.__homeY = None

    def set_methods(self, board_set, board_hme, board_map, board_upd):
        self.__board_set = board_set
        self.__board_hme = board_hme
        self.__board_map = board_map
        self.__board_upd = board_upd

    @property
    def event(self):
        return self.__sendEvent

    def launch_game(self):
        # Sending name
        self.server_connection.send(struct.pack('3s B {}s'.format(len(self.name)), b'NME', len(self.name), self.name.encode()))
        print('Sent name')
        self.connect_routine()

    def connect_routine(self):
        # Getting set signal (grid size)
        end_game = self.__get_set()
        if end_game:
            self.active_connection = False
            return

        # Getting house coordinates
        self.__get_hum()

        # Getting home coordinates
        self.__get_hme()

        # Getting MAP
        self.__get_upd()

    def __get_set(self):
        """
        Gets grid size.
        :return: True if the servers quits, False if it is indeed a new game
        """
        response = self.server_connection.recv(3)
        cmd, = struct.unpack('3s', response)
        print(cmd)
        if cmd == b'BYE':
            return True
        response = self.server_connection.recv(2)
        n, m = struct.unpack('B B', response)
        assert cmd == b'SET'
        self.__handle_set(m, n)
        return False

    def __get_hum(self):
        response = self.server_connection.recv(4)
        cmd, n = struct.unpack('3s B', response)
        assert cmd == b'HUM'
        response = self.server_connection.recv(n*2)
        coordinates = struct.unpack('BB'*n, response)
        houses = [(coordinates[i], coordinates[i+1]) for i in range(0, n*2, 2)]
        self.__handle_hum(houses)

    def __get_hme(self):
        response = self.server_connection.recv(5)
        cmd, x, y = struct.unpack('3s B B', response)
        assert cmd == b'HME'
        self.__handle_hme(x, y)

    def __get_upd(self):
        response = self.server_connection.recv(3)
        cmd, = struct.unpack('3s', response)
        if cmd == b'END':
            self.connect_routine()
            return
        response = self.server_connection.recv(1)
        n, = struct.unpack('B', response)
        assert cmd == b'MAP' or b'UPD'  # UPD and MAP behave in the same way
        response = self.server_connection.recv(n*5)
        cells = struct.unpack('BBBBB'*n, response)
        upd = [(cells[i], cells[i+1], self.__parse_species(cells[i + 2], cells[i + 3], cells[i + 4]))
               for i in range(0, n * 5, 5)]
        if cmd == b'MAP':
            self.__handle_map(upd)
        else:
            self.__handle_upd(upd)

    @staticmethod
    def __parse_species(h, v, w):
        # print('TEST', h, v, w)
        species = 'h' if h else 'v' if v else 'w' if w else None
        return species, h or v or w

    def __handle_set(self, n, m):
        print("Grid size : {}x{}".format(n, m))
        self.__board_set(n, m)

    @staticmethod
    def __handle_hum(houses):
        print("Human houses:", houses)

    def __handle_hme(self, x, y):
        print('Departing at coordinates: ({}, {})'.format(x, y))
        self.__homeX = x
        self.__homeY = y

    def __handle_map(self, map):
        print("Map:", map)
        self.__board_map(map)
        self.__board_hme(self.__homeX, self.__homeY)

    def __handle_upd(self, upd):
        print("Map:", upd)
        self.__board_upd(upd)
        self.__sendEvent.set()
        
    def send_mov(self, mov_list):
        """
        mov_list = [(x_origin_1, y_origin_1, nb_unit_1, x_dest_1, y_dest_1),
                    (x_origin_2, y_origin_2, nb_unit_2, x_dest_2, y_dest_2),
                    ...]
        """
        self.__sendEvent.wait()
        n = len(mov_list)
        orders = []
        for mov in mov_list:
            orders += list(mov)
        print('Sending MOV:', mov_list)
        self.server_connection.send(struct.pack('3s B'+'BBBBB'*n, b'MOV', n, *orders))
        self.__sendEvent.clear()

    def run(self):
        while self.active_connection:
            self.__get_upd()

        print('Quitting socket.')


if __name__ == '__main__':
    servercomms = SocketConnector('192.168.1.19', 5555)
    servercomms.start()
    servercomms.join()
