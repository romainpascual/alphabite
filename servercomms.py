import socket
from threading import Thread
import struct

commandes_calcul = [b'ADD', b'MIN', b'TIM', b'DIV']


class SocketConnector(Thread):
    def __init__(self, ip, port, name='AlphaBite'):
        Thread.__init__(self)
        self.server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_connection.connect((ip, port))
        print('Connected')
        self.active_connection = True
        # Sending name
        self.server_connection.send(struct.pack('3s B 9s', b'NME', 9, name.encode()))
        print('Sent name')
        self.connect_routine()

    def connect_routine(self):
        # Getting set signal (grid size)
        end_game = self._get_set()
        if end_game:
            self.active_connection = False
            return

        # Getting house coordinates
        self._get_hum()

        # Getting home coordinates
        self._get_hme()

        # Getting MAP
        self._get_upd()

    def _get_set(self):
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
        self._handle_set(n, m)
        return False

    def _get_hum(self):
        response = self.server_connection.recv(4)
        cmd, n = struct.unpack('3s B', response)
        assert cmd == b'HUM'
        response = self.server_connection.recv(n*2)
        coordinates = struct.unpack('BB'*n, response)
        houses = [(coordinates[i], coordinates[i+1]) for i in range(0, n*2, 2)]
        self._handle_hum(houses)

    def _get_hme(self):
        response = self.server_connection.recv(5)
        cmd, x, y = struct.unpack('3s B B', response)
        assert cmd == b'HME'
        self._handle_hme(x, y)

    def _get_upd(self):
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
        upd = [(cells[i], cells[i+1], self._parse_species(cells[i + 2], cells[i + 3], cells[i + 4]))
                for i in range(0, n * 5, 5)]
        if cmd == b'MAP':
            self._handle_map(upd)
        else:
            self._handle_upd(upd)

    @staticmethod
    def _parse_species(h, v, l):
        species = 'h' if h else 'v' if v else 'l'
        return h or v or l, species

    @staticmethod
    def _handle_set(n, m):
        print("Grid size : {}x{}".format(n, m))

    @staticmethod
    def _handle_hum(houses):
        print("Human houses:", houses)

    @staticmethod
    def _handle_hme(x, y):
        print('Departing at coordinates: ({}, {})'.format(x, y))

    @staticmethod
    def _handle_map(map):
        print("Map:", map)

    @staticmethod
    def _handle_upd(map):
        print("UPD:", map)
        
    def _send_mov(self, mov_list):
        """
        mov_list = [(x_origin_1, y_origin_1, nb_unit_1, x_dest_1, y_dest_1),
                    (x_origin_2, y_origin_2, nb_unit_2, x_dest_2, y_dest_2),
                    ...]
        """
        n = len(mov_list)
        orders = []
        for mov in mov_list:
            orders += list(mov)
        print('Sending MOV:', mov_list)
        self.server_connection.send(struct.pack('3s B'+'BBBBB'*n, b'MOV', n, *orders))

    def run(self):
        while self.active_connection:
            self._get_upd()
            self._send_mov([(4, 3, 4, 3, 2)])

            self._get_upd()
            self._send_mov([(3, 2, 4, 2, 2)])

            self._get_upd()
            self._send_mov([(2, 2, 8, 3, 1)])

            self._get_upd()
            self._send_mov([(3, 1, 8, 4, 1)])
        print('Ran.')


if __name__ == '__main__':
    servercomms = SocketConnector('192.168.1.19', 5555)
    servercomms.start()
    servercomms.join()
