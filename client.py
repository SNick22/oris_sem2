from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *

import sys
import socket
from threading import Thread

socket = socket.socket()


def recv_data():
    while True:
        try:
            data_encoded = socket.recv(1024)
        except:
            main_window.setCurrentIndex(main_window.currentIndex() + 1)
            dialog_window.change_text('Сервер не на тусе((')
            break
        data = data_encoded.decode('utf-8')
        if not data:
            break
        elif (2).to_bytes(1, byteorder='big') == data_encoded:
            game_window.status = False
            game_window.check_status()
            game_window.round_label.setText('я вообще делаю, что хочу')
            return
        elif (3).to_bytes(1, byteorder='big') == data_encoded:
            game_window.status = False
            game_window.check_status()
            game_window.round_label.setText('че, схавала?')
            return
        cells = game_window.push_list
        cell = cells[int(data[0])][int(data[1])]
        cell.setAccessibleName('filled')
        if game_window.role:
            cell.setStyleSheet("#Cell{background: #ff97af url(img/instasamka.png) no-repeat;"
                               "background-position: center;"
                               "border: 1px solid #D3D3D3;}")
        else:
            cell.setStyleSheet("#Cell{background: #ff97af url(img/moneyken.png) no-repeat;"
                               "background-position: center;"
                               "border: 1px solid #D3D3D3;}")
        cell.setEnabled(False)
        game_window.status = True
        game_window.check_status()


def send_data(data):
    socket.sendall(data.encode('utf-8'))
    game_window.status = False
    game_window.check_status()


def wait_player():
    global game_window
    try:
        socket.connect(('localhost', 2000))
    except:
        main_window.setCurrentIndex(main_window.currentIndex() + 2)
        dialog_window.change_text('Сервер не на тусе((')
        return
    data = socket.recv(1)
    if (0).to_bytes(1, byteorder='big') == data:
        game_window.status = True
    elif (1).to_bytes(1, byteorder='big') == data:
        game_window.status = False
        game_window.role = False
    game_window.check_status()
    main_window.setCurrentIndex(main_window.currentIndex() + 1)
    t = Thread(target=recv_data, daemon=True)
    t.start()


class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.UiComponents()

    def UiComponents(self):
        start_game = QPushButton(self)
        start_game.setFont(QFont('Arial', 18))
        start_game.setText('Пусси джуси')
        start_game.setGeometry(175, 300, 200, 70)
        start_game.clicked.connect(self.switch_next)

    def switch_next(self):
        main_window.setCurrentIndex(main_window.currentIndex() + 1)
        t = Thread(target=wait_player)
        t.start()


class PlayerWaitingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.UiComponents()

    def UiComponents(self):
        label = QLabel(self)
        movie = QMovie('img/loader.gif')
        movie.setScaledSize(QSize(320, 277))
        label.setMovie(movie)
        movie.start()
        label.setGeometry(120, 100, 320, 320)
        text = QLabel(self)
        text.setText('Ждем мамми...')
        text.setFont(QFont('Arial', 18))
        text.move(180, 500)


class GameWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.status = True
        self.role = True
        self.UiComponents()

    def UiComponents(self):
        self.push_list = []
        for _ in range(4):
            temp = []
            for _ in range(4):
                temp.append((QPushButton(self)))
            self.push_list.append(temp)
        x = 60
        y = 30
        for i in range(4):
            for j in range(4):
                self.push_list[i][j].setGeometry(110 * i + x,
                                                 110 * j + y,
                                                 100, 100)
                self.push_list[i][j].setObjectName("Cell")
                self.push_list[i][j].setStyleSheet("#Cell{background-color: #ff97af; border: 1px solid #D3D3D3;}"
                                                   "#Cell:hover{background-color: #fff;}")
                self.push_list[i][j].clicked.connect(self.fill_cell)
                self.push_list[i][j].setAccessibleName(f"{i}{j}")
                if not self.status:
                    self.push_list[i][j].setEnabled(False)
        self.round_label = QLabel(self)
        self.round_label.setFont(QFont('Arial', 18))
        self.round_label.resize(400, 30)
        self.round_label.move(70, 550)
        self.round_label.setAlignment(Qt.AlignHCenter)

    def fill_cell(self):
        button = self.sender()
        send_data(button.accessibleName())
        button.setAccessibleName('filled')
        button.setEnabled(False)
        if self.role:
            button.setStyleSheet("#Cell{background: #ff97af url(img/moneyken.png) no-repeat;"
                                 "background-position: center;"
                                 "border: 1px solid #D3D3D3;}")
        else:
            button.setStyleSheet("#Cell{background: #ff97af url(img/instasamka.png) no-repeat;"
                                 "background-position: center;"
                                 "border: 1px solid #D3D3D3;}")

    def check_status(self):
        if not self.status:
            for i in self.push_list:
                for j in i:
                    j.setEnabled(False)
            if self.role:
                self.round_label.setText('Сейчас ход мамми')
            else:
                self.round_label.setText('Сейчас ход папика')
        else:
            for i in self.push_list:
                for j in i:
                    if j.accessibleName() != 'filled':
                        j.setEnabled(True)
            self.round_label.setText('Сейчас твой ход')


class DialogWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.UiComponents()

    def UiComponents(self):
        self.label = QLabel(self)
        self.label.setFont(QFont('Arial', 18))
        self.label.resize(main_window.width(), 30)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.move(0, main_window.height() // 2)

    def change_text(self, text):
        self.label.setText(text)


class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Moneyken love")
        self.setFixedSize(550, 700)
        self.setObjectName("MainWindow")
        self.setStyleSheet("#MainWindow{background: url(img/background.png)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    start_window = StartWindow()
    loading_window = PlayerWaitingWindow()
    game_window = GameWindow()
    dialog_window = DialogWindow()
    main_window.addWidget(start_window)
    main_window.addWidget(loading_window)
    main_window.addWidget(game_window)
    main_window.addWidget(dialog_window)
    main_window.show()
    url = QUrl.fromLocalFile("audio/track.mp3")
    content = QMediaContent(url)
    player = QMediaPlayer()
    player.setMedia(content)
    player.play()
    sys.exit(app.exec())
