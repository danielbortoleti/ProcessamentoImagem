import io 
import os
from turtle import width
import requests
import numpy as np
import PySimpleGUI as sg
from PIL  import Image

def main():
    layout =[
        [sg.Image(key="-IMAGE-", size=(500,500))],
        [
            sg.Text("Arquivo de Imagem: "),
            sg.Input(size=(25,1), key="-FILE-"),
            sg.FileBrowse(file_types=[("JPEG (*jpg)", "*.jpg"), ("Todos os arquivos" , "*.*")]),
            sg.Button("Carregar Imagem"),
            sg.Button("Thumbnail"),
        ],
        [   sg.Text("Endereço URL: "),
            sg.Input(size=(25,1), key="-URL-"),
            sg.Button("Carregar Imagem da URL"),
            sg.Button("Reduzir qualidade")
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
            image = value["-URL-"] 
            image=Image.open(requests.get(url=image, stream=True).raw)
            bio = io.BytesIO()
            image.save(bio, format="PNG")  
            window["-IMAGE-"].update(data=bio.getvalue(), size=(500,500)) 
            
        if event == "Thumbnail":
            image.thumbnail((75, 75))
            image.save("teste.jpg")

        if event == "Reduzir qualidade":
            image.resize((800,600))
            image.save("qualidadeRuim.jpg")

    window.close()                

if __name__ == "__main__":
    main()