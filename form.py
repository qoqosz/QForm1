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

    @pyqtSlot()
    def selectFolder(self, textField):
        fn = str(QFileDialog.getExistingDirectory(self, 'Select Folder'))
        textField.setText(fn)

    @pyqtSlot()
    def sync(self):
        self.output = Output(self)
        self.output.show()


class Output(QDialog):
    textChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Output, self).__init__(parent)

        self.textArea1 = QTextEdit()
        self.textArea1.setFontFamily('Courier')
        self.textArea1.setFontPointSize(11)
        self.button1 = QPushButton('Close')
        self.button1.clicked.connect(self.close)
        self.button2 = QPushButton('Start')
        self.button2.clicked.connect(self.startOutput)
        self.button3 = QPushButton('Halt')
        self.button3.clicked.connect(self.haltOutput)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.textArea1, 0, 0)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.button1)
        buttonLayout.addWidget(self.button2)
        buttonLayout.addWidget(self.button3)
        mainLayout.addLayout(buttonLayout, 1, 0)

        self.textChanged.connect(self.setText)

        self.setLayout(mainLayout)
        self.setFixedSize(500, 400)
        self.setWindowTitle('Output')

    @pyqtSlot(str)
    def setText(self, text):
        self.textArea1.append(text)

    @pyqtSlot()
    def startOutput(self):
        self.textChanged.emit('Starting')

        self.worker = Worker()
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.start)
        self.worker.progress.connect(self.setText)

        self.thread.start()

    @pyqtSlot()
    def haltOutput(self):
        self.textChanged.emit('Stoping')
        QApplication.processEvents()

        if self.worker.isWorking:
            self.worker.quit()
            self.thread.quit()
            self.thread.wait()


class Worker(QObject):
    progress = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
        self.isWorking = True

    def __del__(self):
        self.quit()

    def start(self):
        self.execute()

    def quit(self):
        self.progress.emit('Quiting')
        self.isWorking = False

    def execute(self):
        i = 0
        while self.isWorking:
            self.progress.emit('Iteration: {}'.format(i))
            time.sleep(4.0)
            i += 1
            if i > 3:
                break

        if self.isWorking:
            self.progress.emit('Done')


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    screen = MainForm()
    screen.show()
    sys.exit(app.exec_())
