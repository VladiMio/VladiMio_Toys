from PIL import Image
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('-o', '--output')
parser.add_argument('--width', type=int, default=90)
parser.add_argument('--height', type=int, default=90)

args = parser.parse_args()

IMG = args.file
WIDTH = args.width
HEIGHT = args.height
OUTPUT = args.output

ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")


def convert_pixel_to_char(r, g, b, alphe=256):
    if alphe == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    unit = (256.0 + 1) / length
    return ascii_char[int(gray / unit)]


if __name__ == '__main__':
    img = Image.open(IMG)
    img = img.resize((WIDTH, HEIGHT), Image.NEAREST)

    text = ''

    for i in range(HEIGHT):
        for j in range(WIDTH):
            text += convert_pixel_to_char(*img.getpixel((i, j)))
        text += "\n"

    print(text)

    if OUTPUT:
        with open(OUTPUT, 'w') as f:
            f.write(text)
    else:
        with open('output.txt', 'w') as f:
            f.write(text)
