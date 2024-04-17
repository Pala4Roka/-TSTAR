import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
import cv2
from genderize import Genderize

class GenderDetector(QWidget):
    def __init__(self):
        super().__init__()
        self.detector = Genderize()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Gender Detection")
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
        try:
            # Load the cascade classifier for face detection
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

            # Read the image
            img = cv2.imread(file_path)

            # Convert the image to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Detect faces in the image
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # Check if faces are detected
            if len(faces) > 0:
                # Extract the name from the file path
                name = self.extract_name_from_path(file_path)
                # Use the full name for gender detection
                gender = self.detect_gender_by_name(name)

                # Display the result
                self.display_result(file_path, gender)
            else:
                self.image_label.setText("No face detected in the image")
        except Exception as e:
            print(f"An error occurred: {e}")

    def detect_gender_by_name(self, name):
        # Use the Genderize library for gender detection
        # If gender detection fails, return "Unknown"
        try:
            gender = self.detector.get([name])[0]['gender'] if name else "Unknown"
            return gender
        except Exception as e:
            print(f"Error detecting gender: {e}")
            return "Unknown"

    def display_result(self, file_path, gender):
        self.image_label.setText(f"Detected Gender: {gender}")
        # Here you can save or display the image with a bounding box around the face

    def extract_name_from_path(self, file_path):
        # Extract the name from the file path
        # This is a simple example, you might need a more sophisticated method
        return file_path.split('/')[-1].split('.')[0]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GenderDetector()
    window.show()
    sys.exit(app.exec_())
