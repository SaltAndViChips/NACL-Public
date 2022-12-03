import math
# from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import QApplication, QMainWindow
# import sys
# from dataclasses import dataclass
#
# def window():
#     app = QApplication(sys.argv)
#     win = QMainWindow()
#     win.setGeometry(200,200,300,300)
#     win.setWindowTitle("NaCl Control Panel")
#     # win.setWindowIcon(icon=)
#
#     label = QtWidgets.QLabel(win)
#     label.setText("Testing")
#     label.move(50,50)
#
#     win.show()
#     sys.exit(app.exec_())
#
# window()
# @dataclass
# def Super:
#     TestValue = 0

def main():
    StartingNum=7
    CurrentNum=StartingNum
    steplist = []
    while CurrentNum != 1:
        if (CurrentNum % 2) == 0:
            CurrentNum = CurrentNum / 2
            steplist.append(CurrentNum)

        else:
            CurrentNum = CurrentNum*3+1
            steplist.append(CurrentNum)
    print (steplist)
if __name__ == "__main__":
    main()