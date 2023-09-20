import sys
from pynput import keyboard
from PyQt5.QtWidgets import QApplication, QWidget,QLineEdit,QTextEdit,QTextBrowser, QComboBox, QMainWindow, QLabel, QPushButton,QHBoxLayout, QVBoxLayout, \
    QFormLayout, QCheckBox
from PyQt5.QtGui import QCursor, QIcon, QMouseEvent, QPixmap, QFont, QIntValidator, QDoubleValidator

from PyQt5.QtCore import Qt, QSize, QTimer
import pyautogui
import time
import threading

pyautogui.FAILSAFE = True


class CursorTracker(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: #B4A795;color:black;height:30")
        self.setWindowIcon(QIcon(r"C:\Users\Ranga\PycharmProjects\Mouse_Automate_v0.1\asset\icon.ico"))
        self.style_lable = "background-color:#2F539B;border-radius:5px;padding: 5px 5px;color:white"
        self.style_footer = "background-color:#1E7A8A;border-radius:5px;padding: 5px 5px;color:white"
        self.style = "background-color:#BCC6EE;border-radius:5px;"
        self.style_status="background-color:#001300;border-radius:1px;color:#FFFFFF;padding: 8px"
        self.style_button = "background-color:#945E0F;border-radius:5px;"
        self.btnDisabledStyle="background-color:#CBCB9E;border-radius:5px"
        self.new_font = QFont("Helvetica", 11)
        self.status_font=QFont("Courier New", 10)
        self.footer_font = QFont("Helvetica", 8)
        self.button_font=QFont("Helvetica", 12)

        self.image=QPixmap(r"C:\Users\Ranga\PycharmProjects\Mouse_Automate_v0.1\asset\goldenpixel.png")
        picwidth=200
        self.pixmap=self.image.scaledToWidth(picwidth)


        self.setWindowTitle("Mouse Automate v0.1.2")
        self.setGeometry(400, 100, 350, 300)
        self.layout_main = QVBoxLayout()
        self.Hlayout1 = QFormLayout()
        self.Hlayout2 = QFormLayout()

        self.selected_position = None
        self.cursor_pos = None
        self.reset_Position = False
        self.exitByKey = False
        self.firstMouseClickDone = False
        self.clickedOnbtn=False
        self.apppaused = False
        self.listener=None


        # Create a keyboard listener thread
        self.keyboard_listener_thread = threading.Thread(target=self.start_keyboard_listener)
        self.keyboard_listener_thread.daemon = True
        self.keyboard_listener_thread.start()

        self.initUi()




    def initUi(self):
        self.central_widget = QWidget()

        self.setCentralWidget(self.central_widget)

        self.label1 = QLabel(self)
        self.label1.setGeometry(50, 50, 300, 30)

        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setStyleSheet(self.style_lable)
        self.label1.setFont(self.new_font)
        self.label1.setText("Click anywhere on the screen to select a position")
        self.Hlayout1.addWidget(self.label1)

        self.button1 = QPushButton("Select position", self)
        self.button1.setGeometry(150, 220, 100, 30)
        self.button1.clicked.connect(self.set_Position_window)
        self.button1.setStyleSheet(self.style_button)
        self.button1.setFont(self.button_font)

        self.Hlayout1.setAlignment(Qt.AlignCenter)

        self.Hlayout1.addWidget(self.button1)


        self.label2 = QLabel(self)
        self.label2.setGeometry(50, 50, 300, 30)
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setStyleSheet(self.style_lable)
        self.label2.setFont(self.new_font)
        self.label2.setText("Enter amount of clicks ")
        self.Hlayout1.addWidget(self.label2)

        self.combo_box1 = QComboBox()
        self.combo_box1.addItems(["10", "100", "1000", "10000"])
        self.combo_box1.setGeometry(150, 220, 100, 30)
        self.combo_box1.currentIndexChanged.connect(self.updateValues)
        self.combo_box1.currentTextChanged.connect(self.updateValues)
        self.combo_box1.setFont(self.button_font)
        self.combo_box1.setEditable(True)
        intvalid1=QIntValidator()
        self.combo_box1.setValidator(intvalid1)
        self.count =self.combo_box1.currentText()
        self.combo_box1.setStyleSheet(self.style)
        self.combo_box1.setStyleSheet(self.style)
        self.Hlayout1.addWidget(self.combo_box1)

        self.label3 = QLabel(self)
        self.label3.setGeometry(50, 50, 300, 30)
        self.label3.setAlignment(Qt.AlignCenter)
        self.label3.setStyleSheet(self.style_lable)
        self.label3.setText("Select the amount of delay in seconds ")
        self.label3.setFont(self.new_font)
        self.Hlayout1.addWidget(self.label3)


        self.combo_box2 = QComboBox()
        self.combo_box2.addItems(
            ["0.01", "0.05", "0.1", "0.2", "0.4", "0.5", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
        self.delay =self.combo_box2.currentText()
        self.combo_box2.setEditable(True)
        intvalid2=QDoubleValidator()
        self.combo_box2.setValidator(intvalid2)
        self.combo_box2.setGeometry(150, 220, 100, 30)
        self.combo_box2.setStyleSheet(self.style)
        self.combo_box2.setFont(self.button_font)
        self.combo_box2.currentIndexChanged.connect(self.updateValues)
        self.combo_box2.currentTextChanged.connect(self.updateValues)
        self.Hlayout1.addWidget(self.combo_box2)

        self.button4 = QPushButton("Start auto clicker", self)
        self.button4.setGeometry(150, 220, 100, 30)
        self.button4.clicked.connect(self.mouseClick)
        self.button4.setStyleSheet(self.style_button)
        self.button4.setFont(self.button_font)
        self.Hlayout2.addWidget(self.button4)

        self.label5 = QLabel(self)
        self.label5.setGeometry(50, 50, 300, 30)
        self.label5.setAlignment(Qt.AlignCenter)
        self.label5.setFont(self.status_font)

        self.label5.setStyleSheet(self.style_status)
        self.label5.setText("Status")
        self.label5.setAlignment(Qt.AlignCenter)
        self.Hlayout2.addWidget(self.label5)
        # ----------------------------------------------key combo box---------------









        self.checkbox1 = QCheckBox("Reset Position")
        self.checkbox1.stateChanged.connect(self.updateValues)
        self.checkbox1.setCheckState(False)
        self.Hlayout2.addWidget(self.checkbox1)

        self.label6 = QLabel(self)
        self.label6.setGeometry(50, 50, 300, 30)
        self.label6.setStyleSheet(self.style_footer)
        self.label6.setFont(self.status_font)
        self.label6.setText("Press Esc to exit from the programme and to stop clicker press F4\n Tick the Reset-position option to make a new selection")
        self.label6.setAlignment(Qt.AlignCenter)
        self.Hlayout2.addWidget(self.label6)






        self.footer_layout=QHBoxLayout()
        self.label7 = QLabel(self)
        self.label7.setGeometry(50, 50, 150, 30)
        self.label7.setMaximumWidth(200)
        self.label7.setFont(self.status_font)
        self.label7.setStyleSheet(self.style_footer)
        self.label7.setPixmap(self.pixmap)

        self.label7.setAlignment(Qt.AlignCenter)

        self.footer_layout.addWidget(self.label7)
        self.label8=QTextEdit(self)
        self.label8.ensureCursorVisible()
        self.label8.setGeometry(50, 50, 300, 30)
        self.label8.setText("<b>Please visit our web site to download more useful applications and services <a href='http//:www.goldenpixelit.com'>www.goldenpixelit.com</a> if you have request or projects contact us via <a href>rvdistributes@gmail.com</a></b><br>Author name: vimukthi Ekanayake<br>App name : Mouse Automate<br>version :v0.1.2")
        self.label8.setStyleSheet(self.style_footer)
        self.label8.setReadOnly(True)
        self.label8.setFont(self.footer_font)
        self.footer_layout.addWidget(self.label8)



        self.layout_main.addLayout(self.Hlayout1)
        self.layout_main.addLayout(self.Hlayout2)
        self.layout_main.addLayout(self.footer_layout)
        self.central_widget.setLayout(self.layout_main)






    def set_Position_window(self):
        self.selected_position = None
        self.setCursor(Qt.CrossCursor)
        self.setWindowOpacity(0.1)
        window.showFullScreen()
        self.central_widget.hide()
        self.updateValues()
        self.clickedOnbtn=True



    def start_keyboard_listener(self):
        def on_key_press(key):
            try:
                # Print the key that was pressed
                print(f'Key pressed: {key}')
                print(f'Key pressed: {str(key)}')
                if key == keyboard.Key.f4:
                    self.apppaused=True

                    self.label5.setText("task  cancelled by user...")


                elif key == keyboard.Key.esc:

                    print("Program exit by user")
                    self.label5.setText("Program exit by user")
                    QApplication.exit()
                else:
                    print("invalid key input")

            except AttributeError:

                # Some keys don't have a char attribute (e.g., special keys)
                print(f'Special key pressed: {key}')

        # Create a keyboard listener
        with keyboard.Listener(on_press=on_key_press) as listener:
            listener.join()

    def mousePressEvent(self, event: QMouseEvent):


        try:
            if event.button() == Qt.LeftButton and not  self.firstMouseClickDone and self.clickedOnbtn :
                self.firstMouseClickDone = True
                self.central_widget.show()
                self.cursor_pos = QCursor.pos()
                x = self.cursor_pos.x()
                y = self.cursor_pos.y()
                self.selected_position = (x, y)
                self.button1.setDisabled(True)
                self.button1.setStyleSheet(self.btnDisabledStyle)
                self.label5.setText(
                    f"Mouse position: {'Not selected' if self.selected_position==None else self.selected_position} count: {self.count} delay: {self.delay}")

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
        self.firstMouseClickDone=False
        self.label5.setText(
            f"Mouse position: {'Not selected' if self.selected_position==None else self.selected_position} count: {self.count} delay: {self.delay}")
        if (self.checkbox1.isChecked()):
            self.button1.setDisabled(False)
            self.button1.setStyleSheet(self.style)





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
                self.label5.setText("task Starting.... ")

                # Loop to perform the clicks
                for turn in range(num_clicks):


                    self.setCursor(Qt.ClosedHandCursor)
                    pyautogui.click(x=target_x, y=target_y)
                    print(f"{turn + 1} Times  Clicked at ({target_x}, {target_y}) with delay of {click_delay} and count {num_clicks}"),


                    self.label5.setText(f"{turn + 1} Times  Clicked at ({target_x}, {target_y}) with delay of {click_delay} and count {num_clicks}")

                    self.button1.setDisabled(True)
                    self.button1.setStyleSheet(self.btnDisabledStyle)


                    if self.apppaused == True:
                        self.label5.setText("Programme stopped by user...")
                        break
                    time.sleep(click_delay)


                print("clicked done ")
                self.label5.setText(f'task completed..{turn + 1} Times clicked with  count:{self.count} delay: {self.delay}')

                self.setCursor(Qt.ArrowCursor)
                self.button1.setDisabled(False)
                self.button1.setStyleSheet(self.style)
                self.firstMouseClickDone = False
                self.selected_position=None
                self.clickedOnbtn=False

            else:
                print("At first select a position ")
                self.label5.setText(f"At first select a position ")

        except Exception as error:
            print(error)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CursorTracker()
    window.show()

    sys.exit(app.exec_())
