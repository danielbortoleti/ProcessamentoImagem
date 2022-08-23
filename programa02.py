from ast import If
import io 
import os
from pickletools import optimize
from turtle import width
import requests
import numpy as np
import PySimpleGUI as sg
from PIL  import Image

sg.theme('PythonPlus')



def main():

    def loadUrl():
        image = value["-URL-"] 
        image=Image.open(requests.get(url=image, stream=True).raw)
        bio = io.BytesIO()
        image.save(bio, format="PNG")  
        window["-IMAGE-"].update(data=bio.getvalue(), size=(500,500))

    def getThumbnail():
        image.thumbnail((75, 75))
        image.save("thumbnail.jpg")

    def lossQuality():
        image.save("qualidadeRuim.jpg", quality=20)

    def confirmFormat():
        if value['Combo'] == '.PNG':
            image.save('imagemFormato.png')
        else:
            image.save('imagemFormato.jpg')

    layout =[
        [sg.Image(key="-IMAGE-", size=(500,500))],
        [
            sg.Text("Arquivo de Imagem: "),
            sg.Input(size=(25,1), key="-FILE-"),
            sg.FileBrowse(file_types=[("JPEG (*jpg)", "*.jpg"), ("Todos os arquivos" , "*.*")]),
            sg.Button("Carregar Imagem"),
            sg.Button("Thumbnail"),
            sg.Combo(['.JPG', '.PNG'], key='Combo')
        ],
        [   sg.Text("Endereço URL: "),
            sg.Input(size=(25,1), key="-URL-"),
            sg.Button("Carregar Imagem da URL"),
            sg.Button("Reduzir qualidade"),
            sg.Button("Confirmar formato")
        ]
    ]

    window = sg.Window("Visualizador de Imagem", layout=layout)
    while True:
        event, value = window.read()
        if event == "Exit" or event == sg.WINDOW_CLOSED:
            break
       
        if event == "Carregar Imagem":
            filename = value["-FILE-"]
            if os.path.exists(filename):
                image = Image.open(filename)
                image.thumbnail((500,500))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["-IMAGE-"].update(data=bio.getvalue(), size=(500,500))

        if event == "Carregar Imagem da URL":
             loadUrl()
            
        if event == "Thumbnail":
            getThumbnail()

        if event == "Reduzir qualidade":
            lossQuality()

        if event == "Confirmar formato":
           confirmFormat()

    window.close()                

if __name__ == "__main__":
    main()