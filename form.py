#http://stackoverflow.com/questions/36462003/pyqt5-signal-slot-decorator-example
#http://stackoverflow.com/questions/17578428/pyqt5-signals-and-slots-qobject-has-no-attribute-error
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import time

class MainForm(QWidget):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.folder1 = QLineEdit()
        self.button1 = QPushButton('Browse')
        self.button1.clicked.connect(lambda: self.selectFolder(self.folder1))

        self.folder2 = QLineEdit()
        self.button2 = QPushButton('Browse')
        self.button2.clicked.connect(lambda: self.selectFolder(self.folder2))

        self.submitButton = QPushButton('Sync')
        self.submitButton.clicked.connect(self.sync)

        selectLayout1 = QHBoxLayout()
        selectLayout1.addWidget(self.folder1)
        selectLayout1.addWidget(self.button1)

        selectLayout2 = QHBoxLayout()
        selectLayout2.addWidget(self.folder2)
        selectLayout2.addWidget(self.button2)

        mainLayout = QGridLayout()
        mainLayout.addLayout(selectLayout1, 0, 0)
        mainLayout.addLayout(selectLayout2, 1, 0)
        mainLayout.addWidget(self.submitButton, 2, 0)

        mainLayout.setVerticalSpacing(0)

        self.setLayout(mainLayout)
        self.setFixedSize(430, 130)
        self.setWindowTitle('Folder Sync')

        #self.output = Output(self)

    def selectFolder(self, textField):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.ShowDirsOnly, True)
        dialog.show()

        if dialog.exec_():
            fns = dialog.selectedFiles()
            textField.setText(fns[0])

    def sync(self):
        sync = QMessageBox.question(self, 'Proceed?',
                'Do you want to proceed?', QMessageBox.No | QMessageBox.Yes,
                QMessageBox.Yes)

        if sync == QMessageBox.Yes:
            self.output = Output(self)
            #self.output.textChanged.connect(self.do_stuff)

            for i in range(4):
                time.sleep(0.4)
                self.output.setText(str(i))

    def do_stuff(self):
        pass


class Output(QDialog):
    textChanged = pyqtSignal()

    def __init__(self, parent=None):
        super(Output, self).__init__(parent)

        self.textArea1 = QTextEdit()
        self.textArea1.setFontFamily('Courier')
        self.textArea1.setFontPointSize(11)
        self.button1 = QPushButton('Close')
        self.button1.clicked.connect(self.close)
        self.button2 = QPushButton('Start')
        self.button2.clicked.connect(self.startSync)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.textArea1, 0, 0)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.button1)
        buttonLayout.addWidget(self.button2)
        mainLayout.addLayout(buttonLayout, 1, 0)

        self.setLayout(mainLayout)
        self.setFixedSize(500, 400)
        self.setWindowTitle('Output')

    def setText(self, text):
        self.textArea1.append(text)
        self.textChanged.emit()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    screen = MainForm()
    screen.show()

    sys.exit(app.exec_())
