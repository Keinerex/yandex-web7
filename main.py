import os
import sys

import requests
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QDoubleSpinBox

SCREEN_SIZE = [600, 800]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def getImage(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll=37.530887,55.703118&spn=0.002,0.002&l=map&scale={str(self.scale)[:3]}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def update_image(self):
        self.getImage()
        ## Изображение
        self.image.setPixmap(QPixmap(self.map_file))
        self.scale_label.setText(f"Scale > {str(self.scale)[:3]}")

    def initUI(self):
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.scale = 1
        self.scale_label = QLabel(self)
        self.scale_label.setText(f"Scale > {self.scale}")
        font = QFont()
        font.setBold(True)
        font.setPointSize(16)
        self.scale_label.setFont(font)
        self.scale_label.setGeometry(10, 475, 150, 50)
        self.update_image()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_PageUp:
            if self.scale < 4:
                self.scale += 0.1
                self.update_image()

        if event.key() == QtCore.Qt.Key_PageDown:
            if self.scale > 1:
                self.scale -= 0.1
                self.update_image()

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
