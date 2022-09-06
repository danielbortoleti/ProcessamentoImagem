from ast import If
import io 
import os
from turtle import width
import requests
import numpy as np
import PySimpleGUI as sg
from PIL  import Image
sg.theme("DarkGreen3")

def main():

    def loadCombo(combo, image, combo2):

        if combo == "Thumbnail":
            image.thumbnail((75, 75))
            image.save("thumbnail.jpg")
            show(image)


        if combo == "Loss quality":
            image.resize((500,500))
            image.save("lossQuality.jpg")
            show(image)


        if combo == ".JPG":
            image.save("img.jpg")
            
        
        if combo == ".PNG":
            image.save("img.png")


        if combo2 == "Black and White":
            image = image.convert("L")
            show(image)
            image.save("blackWhite.jpg")
        
        if combo2 == "Sepia":
            image = sepia_conversion(image)
            

        if combo2 == "Blue":
            image = blue(image)
            

        if combo2 == "Green":
            image = green(image)
            

        if combo2 == "Red":
            image = red(image)
            

    
    def blue(image):
            blue = (140, 240, 255)
            palette = calculate_palette(blue)
            image = image.convert("L")
            image.putpalette(palette)
            blueFilter = image.convert("RGB")

            show(blueFilter)

    def green(image):
            green = (190, 255, 140)
            palette = calculate_palette(green)
            image = image.convert("L")
            image.putpalette(palette)
            greenFilter = image.convert("RGB")

            show(greenFilter)

    def red(image):
            red = (255, 140, 140)
            palette = calculate_palette(red)
            image = image.convert("L")
            image.putpalette(palette)
            redFilter = image.convert("RGB")

            show(redFilter)

    def calculate_palette(white):
        i = 0
        palette = []
        r, g, b = white
        for i in range(255):
            new_red = (r* i) // 255
            new_green = (g * i) // 255
            new_blue = (b * i) // 255
            palette.extend((new_red, new_green, new_blue))
        return palette

    def loadImage():
        filename = value["-FILE-"]
        if os.path.exists(filename):
            image = Image.open(filename)
            image.thumbnail((500,500))
            bio = io.BytesIO()
            image.save(bio, format="PNG")
            window["-IMAGE-"].update(data=bio.getvalue(), size=(500,500))
            return image
       
    def loadUrl():
        image = value["-LINK-"] 
        image=Image.open(requests.get(url=image, stream=True).raw) 
        bio = io.BytesIO()
        image.save(bio, format="PNG")  
        window["-IMAGE-"].update(data=bio.getvalue(), size=(500,500)) 
        return image
        
    def show(image):
        image.thumbnail((500,500))
        bio = io.BytesIO()
        image.save(bio, format="PNG")
        window["-IMAGE-"].update(data=bio.getvalue(), size=(500,500))

    def sepia_conversion(image):
            white = (255, 240, 192)
            palette = calculate_palette(white)
            image = image.convert("L")
            image.putpalette(palette)
            sepia = image.convert("RGB")
            show(sepia)
         
    layout =[
        [
            sg.Combo(["Thumbnail", ".JPG", "Loss quality", ".PNG"], key="-COMBO-"),
            sg.Combo(["Black and White", "Sepia", "Blue", "Red", "Green"], key="-COMBO2-"),
            sg.Button("Save")
        ],
        [sg.Image(key="-IMAGE-", size=(500,500))],
        [   sg.Text("Image Address: "),
            sg.Input(size=(25,1), key="-FILE-"),
            sg.FileBrowse(file_types=[("JPEG (*jpg)", "*.jpg"), ("Todos os arquivos" , "*.*")]),
            sg.Button("Load Img"),
        ],
         [
            sg.Text("URL: "),
            sg.Input(size=(25,1), key="-LINK-"),
            sg.Button("Load Url")
        ]        
    ]

    window = sg.Window("Image Manager", layout=layout)
    while True:
        event, value = window.read()
        if event == "Exit" or event == sg.WINDOW_CLOSED:
            break
       
        if event == "Load Img":
            image = loadImage()

        if event == "Load Url":
            image =loadUrl()

        combo1 = value["-COMBO-"]
        combo2 = value["-COMBO2-"]
        if event == "Save":
            loadCombo(combo1, image, combo2)

    window.close()                

if __name__ == "__main__":
    main()
