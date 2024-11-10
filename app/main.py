import sys
from PyQt5.QtWidgets import QApplication
from canvas import MainWindow

try:
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern looking style
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
except Exception as e:
    print(f"Application failed to start: {str(e)}")
    sys.exit(1)
