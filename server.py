import socket as Socket

address = 'localhost'
port = 2000

field = [
    ['', '', '', ''],
    ['', '', '', ''],
    ['', '', '', ''],
    ['', '', '', '']
]


def check_victory():
    victory_combinations = ['0000', 'xxxx']
    if field[0][0] + field[1][1] + field[2][2] + field[3][3] in victory_combinations or field[0][3] + field[1][2] + field[2][1] + field[3][0] in victory_combinations:
        return True
    for i in range(len(field)):
        string1 = ''
        string2 = ''
        for j in range(len(field[i])):
            string1 += field[i][j]
            string2 += field[j][i]
        if string1 in victory_combinations or string2 in victory_combinations:
            return True
    return False


def reset_field():
    for i in range(len(field)):
        for j in range(len(field[i])):
            field[i][j] = ''


def start_server():
    with Socket.socket(Socket.AF_INET, Socket.SOCK_STREAM) as socket:
        socket.bind((address, port))
        socket.listen()
        conn1, addr1 = socket.accept()
        print(f'{addr1} has been connected')
        conn2, addr2 = socket.accept()
        print(f'{addr2} has been connected')
        conn1.send((0).to_bytes(1, byteorder='big'))
        conn2.send((1).to_bytes(1, byteorder='big'))
        while True:
            data = conn1.recv(1024).decode('utf-8')
            if not data:
                conn2.sendall((2).to_bytes(1, byteorder='big'))
                break
            i = int(data[0])
            j = int(data[1])
            field[i][j] = '0'
            conn2.sendall(data.encode('utf-8'))
            if check_victory():
                conn1.send((2).to_bytes(1, byteorder='big'))
                conn2.send((3).to_bytes(1, byteorder='big'))
                break
            data = conn2.recv(1024).decode('utf-8')
            if not data:
                conn1.sendall((2).to_bytes(1, byteorder='big'))
                break
            i = int(data[0])
            j = int(data[1])
            field[i][j] = 'x'
            conn1.sendall(data.encode('utf-8'))
            if check_victory():
                conn1.send((3).to_bytes(1, byteorder='big'))
                conn2.send((2).to_bytes(1, byteorder='big'))
                break


if __name__ == '__main__':
    while True:
        start_server()
        reset_field()
