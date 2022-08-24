from PIL import Image

def muda_para_cinza(imagem_entrada, imagem_saida):
    imagem = Image.open(imagem_entrada)
    imagem = imagem.convert('L') #Converte para outro modelo.
    imagem = imagem.save(imagem_saida)


if __name__ == "__main__":
    muda_para_cinza("freeza.jpg", "freezaCinza.jpg")
