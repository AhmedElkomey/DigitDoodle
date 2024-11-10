import sys
import os
from pathlib import Path
import numpy as np
import tensorflow as tf
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget,
    QMessageBox, QFrame, QSizePolicy
)
from PyQt5.QtGui import QPainter, QPen, QImage, QFont, QLinearGradient, QColor
from PyQt5.QtCore import Qt, QPoint, pyqtSlot

class StyleConfig:
    """Configuration class for application styling"""
    CANVAS_SIZE = 280
    PEN_COLOR = QColor(40, 44, 52)  # Dark blue-gray
    PEN_WIDTH = 18
    BACKGROUND_COLOR = Qt.white
    BUTTON_STYLE = """
        QPushButton {
            background-color: #4a90e2;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            font-size: 14px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #357abd;
        }
        QPushButton:pressed {
            background-color: #2a5d8f;
        }
    """
    LABEL_STYLE = """
        QLabel {
            color: #2c3e50;
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
        }
    """

class HandwritingCanvas(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(StyleConfig.CANVAS_SIZE, StyleConfig.CANVAS_SIZE)
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.drawing = False
        
        # Initialize canvas
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(StyleConfig.BACKGROUND_COLOR)
        self.last_point = QPoint()
        
        # Add drop shadow effect
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #ccc;
                border-radius: 10px;
            }
        """)

    def paintEvent(self, event):
        super().paintEvent(event)
        canvas = QPainter(self)
        canvas.drawImage(self.rect(), self.image, self.image.rect())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.drawing:
            painter = QPainter(self.image)
            pen = QPen(StyleConfig.PEN_COLOR, 
                      StyleConfig.PEN_WIDTH, 
                      Qt.SolidLine, 
                      Qt.RoundCap, 
                      Qt.RoundJoin)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.update()

    def clear_canvas(self):
        self.image.fill(StyleConfig.BACKGROUND_COLOR)
        self.update()

    def get_image_data(self):
        try:
            scaled_image = self.image.scaled(28, 28, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            gray_image = scaled_image.convertToFormat(QImage.Format_Grayscale8)
            buffer = gray_image.bits()
            buffer.setsize(gray_image.byteCount())
            img_data = np.frombuffer(buffer, dtype=np.uint8).reshape((28, 28))
            return (255 - img_data) / 255.0  # Invert and normalize
        except Exception as e:
            raise RuntimeError(f"Error processing image data: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_model()

    def init_ui(self):
        self.setWindowTitle("Digit Recognition")
        self.setStyleSheet("background-color: #f5f6fa;")
        
        # Main widget and layout
        main_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title label
        title_label = QLabel("Draw a Digit")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 20px;
            }
        """)
        layout.addWidget(title_label)

        # Canvas
        self.canvas = HandwritingCanvas()
        layout.addWidget(self.canvas, alignment=Qt.AlignCenter)

        # Buttons
        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)

        self.recognize_button = QPushButton("✨ Recognize")
        self.clear_button = QPushButton("🗑️ Clear")
        
        for button in (self.recognize_button, self.clear_button):
            button.setStyleSheet(StyleConfig.BUTTON_STYLE)
            button.setFixedHeight(40)
            button_layout.addWidget(button)

        self.recognize_button.clicked.connect(self.recognize_digit)
        self.clear_button.clicked.connect(self.canvas.clear_canvas)
        layout.addLayout(button_layout)

        # Result label
        self.result_label = QLabel("Draw a number and click Recognize")
        self.result_label.setStyleSheet(StyleConfig.LABEL_STYLE)
        self.result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_label)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
        self.setFixedSize(400, 600)

    def load_model(self):
        try:
            model_path = Path("models") / "digit_recognizer_model.h5"
            if not model_path.exists():
                raise FileNotFoundError(f"Model file not found at {model_path}")
            self.model = tf.keras.models.load_model(str(model_path))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load model: {str(e)}")
            sys.exit(1)

    @pyqtSlot()
    def recognize_digit(self):
        try:
            img_data = self.canvas.get_image_data()
            predictions = self.model.predict(img_data.reshape(1, 28, 28), verbose=0)
            predicted_digit = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_digit]) * 100
            
            self.result_label.setText(
                f"Predicted Digit: {predicted_digit}\n"
                f"Confidence: {confidence:.1f}%"
            )
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Recognition failed: {str(e)}")

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        app.setStyle('Fusion')  # Modern looking style
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Application failed to start: {str(e)}")
        sys.exit(1)