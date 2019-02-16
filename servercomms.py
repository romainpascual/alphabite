import socket
from threading import Thread
import struct

commandes_calcul = [b'ADD', b'MIN', b'TIM', b'DIV']


class SocketConnector(Thread):
    def __init__(self, ip, port):
        Thread.__init__(self)
        self.server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_connection.connect((ip, port))
        print('Connected')
        self.active_connection = True
        self.connect_routine()

    def connect_routine(self, name='AlphaBite'):
        # Sending name
        self.server_connection.send(struct.pack('3s B 9s', b'NME', 9, name.encode()))

        # Getting set signal (grid size)
        n, m = self._read_set()
        self._handle_set(n, m)

        # Getting house coordinates
        houses = self._read_hum()
        self._handle_hum(houses)

        # Getting home coordinates
        x, y = self._read_hme()
        self._handle_hme(x, y)

        # Getting MAP
        map = self._read_upd()
        self._handle_upd(map)

    def _read_set(self):
        response = self.server_connection.recv(5)
        cmd, n, m = struct.unpack('3s B B', response)
        assert cmd == b'SET'
        return n, m

    def _read_hum(self):
        response = self.server_connection.recv(4)
        cmd, n = struct.unpack('3s B', response)
        assert cmd == b'HUM'
        response = self.server_connection.recv(n*2)
        coordinates = struct.unpack('BB'*n, response)
        return [(coordinates[i], coordinates[i+1]) for i in range(0, n*2, 2)]

    def _read_hme(self):
        response = self.server_connection.recv(5)
        cmd, x, y = struct.unpack('3s B B', response)
        assert cmd == b'HME'
        return x, y

    def _read_upd(self):
        response = self.server_connection.recv(4)
        cmd, n = struct.unpack('3s B', response)
        assert cmd == b'MAP' or b'UPD'  # UPD and MAP behave in the same way
        response = self.server_connection.recv(n*5)
        cells = struct.unpack('BBBBB'*n, response)
        return [(cells[i], cells[i+1], self._parse_species(cells[i + 2], cells[i + 3], cells[i + 4]))
                for i in range(0, n * 5, 5)]

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
    def _handle_upd(map):
        print("Map:", map)

    def run(self):
        while self.active_connection:
            response = self.server_connection.recv(4)
            cmd, n = struct.unpack('3s B', response)
            print(cmd, n)
            self.active_connection = False
        print('Ran.')


if __name__ == '__main__':
    servercomms = SocketConnector('192.168.1.19', 5555)
    servercomms.start()
    servercomms.join()
