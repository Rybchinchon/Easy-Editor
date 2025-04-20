from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout, QFileDialog)
from PIL import Image
from PyQt5.QtGui import QPixmap #для изменения размера
from PyQt5.QtCore import Qt #для показа картинки
from PIL import ImageOps
from PIL import ImageFilter
from PIL import ImageEnhance

app = QApplication([])

win = QWidget()
win.setWindowTitle('Easy Editor')
win.resize(900, 600)

lw = QListWidget()

img_label = QLabel('Картинка')

button_folder = QPushButton('Папка')
button_left = QPushButton('Лево')
button_right = QPushButton('Право')
button_mirror = QPushButton('Зеркало')
button_rez = QPushButton('Резкость')
button_bw = QPushButton('Ч/Б')
button_save = QPushButton('Сохранить')
button_sbros = QPushButton('Сбросить')

row = QHBoxLayout()

сol1 = QVBoxLayout()
сol1.addWidget(button_folder)
сol1.addWidget(lw)

col2 = QVBoxLayout()
line = QHBoxLayout()
line.addWidget(button_left, 50)
line.addWidget(button_right, 50)
line.addWidget(button_mirror, 50)
line.addWidget(button_rez, 50)
line.addWidget(button_bw, 50)
line.addWidget(button_save, 50)
line.addWidget(button_sbros, 50)
col2.addWidget(img_label)

row.addLayout(сol1)
row.addLayout(col2)
col2.addItem(line)

win.setLayout(row)

import os

workdir = ''

def filter(files, extensions):
    result = [] #список
    for filename in files: #перебор файлов
        for ext in extensions: #перебор расширений
            if filename.endswith(ext):
                result.append(filename)
    return result

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():
    extensions = ['png', '.jpg', '.gif', '.jpeg', '.bmp']
    chooseWorkdir() #выбираем рабочую папку
    filenames = filter(os.listdir(workdir), extensions) #загрузка c extensions
    lw.clear() #очистка списка с картинками
    for filename in filenames:
        lw.addItem(filename)


class ImageProcessor():
    def __init__(self):
        self.image = None
        self.original = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"
    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        fullname = os.path.join(dir, filename)
        self.image = Image.open(fullname)
        self.original = self.image
    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def saveImage(self):
        path = os.path.join(workimage.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
    def showImage(self, path):
        pixmapimage = QPixmap(path)
        label_width, label_height = img_label.width(), img_label.height()
        scaled_pixmap = pixmapimage.scaled(label_width, label_height, Qt.KeepAspectRatio)
        img_label.setPixmap(scaled_pixmap)
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_contrast(self):
        self.image = ImageEnhance.Contrast(self.image)
        self.image = self.image.enhance(1.5)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_right(self):
        self.image = self.image.rotate(90)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_left(self):
        self.image = self.image.rotate(270)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def resetImage(self):
        self.image = self.original
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

workimage = ImageProcessor()

def showChosenImage():
    if lw.currentRow() >= 0:
        filename = lw.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)

button_folder.clicked.connect(showFilenamesList)
lw.currentRowChanged.connect(showChosenImage)
button_bw.clicked.connect(workimage.do_bw)
button_save.clicked.connect(workimage.saveImage)
button_mirror.clicked.connect(workimage.do_flip)
button_rez.clicked.connect(workimage.do_contrast)
button_right.clicked.connect(workimage.do_right)
button_left.clicked.connect(workimage.do_left)
button_sbros.clicked.connect(workimage.resetImage)


win.show()
app.exec_()