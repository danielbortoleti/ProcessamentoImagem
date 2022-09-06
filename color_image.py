from turtle import color
from PIL import Image

def pega_cores_da_image(image):
    image = Image.open(image)
    colors = image.getcolors(image.size[0]*image.size[1]) # 0 Largura 1 Altura
    for pixel in colors:
        print(pixel)

if __name__ == "__main__":
    pega_cores_da_image('freeza.jpg')