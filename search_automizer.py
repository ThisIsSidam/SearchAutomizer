import time
import pyautogui
import random
import sys
from PyQt6.QtCore import (
    QSize, 
    QCoreApplication, 
    Qt, 
    pyqtSignal,
    QThread,
)
from PyQt6.QtWidgets import (
    QSizePolicy,
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QPushButton,
    QLabel,
    QMainWindow,
    QSpinBox
)
from random_question_generator import RandomQuestion
from config import read_config, write_config

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main Window Section
        self.setWindowTitle("Search Automizer")
        self.setFixedSize(QSize(400, 100))
        self.setStyleSheet("background-color: #282828")


        # Widgets Section
        self.start_button = QPushButton("Start")
        self.start_button.setEnabled(True)
        self.start_button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.start_button.clicked.connect(self.start_automizer)
        self.start_button.setStyleSheet("background-color: green;"
                                        "color: black;" 
                                        "border-radius: 15px;")
        
        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)
        self.stop_button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.stop_button.clicked.connect(self.stop_automizer)
        self.stop_button.setStyleSheet("background-color: grey;"
                                       "color: black;" 
                                       "border-radius: 15px;")

        default_value = read_config()
        if default_value:
            self.default_loop_count = default_value
        else:
            self.default_loop_count = 1
            write_config(1)

        self.loop_counter_spinbox = QSpinBox()
        self.loop_counter_spinbox.setValue(int(self.default_loop_count))
        self.loop_counter_spinbox.setStyleSheet("background-color: #282828;"
                                                "color: white;"
                                                "selection-background-color: #282828;")

        self.loop_counter_label = QLabel()
        self.loop_counter_label.setText("0")
        self.loop_counter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loop_counter_label.setStyleSheet("background-color: grey;"
                                              "color: black;"
                                              "border-radius: 15px;"
                                              "font-size: 24px;")
    
        # Layouts Section
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.start_button, 2)

        side_container = QWidget()
        vertical_layout = QVBoxLayout(side_container)
        main_layout.addWidget(side_container, 1)

        main_layout.addWidget(self.stop_button, 2)

        vertical_layout.addWidget(self.loop_counter_spinbox)
        vertical_layout.addWidget(self.loop_counter_label)

        # Thread Section
        self.worker = Worker(self.get_loop_value())
        # self.worker.started.connect(self.worker.run)
        self.worker.update.connect(self.update_counter)
        self.worker.finished.connect(self.automizer_off)

        # Final Section
        main_layout.addStretch(0)

        window = QWidget()
        window.setLayout(main_layout)
        self.setCentralWidget(window)
        
    def start_automizer(self):
        self.update_button_state(True)
        self.worker.get_counter(self.get_loop_value())
        if self.worker.isRunning():
            print("Already Running")
        else:
            self.worker.start()

    def update_counter(self, counter):
        self.loop_counter_label.setText(counter)
        QCoreApplication.processEvents()

    def automizer_off(self):
        self.loop_counter_label.setText("0")
        self.update_button_state(False)

    def stop_automizer(self):
        if self.worker.isRunning():
            self.stop_button.setStyleSheet(f"{self.stop_button.styleSheet()} background-color: orange;")
            self.stop_button.setText("Stopping!")
            self.worker.stop()
        
    def get_loop_value(self):
        spinbox_value = self.loop_counter_spinbox.value()
        if self.default_loop_count is not spinbox_value:
            write_config(spinbox_value)
        return spinbox_value

    def update_button_state(self, bool):
        """
        Case 1: bool argument is True
        Used when the Start button is pressed. Disables Start button and changes its bg-color
        to grey. While enables Stop button and changes its bg-color to red.
        Case 2: bool argument is False
        Used when the Loop ends. Enables Start button and changes its bg-color to green. While
        disables the Stop button and changes its bg-color to grey.
        """
        if bool is True:
            self.start_button.setEnabled(False)
            self.start_button.setStyleSheet(f"{self.start_button.styleSheet()} background-color: grey;")
            self.stop_button.setEnabled(True)
            self.stop_button.setStyleSheet(f"{self.stop_button.styleSheet()} background-color: red;")
        else: 
            self.start_button.setEnabled(True)
            self.start_button.setStyleSheet(f"{self.start_button.styleSheet()} background-color: green;")
            self.stop_button.setText("Stop") # Text changes if stop button was pressed. 
            self.stop_button.setEnabled(False)
            self.stop_button.setStyleSheet(f"{self.stop_button.styleSheet()} background-color: grey;")

class Worker(QThread):
    update = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, counter):
        super().__init__()
        self.automizer_is_on = True
        self.loop_counter = counter
    
    def stop(self):
        self.automizer_is_on = False

    def get_counter(self, new_counter):
        self.loop_counter = new_counter

    def run(self):
        for i in range(int(self.loop_counter)):
            
            if self.automizer_is_on is False:
                break

            seconds = random.randint(7, 13)
            time.sleep(seconds)
            pyautogui.press('/')
            pyautogui.press('backspace')

            question = get_question()
            pyautogui.write(question)
            pyautogui.press('enter')

            self.update.emit(f"{i+1}")

        self.finished.emit()

def get_question():
    question = RandomQuestion()
    return question.get_random_question()      

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    app.exec()

if __name__ == "__main__":
    main()
    