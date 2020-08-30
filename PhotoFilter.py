import sys, os, tempfile
from PyQt5.QtWidgets import QFileDialog, QLabel, QAction,\
    QApplication, QMenuBar, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QEvent
from Filters import Filters
from PIL import Image, ImageGrab


class PhotoFilter(QWidget, Filters):

    def __init__(self):
        super().__init__()
        self.ui()

    def ui(self):
        self.fname = None
        screen_res = ImageGrab.grab().size
        self.lbl = QLabel(self)
        self.lbl.setAlignment(Qt.AlignCenter)
        self.pixmap = QPixmap(self.fname)
        self.lbl.setPixmap(self.pixmap)
        self.lbl.setMinimumSize(screen_res[0] // 10, screen_res[1] // 10)
        self.lbl.installEventFilter(self)
        hbox = QVBoxLayout(self)
        hbox.addWidget(self.lbl)
        self.setLayout(hbox)
        self.setGeometry(screen_res[0] // 5, screen_res[1] // 5,
                         screen_res[0] // 2, screen_res[1] // 2)
        self.setWindowState(Qt.WindowMaximized)
        self.setWindowTitle('PhotoFilter')
        self.setWindowIcon(QIcon(self.resource_path('data\Logo.ico')))

        openFile = QAction('Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open file')
        openFile.triggered.connect(self.open_file)

        saveFile = QAction('Save As...', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save file as...')
        saveFile.triggered.connect(self.save_file)

        orig = QAction('Original', self)
        orig.setShortcut('ctrl+I')
        orig.setStatusTip('Original image')
        orig.triggered.connect(self.original_image)

        blur = QAction('Blur', self)
        blur.setShortcut('ctrl+L')
        blur.setStatusTip('Blur filter')
        blur.triggered.connect(self.blur_filter)

        grayscale = QAction('Grayscale', self)
        grayscale.setShortcut('ctrl+G')
        grayscale.setStatusTip('Grayscale filter')
        grayscale.triggered.connect(self.grayscale_filter)

        stereo = QAction('Stereo', self)
        stereo.setShortcut('Ctrl+T')
        stereo.setStatusTip('Stereo filter')
        stereo.triggered.connect(self.stereo_filter)

        negativ = QAction('Negativ', self)
        negativ.setShortcut('ctrl+N')
        negativ.setStatusTip('Negativ filter')
        negativ.triggered.connect(self.negativ_filter)

        bw = QAction('Black-white', self)
        bw.setShortcut('ctrl+B')
        bw.setStatusTip('Black-white filter')
        bw.triggered.connect(self.black_white_filter)

        contour = QAction('Contour', self)
        contour.setShortcut('ctrl+U')
        contour.setStatusTip('Contour filter')
        contour.triggered.connect(self.contour_filter)

        texture = QAction('Texture', self)
        texture.setShortcut('ctrl+E')
        texture.setStatusTip('Texture filter')
        texture.triggered.connect(self.texture_filter)

        menubar = QMenuBar()
        fileMenu = menubar.addMenu('&File')
        filterMenu = menubar.addMenu('&Filters')
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)
        filterMenu.addAction(orig)
        filterMenu.addAction(blur)
        filterMenu.addAction(grayscale)
        filterMenu.addAction(stereo)
        filterMenu.addAction(negativ)
        filterMenu.addAction(bw)
        filterMenu.addAction(contour)
        filterMenu.addAction(texture)
        hbox.setMenuBar(menubar)

    def eventFilter(self, source, event):
        if (source is self.lbl and event.type() == QEvent.Resize):
            self.lbl.setPixmap(self.pixmap.scaled(
                self.lbl.size(), Qt.KeepAspectRatio))
        return super(PhotoFilter, self).eventFilter(source, event)

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath('.')
        return os.path.join(base_path, relative_path)

    def screen_print(self, name):
        self.pixmap = QPixmap(name)
        self.lbl.setPixmap(self.pixmap.scaled(
            self.lbl.size(), Qt.KeepAspectRatio))

    def open_file(self):
        ofname = QFileDialog.getOpenFileName(self, 'Open file',
                                        filter='*.jpg *.png')[0]

        if ofname:
            self.fname = ofname
            self.rec = ''
            self.td = tempfile.TemporaryDirectory()
            self.oi = os.path.join((self.td).name,
                                   os.path.basename(self.fname))
            Image.open(self.fname).save(self.oi)
            self.screen_print(self.oi)

    def save_file(self):
        if self.fname:
            sname = QFileDialog.getSaveFileName(self, 'Save file',
                                                filter='*.jpg;;*.png')
            if sname[0]:
                sf = Image.open(os.path.join((self.td).name,
                                self.rec + os.path.basename(self.fname)))

                sn = sname[0]
                if sn[-4:] != '.jpg' and sn[-4:] != '.png':
                    sn = sn + sname[1][-4:]
                sf.save(sn)

    def show_im(self, im):
        fn = os.path.join((self.td).name,
                          self.rec + os.path.basename(self.fname))
        im.save(fn)

        self.screen_print(fn)

    def overlap(self):
        fn = os.path.join((self.td).name,
                          self.rec + os.path.basename(self.fname))

        self.screen_print(fn)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pf = PhotoFilter()
    pf.show()
    sys.exit(app.exec_())
