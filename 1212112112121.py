
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore  # Add this line to import QtCore
import cv2
import numpy as np
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image

class GenderRecognitionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Gender Recognition App')
        self.setGeometry(100, 100, 600, 400)

        self.image_label = QLabel(self)
        self.image_label.setFixedSize(300, 300)
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)

        self.upload_button = QPushButton('Upload Image', self)
        self.upload_button.clicked.connect(self.uploadImage)

        self.detect_button = QPushButton('Detect Gender', self)
        self.detect_button.clicked.connect(self.detectGender)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.detect_button)
        self.setLayout(layout)

    def uploadImage(self):
        file_dialog = QFileDialog()
        filename, _ = file_dialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if filename:
            pixmap = QPixmap(filename)
            self.image_label.setPixmap(pixmap)

            # Save the image file path
            self.image_path = filename

    def detectGender(self):
        if not hasattr(self, 'image_path'):
            QMessageBox.warning(self, "Warning", "Please upload an image first.")
            return

        print("Image path:", self.image_path)

        # Load the pre-trained MobileNetV2 model for each image detection
        model = MobileNetV2(weights='imagenet')

        # Load the image and preprocess it
        img = image.load_img(self.image_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        # Predict the class of the image
        predictions = model.predict(img_array)
        decoded_predictions = decode_predictions(predictions)

        # Print top 5 predictions
        print("Top 5 predictions:", decoded_predictions)

        # Get the predicted genders and their probabilities
        genders = {"man": 0, "woman": 0}
        for pred in decoded_predictions[0]:
            label = pred[1]
            if 'man' in label:
                genders['man'] += pred[2]
            elif 'woman' in label:
                genders['woman'] += pred[2]

        # Calculate percentages
        total_probability = genders['man'] + genders['woman']
        if total_probability > 0:  # Ensure division by zero does not occur
            man_percentage = (genders['man'] / total_probability) * 100
            woman_percentage = (genders['woman'] / total_probability) * 100
        else:
            man_percentage = 0
            woman_percentage = 0

        # Display result in a message box
        result_message = (
            f"The person in the image is identified as:\n"
            f"Man: {man_percentage:.2f}%\n"
            f"Woman: {woman_percentage:.2f}%"
        )
        print("Result message:", result_message)
        QMessageBox.information(self, "Gender Detection Result", result_message)

        # Save result to a text file
        output_filename = os.path.splitext(os.path.basename(self.image_path))[0] + "_result.txt"
        with open(output_filename, 'w') as f:
            f.write(result_message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GenderRecognitionApp()
    window.show()
    sys.exit(app.exec_())

