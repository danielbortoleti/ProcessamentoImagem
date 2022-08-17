import io 
import os
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
        ],
        [   sg.Text("Endereço URL: "),
            sg.Input(size=(25,1), key="-URL-"),
            sg.Button("Carregar Imagem da URL")
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
            url = value["-URL-"] 
            url=Image.open(requests.get(url=url, stream=True).raw)
            bio = io.BytesIO()
            url.save(bio, format="PNG")  
            window["-IMAGE-"].update(data=bio.getvalue(), size=(500,500))  
    window.close()                

if __name__ == "__main__":
    main()