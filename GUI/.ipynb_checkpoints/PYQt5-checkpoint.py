import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon, QFont

class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        QToolTip.setFont(QFont('SanSerif', 10))
        self.setToolTip('투울팁')

        btn = QPushButton('Quit', self)
        btn.setToolTip('끼에에엥')
        btn.move(50,50)
        #버튼 크기 설정에 적절한 도움
        btn.resize(btn.sizeHint())
        btn.clicked.connect(QCoreApplication.instance().quit)



        self.setWindowTitle('에에에')
        #self. setWidowIcon(QIcon('파일명'))
        '''        
        self.move(300,300)
        self.resize(400, 200)
        '''
        self.setGeometry(300, 300, 400, 200)
        self.show()
        
if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
