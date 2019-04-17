from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QObject, pyqtSlot, QUrl, QVariant

import os


app = QApplication([])
view = QWebEngineView()
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "mdod850-HbO.html"))
local_url=QUrl.fromLocalFile(file_path)
view.load(local_url)
view.show()
app.exec_()