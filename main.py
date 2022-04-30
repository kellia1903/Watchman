from PyQt6 import QtWidgets
from PyQt6.QtCore import QDateTime, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QDateTimeEdit, QLabel

import sys

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle('Будильник')
        self.setGeometry(250, 250, 400, 400)

        self.date = QDateTimeEdit(QDateTime.currentDateTime(), self)  # 2
        self.date.setDisplayFormat('HH:mm dd-MM-yyyy')
        self.date.setFixedSize(200, 40)
        self.date.move(110, 35)
        self.date.dateTimeChanged.connect(self.set_time)
        self.time_alarm = QDateTime.currentDateTime()

        self.btn = QtWidgets.QPushButton(self)
        self.btn.move(105, 75)
        self.btn.setText('&Завести будильник')
        self.btn.setFixedSize(180, 30)
        self.btn.clicked.connect(self.start_window)

        self.btn_stop = QtWidgets.QPushButton(self)
        self.btn_stop.move(105, 200)
        self.btn_stop.setText('&Стоп будильник')
        self.btn_stop.setFixedSize(200, 30)
        self.btn_stop.setVisible(False)
        self.btn_stop.clicked.connect(self.alarm_stop)

        self.present_alarm = QLabel(self)
        self.present_alarm.move(130, 150)
        self.present_alarm.setFixedSize(300, 50)
        self.present_alarm.setVisible(False)

        self.accept_window = QMessageBox()
        self.accept_window.setMinimumHeight(200)
        self.accept_window.setSizeIncrement(1, 1)
        self.accept_window.setSizeGripEnabled(True)
        self.accept_window.setStandardButtons(
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
        )
        self.accept_window.buttonClicked.connect(self.start_alarm)

        self.alarm_window = QMessageBox()
        self.alarm_window.setText('ПОРА ВСТАВАТЬ!!!')
        self.alarm_window.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.alarm_window.setMinimumHeight(200)
        self.alarm_window.setSizeIncrement(1, 1)
        self.alarm_window.setSizeGripEnabled(True)

        self.timer = QTimer()


    def set_time(self):
        self.time_alarm = self.date.dateTime()


    def start_window(self):
        if self.time_alarm > QDateTime.currentDateTime():
            time_set = self.time_alarm.toString('HH:mm dd-MM-yyyy')
            self.accept_window.setText(f'Подтвердите время будильника \n'
                                       f'           {time_set}')
            self.accept_window.exec()
        else:
            error = QMessageBox()
            error.setWindowTitle('Ошибка')
            error.setText('Время уже прошло')
            error.setIcon(QMessageBox.Icon.Warning)
            error.setStandardButtons(QMessageBox.StandardButton.Ok)

            error.exec()


    def start_alarm(self, btn):
        if btn.text() == 'OK':
            self.timer.timeout.connect(self.equal_time)
            self.timer.start(10000)
            self.time_in_window()


    def time_in_window(self):
        self.present_alarm.setText(
            f'Будильник запущен на: \n'
            f'    {self.time_alarm.toString("HH:mm dd-MM-yyyy")}'
        )
        self.present_alarm.setVisible(True)
        self.btn_stop.setVisible(True)
        self.btn.setVisible(False)
        self.date.setVisible(False)


    def equal_time(self):
        time_now = QDateTime.currentDateTime().toString('HH:mm dd-MM-yyyy')
        time_alarm = self.time_alarm.toString('HH:mm dd-MM-yyyy')
        if time_now != time_alarm:
            self.timer.start(10000)
        else:
            self.alarm_work()
            self.alarm_stop()


    def alarm_work(self):
        self.alarm_window.exec()

    def alarm_stop(self):
        self.timer.stop()
        self.btn_stop.setVisible(False)
        self.present_alarm.setVisible(False)
        self.btn.setVisible(True)
        self.date.setVisible(True)
        self.time_alarm = self.date.dateTime()

def app():
    app = QApplication(sys.argv)

    window = Window()
    window.show()
    sys.exit(app.exec())




if __name__ == '__main__':
    app()

