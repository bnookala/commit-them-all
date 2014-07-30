from PIL import Image
import os

def convert_to_jpg(name, png_path):
    im = Image.open(png_path)
    im.load()

    jpeg_file = 'sprites/' + name + '.jpg'
    jpeg = Image.new('RGB', im.size, (255, 255, 255))
    jpeg.paste(im, mask=im.split()[3])

    jpeg.save(jpeg_file, 'JPEG', quality=100)

    im.close()
    os.remove(png_path)

    return jpeg
