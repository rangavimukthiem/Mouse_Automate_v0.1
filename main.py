import sys
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QMainWindow, QLabel, QPushButton, QVBoxLayout, \
    QFormLayout, QCheckBox
from PyQt5.QtGui import QCursor, QIcon, QMouseEvent, QPixmap

from PyQt5.QtCore import Qt, QSize
import pyautogui
import time

pyautogui.FAILSAFE = False


class CursorTracker(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: #566D7E;color:black;height:30")
        self.setWindowIcon(QIcon("asset/mouse-icon-png-8.jpg"))
        self.style_lable = "background-color:#2F539B;border-radius:5px;padding: 5px 0px;color:white"
        self.style = "background-color:#BCC6EE;border-radius:5px"
        self.btnDisabledStyle="background-color:#CBCB9E;border-radius:5px"
        self.image=QPixmap("asset/goldenpixel.png")
        picwidth=200
        self.pixmap=self.image.scaledToHeight(picwidth)


        self.setWindowTitle("Mouse Automate v0.1")
        self.setGeometry(400, 100, 350, 300)
        self.layout_main = QVBoxLayout()
        self.Hlayout1 = QFormLayout()
        self.Hlayout2 = QFormLayout()

        self.selected_position = None
        self.cursor_pos = None
        self.reset_Position = False
        self.exitByKey = False
        self.firstMouseClick = False
        self.initUi()



    def initUi(self):
        self.central_widget = QWidget()

        self.setCentralWidget(self.central_widget)

        self.label1 = QLabel(self)
        self.label1.setGeometry(50, 50, 300, 30)

        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setStyleSheet(self.style_lable)
        self.label1.setText("Click anywhere on the screen to select a position")
        self.Hlayout1.addWidget(self.label1)

        self.button1 = QPushButton("Select position", self)
        self.button1.setGeometry(150, 220, 100, 30)
        self.button1.clicked.connect(self.set_Position_window)
        self.button1.setStyleSheet(self.style)
        self.Hlayout1.addWidget(self.button1)
        self.layout_main.addLayout(self.Hlayout1)

        self.label2 = QLabel(self)
        self.label2.setGeometry(50, 50, 300, 30)
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setStyleSheet(self.style_lable)
        self.label2.setText("Select the amount of clicks ")
        self.Hlayout1.addWidget(self.label2)

        self.combo_box1 = QComboBox()
        self.combo_box1.addItems(["10", "100", "1000", "10000"])
        self.combo_box1.setGeometry(150, 220, 100, 30)
        self.combo_box1.currentIndexChanged.connect(self.updateValues)
        self.count = None
        self.combo_box1.setStyleSheet(self.style)
        self.combo_box1.setStyleSheet(self.style)
        self.Hlayout1.addWidget(self.combo_box1)

        self.label3 = QLabel(self)
        self.label3.setGeometry(50, 50, 300, 30)
        self.label3.setAlignment(Qt.AlignCenter)
        self.label3.setStyleSheet(self.style_lable)
        self.label3.setText("Select the amount of delay ")
        self.Hlayout1.addWidget(self.label3)
        self.layout_main.addLayout(self.Hlayout1)

        self.combo_box2 = QComboBox()
        self.combo_box2.addItems(
            ["0.01", "0.05", "0.1", "0.2", "0.4", "0.5", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
        self.delay = None
        self.combo_box2.setGeometry(150, 220, 100, 30)
        self.combo_box2.setStyleSheet(self.style)
        self.combo_box1.currentIndexChanged.connect(self.updateValues)
        self.Hlayout1.addWidget(self.combo_box2)

        self.button4 = QPushButton("Start auto clicker", self)
        self.button4.setGeometry(150, 220, 100, 30)
        self.button4.clicked.connect(self.mouseClick)
        self.button4.setStyleSheet(self.style)
        self.Hlayout2.addWidget(self.button4)

        self.label5 = QLabel(self)
        self.label5.setGeometry(50, 50, 300, 30)
        self.label1.setAlignment(Qt.AlignCenter)

        self.label5.setStyleSheet(self.style_lable)
        self.label5.setText("Status")
        self.label5.setAlignment(Qt.AlignCenter)
        self.Hlayout2.addWidget(self.label5)
        self.layout_main.addLayout(self.Hlayout1)
        self.layout_main.addLayout(self.Hlayout2)

        self.checkbox1 = QCheckBox("Reset Position")
        self.checkbox1.stateChanged.connect(self.updateValues)
        self.checkbox1.setCheckState(False)
        self.Hlayout2.addWidget(self.checkbox1)

        self.label6 = QLabel(self)
        self.label6.setGeometry(50, 50, 300, 30)
        self.label6.setStyleSheet(self.style_lable)
        self.label6.setText("Press Esc to exit from the programme\n Tick the Reset position [ ] to make a new selection")
        self.label6.setAlignment(Qt.AlignCenter)
        self.Hlayout2.addWidget(self.label6)

        self.label7 = QLabel(self)
        self.label7.setGeometry(50, 50, 300, 30)
        self.label7.setPixmap(self.pixmap)


        self.label7.setAlignment(Qt.AlignCenter)
        self.Hlayout2.addWidget(self.label7)

        self.central_widget.setLayout(self.layout_main)

    def set_Position_window(self):
        self.selected_position = None
        self.setCursor(Qt.CrossCursor)
        self.setWindowOpacity(0.5)
        window.showFullScreen()



    def keyPressEvent(self, event) -> None:

        if event.key() == Qt.Key_Escape:
            QApplication.exit()
            sys.exit()
        elif event.key() == Qt.Key_Space:

            pass

    def mousePressEvent(self, event: QMouseEvent):
        try:
            if event.button() == Qt.LeftButton and not self.firstMouseClick:
                self.firstMouseClick = True
                self.cursor_pos = QCursor.pos()
                x = self.cursor_pos.x()
                y = self.cursor_pos.y()
                self.selected_position = (x, y)
                self.button1.setDisabled(True)
                self.button1.setStyleSheet(self.btnDisabledStyle)
                self.label5.setText(f"Mouse position: {self.selected_position} count :{self.count} delay : {self.delay}" )

                print(f"Mouse position: ({x}, {y})")
                self.setWindowOpacity(1)
                self.showNormal()
                self.setCursor(Qt.ArrowCursor)
                self.checkbox1.setCheckState(False)
            else:
                print("not LeftButton or not firstMouseClick")


        except Exception as ee:
            print("ee = ", ee)

    def updateValues(self):
        self.count = self.combo_box1.currentText()
        self.delay = self.combo_box2.currentText()
        if (self.checkbox1.isChecked()):
            self.button1.setDisabled(False)
            self.button1.setStyleSheet(self.style)
            self.firstMouseClick=False


        else:
            pass



    def mouseClick(self):
        try:
            if self.selected_position:


                self.updateValues()
                target_x, target_y = self.selected_position

                # Set the number of clicks and the delay between clicks (in seconds)
                num_clicks = int(self.count)

                print(num_clicks)  # You can change this to the desired number of clicks
                click_delay = float(self.delay)
                print(self.delay)  # You can change this to the desired delay between clicks



                # Loop to perform the clicks
                for turn in range(num_clicks):
                    QApplication.processEvents()
                    self.setCursor(Qt.ClosedHandCursor)


                    pyautogui.click(x=target_x, y=target_y)
                    print(
                        f"{turn + 1} Times  Clicked at ({target_x}, {target_y}) with delay of {self.delay} and count {num_clicks}")
                    self.label5.setText(
                        f"{turn + 1} Times  Clicked at ({target_x}, {target_y}) with delay of {self.delay} and count {num_clicks}")
                    time.sleep(click_delay)
                    self.button1.setDisabled(True)
                    self.button1.setStyleSheet(self.btnDisabledStyle)

                print("clicked done ")
                self.setCursor(Qt.ArrowCursor)
                self.updateValues()
                self.button1.setDisabled(False)
                self.button1.setStyleSheet(self.style)
                self.firstMouseClick = False
                self.selected_position=None


            else:
                print("at first select a position ")
                self.label5.setText(f"at first select a position ")


        except Exception as error:

            print(error)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CursorTracker()
    window.show()
    sys.exit(app.exec_())
