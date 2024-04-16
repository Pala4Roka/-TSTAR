import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtGui import QPixmap
import cv2
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gender Recognition App")
        self.setGeometry(100, 100, 500, 400)

        self.image_label = QLabel(self)
        self.image_label.setGeometry(50, 50, 400, 250)
        self.image_label.setScaledContents(True)

        self.upload_button = QPushButton('Upload Image', self)
        self.upload_button.setGeometry(200, 320, 100, 30)
        self.upload_button.clicked.connect(self.upload_image)

    def upload_image(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', '.', 'Image Files (*.png *.jpg *.jpeg *.bmp)')
        if filename:
            image = cv2.imread(filename)
            gender = self.detect_gender(image)
            self.display_results(image, gender)

    def detect_gender(self, image):
        # Use a simple heuristic to determine gender based on facial features
        # For simplicity, assuming if there is a beard or mustache, it's a man
        # Otherwise, it's a woman
        # You can replace this with more advanced gender detection models
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = image[y:y+h, x:x+w]
            if self.detect_beard(roi_gray):
                return "Man"
            else:
                return "Woman"
        return "Gender not detected"

    def detect_beard(self, face):
        # This function checks if the image contains features resembling a beard
        # You can adjust the threshold values for your specific use case
        # This is a very basic heuristic
        # For a more accurate detection, consider using a dedicated beard detection model
        # or more sophisticated feature extraction techniques
        _, thresh = cv2.threshold(face, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 500:
                return True
        return False

    def display_results(self, image, gender):
        # Display image with gender prediction
        pixmap = QPixmap.fromImage(self.cvimage_to_qtimage(image))
        self.image_label.setPixmap(pixmap)
        self.statusBar().showMessage(f"Predicted Gender: {gender}")

    def cvimage_to_qtimage(self, cvimage):
        # Convert cv2 image to Qt image
        height, width, channel = cvimage.shape
        bytesPerLine = 3 * width
        return QImage(cvimage.data, width, height, bytesPerLine, QImage.Format_RGB888)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
