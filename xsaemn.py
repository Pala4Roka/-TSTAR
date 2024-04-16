import sys
from PyQt5.QtCore import Qt  
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from genderize import Genderize
class GenderDetector(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Gender Detector")
        self.setGeometry(100, 100, 400, 200)

        self.image_label = QLabel(self)
        self.image_label.setText("Upload an image to detect gender")
        self.image_label.setAlignment(Qt.AlignCenter)

        self.upload_button = QPushButton("Upload Image", self)
        self.upload_button.clicked.connect(self.upload_image)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.upload_button)
        self.setLayout(layout)

    def upload_image(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg)")
        file_dialog.setViewMode(QFileDialog.List)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)

        if file_dialog.exec_():
            file_paths = file_dialog.selectedFiles()
            if file_paths:
                for file_path in file_paths:
                    self.detect_gender(file_path)

    def detect_gender(self, file_path):
        # Загружает каскадный классификатор для распознавания лиц
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        # Считывание изображения
        img = cv2.imread(file_path)

        # Преобразование изображения в оттенки серого
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Распознавание лиц на изображении
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Проверка, обнаружено ли лицо (лица)
        if len(faces) > 0:
           # Определение пола на основе черт лица
            gender = "Man" if len(faces) > 1 else "Woman"

            # Вывод результатов
            self.display_result(file_path, gender)
        else:
            self.image_label.setText("No face detected in the image")

    def display_result(self, file_path, gender):
        self.image_label.setText(f"Detected gender: {gender}")
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GenderDetector()
    window.show()
    sys.exit(app.exec_())
