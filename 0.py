import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtGui import QPixmap
import webcolors

def get_color_name(rgb_tuple):
    try:
        closest_name = webcolors.rgb_to_name(rgb_tuple)
    except ValueError:
        closest_name = None
    return closest_name

def get_image_colors(image_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.reshape((-1, 3))

    unique_colors = []
    for color in img:
        color_name = get_color_name(tuple(color))
        if color_name:
            unique_colors.append(color_name)
    unique_colors = list(set(unique_colors))
    return unique_colors

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Color Palette Extractor")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.image_label = QLabel("Загрузить изображение чтобы увидеть цвета которые там были использованны")
        self.layout.addWidget(self.image_label)

        self.upload_button = QPushButton("ТЫКАЙ")
        self.upload_button.clicked.connect(self.upload_image)
        self.layout.addWidget(self.upload_button)

    def upload_image(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg)")
        if file_dialog.exec_():
            selected_file = file_dialog.selectedFiles()[0]
            image_colors = get_image_colors(selected_file)
            self.display_image(selected_file)
            self.display_colors(image_colors)

    def display_image(self, image_path):
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaledToWidth(600)
        self.image_label.setPixmap(pixmap)

    def display_colors(self, colors):
        color_text = "\n".join(colors)
        palette_text = ", ".join(colors)

        colors_label = QLabel(f"<b>Цвета использованные в фотографии:</b><br/>{color_text}")
        self.layout.addWidget(colors_label)

        palette_label = QLabel(f"<b>Палитра:</b> {palette_text}")
        self.layout.addWidget(palette_label)

        self.layout.removeWidget(self.upload_button)
        self.upload_button.deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
