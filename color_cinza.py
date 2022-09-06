from PIL import Image

def muda_para_cinza(image_entrada, image_saida):
    image = Image.open(image_entrada)
    image = image.convert('L') #Converte para outro modelo.
    image = image.save(image_saida)


if __name__ == "__main__":
    muda_para_cinza("freeza.jpg", "freezaCinza.jpg")
