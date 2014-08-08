try:
    from PyQt4.QtGui import QApplication
except ImportError, e:
    raise RuntimeError("PyQT 4 is missing from your Python install. The UI extensions will not function properly.")
import sys
from status_view import StatusView

def start_status_view(path):
    app = QApplication([])
    window = StatusView(path)
    window.show()
    return app.exec_()