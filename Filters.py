import os
from PIL import Image, ImageFilter


class Filters:

    def original_image(self):
        if self.fname:
            self.rec = ''
            self.screen_print(self.oi)

    def blur_filter(self):
        if self.fname:
            self.rec = 'br_'
            if self.rec + os.path.basename(self.fname) in \
                    os.listdir(path=(self.td).name):
                self.overlap()
            else:
                im = Image.open(self.oi)
                if im.mode != 'RGB':
                    im = im.convert('RGB')

                x, y = im.size
                im = im.filter(ImageFilter.GaussianBlur(
                    int(0.003 * (x ** 2 + y ** 2) ** 0.5)))

                self.show_im(im)

    def grayscale_filter(self):
        if self.fname:
            self.rec = 'gs_'
            if self.rec + os.path.basename(self.fname) in \
                    os.listdir(path=(self.td).name):
                self.overlap()
            else:
                im = Image.open(self.oi)
                if im.mode != 'RGB':
                    im = im.convert('RGB')
                pixels = im.load()
                x, y = im.size

                for i in range(x):
                    for j in range(y):
                        r, g, b = pixels[i, j]
                        bw = int(0.2989 * r + 0.5870 * g + 0.1140 * b)
                        pixels[i, j] = bw, bw, bw

                self.show_im(im)

    def stereo_filter(self):
        if self.fname:
            self.rec = 'st_'
            if self.rec + os.path.basename(self.fname) in \
                    os.listdir(path=(self.td).name):
                self.overlap()
            else:
                im_o = Image.open(self.oi)
                if im_o.mode != 'RGB':
                    im_o = im_o.convert('RGB')
                pixels = im_o.load()
                x, y = im_o.size
                im = Image.new('RGB', (x, y))
                for i in range(x):
                    for j in range(y):
                        r, g, b = pixels[i, j]
                        if i >= (x // 85):
                            r = pixels[i - (x // 85), j][0]
                        im.putpixel((i, j), (r, g, b))

                self.show_im(im)

    def negativ_filter(self):
        if self.fname:
            self.rec = 'ng_'
            if self.rec + os.path.basename(self.fname) in \
                    os.listdir(path=(self.td).name):
                self.overlap()
            else:
                im = Image.open(self.oi)
                if im.mode != 'RGB':
                    im = im.convert('RGB')
                pixels = im.load()
                x, y = im.size

                for i in range(x):
                    for j in range(y):
                        r, g, b = pixels[i, j]
                        pixels[i, j] = 255 - r, 255 - g, 255 - b

                self.show_im(im)

    def black_white_filter(self):
        if self.fname:
            self.rec = 'bw_'
            if self.rec + os.path.basename(self.fname) in \
                    os.listdir(path=(self.td).name):
                self.overlap()
            else:
                im = Image.open(self.oi)
                if im.mode != 'RGB':
                    im = im.convert('RGB')
                pixels = im.load()
                x, y = im.size

                for i in range(x):
                    for j in range(y):
                        r, g, b = pixels[i, j]
                        if (r + g + b) >= 128:
                            pixels[i, j] = 255, 255, 255
                        else:
                            pixels[i, j] = 0, 0, 0

                self.show_im(im)

    def contour_filter(self):
        if self.fname:
            self.rec = 'ct_'
            if self.rec + os.path.basename(self.fname) in \
                    os.listdir(path=(self.td).name):
                self.overlap()
            else:
                im = Image.open(self.oi)
                if im.mode != 'RGB':
                    im = im.convert('RGB')

                im = im.filter(ImageFilter.CONTOUR)

                self.show_im(im)

    def texture_filter(self):
        if self.fname:
            self.rec = 'tx_'
            if self.rec + os.path.basename(self.fname) in \
                    os.listdir(path=(self.td).name):
                self.overlap()
            else:
                im = Image.open(self.oi)
                if im.mode != 'RGB':
                    im = im.convert('RGB')

                im = im.filter(ImageFilter.EMBOSS)

                self.show_im(im)
