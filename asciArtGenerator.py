from PIL import Image
import numpy as np

def pixel_to_ascii(image):
    pixels = image.getdata()
    ascii_str = "";

    for pixel in pixels:
        if pixel >= 250: #white filter
            ascii_str += " "
        else:
            ascii_str += ASCII_CHARS[pixel%len(ASCII_CHARS)];
    return ascii_str

def pixel_to_filltext(image):
    pixels = image.getdata()
    ascii_str = "";

    L = len(FILLTEXT)
    count = 0
    for pixel in pixels:
        if pixel >= 250: #white filter
            ascii_str += " "
        else:
            ascii_str += FILLTEXT[count%L];
            count += 1
    return ascii_str

def to_blue_scale(image):
    buff = np.asarray(image)
    blue_channel = buff[:,:,0]
    im = Image.fromarray(blue_channel)
    #im.show()
    return im

def resize(image, new_width = 118):
    width, height = image.size
    new_height = int(new_width * height / width)
    return image.resize((new_width, new_height))

FILLTEXT = "66THBOARDOFWSVSIMONSTEVIN"
ASCII_CHARS = ["S",  "@"]
def generateASCIart(filename: object) -> object:
    """

    :rtype: object
    """
    image = Image.open(filename)
    # resize image
    image = resize(image);
    # convert image to greyscale image
    greyscale_image = to_blue_scale(image)
    # convert greyscale image to ascii characters
    ascii_str = pixel_to_filltext(greyscale_image)
    img_width = greyscale_image.width
    ascii_str_len = len(ascii_str)
    ascii_img = ""
    # Split the string based on width  of the image
    for i in range(0, ascii_str_len, img_width):
        ascii_img += ascii_str[i:i + img_width] + "\n"

    print(ascii_img)
    # save the string to a file
    with open("readme.txt", "w") as f:
        f.write(ascii_img);
        f.write("made by Ben Gortemaker, Chairman & Editor-in-Chief of the 66th Board")

if __name__ == '__main__':
    generateASCIart('ASCI-art/66logoCOMPRESSED.png')