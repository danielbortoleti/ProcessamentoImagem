from turtle import color
from PIL import Image

def pega_cores_da_imagem(imagem):
    imagem = Image.open(imagem)
    colors = imagem.getcolors(imagem.size[0]*imagem.size[1]) # 0 Largura 1 Altura
    for pixel in colors:
        print(pixel)

if __name__ == "__main__":
    pega_cores_da_imagem('freeza.jpg')