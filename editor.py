from ast import If
import io 
import os
from turtle import width
import requests
import numpy as np
from PIL import ImageFilter
import PySimpleGUI as sg
from PIL  import Image
from PIL.ExifTags import TAGS, GPSTAGS
from pathlib import Path
import webbrowser

sg.theme("Material2")


file_types = [("(JPEG (.jpg)",".jpg"),
              ("All files (.)", ".")]

#Campos para informação da foto
fields = {
    "File name" : "File name",
    "File size" : "File size",
    "Model" : "Camera Model",
    "ExifImageWidth" : "Width",
    "ExifImageHeight" : "Height",
    "DateTime" : "Creating Date",
    "static_line" : "*",
    "MaxApertureValue" : "Aperture",
    "ExposureTime" : "Exposure",
    "FNumber" : "F-Stop",
    "Flash" : "Flash",
    "FocalLength" : "Focal Length",
    "ISOSpeedRatings" : "ISO",
    "ShutterSpeedValue" : "Shutter Speed"
}


def main():
    
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

    #Pega os dados da imagem
    def get_exif_data(path):
        exif_data = {}
        try:
            image = Image.open(path)
            info = image._getexif()
        except OSError:
            info = {}

        if info is None:
            info = {}
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for gps_tag in value:
                    sub_decoded = GPSTAGS.get(gps_tag, gps_tag)
                    gps_data[sub_decoded] = value[gps_tag]
                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

        return exif_data


#Função para mostrar as imagens no aplivo     
    def show(image):
        image.thumbnail((500,500))
        bio = io.BytesIO()
        image.save(bio, format="PNG")
        window["-IMAGE-"].update(data=bio.getvalue(), size=(500,500))

#Itens dos menus
    menu_def = [
            ['File', ['Load Img', 'Load Url', 'Save',['.PNG', '.JPG', 'Thumbnail']]],
            ['Edit', ['Resize', 'Change Quality']],
            ['Filters', ['Black and White', 'Sepia', 'Reset', 'Brilho', 'Contraste','Nitidez','Cores',['Blue', 'Green', 'Red']]],
            ['Rotation', ['Transpose', 'Flip', 'Baixo-Cima']],
            ['Effects', ['S-Blur', 'Box-Blur', 'Gaussian-Blur', 'Contour','Detail','Edge Enhance','Emboss','Find Edges','Sharpen','Smooth']],
            ['Infos',['GPS INFO', 'Img Info']],
            ]        
         

    layout = [
        [sg.Menu(menu_def)],
        [sg.Image(key="-IMAGE-", size=(500, 500))]
    ]
    window = sg.Window("Image Manager", layout=layout)
    loaded = False
    while True:
        event, value = window.read()
        if event == "Exit" or event == sg.WINDOW_CLOSED:
            break
        

#----------------------------------Carrega Foto------------------------------------------
        if event == "Load Img":
            filename = sg.popup_get_file('Choose a image: ')
            if os.path.exists(filename):
                image = Image.open(filename)
                thumbnail = image
                thumbnail.thumbnail((500,500))
                bio = io.BytesIO()
                thumbnail.save(bio, format = "PNG")
                window["-IMAGE-"].update(data=bio.getvalue(), size=(500,500))
                original = image
                loaded = True


        if event == "Load Url":
            url = sg.popup_get_text('Insert a url: ')
            image = Image.open(requests.get(url=url, stream=True).raw)
            bio = io.BytesIO()
            image.save(bio, format="png")
            window["-IMAGE-"].update(data=bio.getvalue(), size=(500,500))
            loaded = True


#----------------------------------Eventos------------------------------------------

        #Caso esteja com uma imagem carregada
        if loaded:

            if event == "Thumbnail":
                image.thumbnail((75, 75))
                image.save("thumbnail.jpg")
            
            if event == "Reset":
                image = original
                show(image)

            if event  == ".JPG":
                image.save("img.jpg")
                
    
            if event == ".PNG":
                image.save("img.png")   

            if event == "Resize":
                width = int(sg.popup_get_text('Width: '))
                height = int(sg.popup_get_text('Height: '))
                image.resize((width, height))
                image.save("resized.jpg")   

            if event == "Change Quality":
                quality = int(sg.popup_get_text('Quality: '))
                image.resize((800,600))
                image.save("quality.jpg", quality = quality)

            if event == "Black and White":
                image = image.convert("L")
                show(image)
                image.save("blackWhite.jpg")  

            if event == "Sepia":
                white = (255, 240, 192)
                palette = calculate_palette(white)
                image = image.convert("L")
                image.putpalette(palette)
                sepia = image.convert("RGB")
                show(sepia)
                image.save("sepia.png")

            if event == "Blue":
                blue = (140, 240, 255)
                palette = calculate_palette(blue)
                image = image.convert("L")
                image.putpalette(palette)
                blueFilter = image.convert("RGB")
                show(blueFilter)
                image.save("blue.png")
            
            if event == "Red":
                red = (255, 140, 140)
                palette = calculate_palette(red)
                image = image.convert("L")
                image.putpalette(palette)
                redFilter = image.convert("RGB")
                show(redFilter)
                image.save("red.png")
            
            if event == "Green":
                green = (190, 255, 140)
                palette = calculate_palette(green)
                image = image.convert("L")
                image.putpalette(palette)
                greenFilter = image.convert("RGB")
                show(greenFilter)
                image.save("green.png")

#-------Usando get_exif_data para extrair tanto os dados e as informações do GPS------
            if event == "GPS INFO":
                image_path = Path(filename)
                exif_data = get_exif_data(image_path.absolute())
                north = exif_data["GPSInfo"]["GPSLatitude"]
                east = exif_data["GPSInfo"]["GPSLongitude"]
                latitude = round(float(((north[0] * 60 + north[1]) * 60 + north[2]) / 3600),7)
                longitude = round(float(((east[0] * 60 + east[1]) * 60 + east[2]) / 3600),7)
                url = f'https://www.google.com.br/maps/@{latitude},-{longitude},15z'
                webbrowser.open(url)
        
            if event =="Informacao Imagem":
                layout = []
                if loaded:
                    image_path = Path(filename)
                    exif_data = get_exif_data(image_path.absolute())
                    for field in fields:
                        if field == "File name":
                            layout.append([sg.Text(fields[field], size=(10,1)),sg.Text(image_path.name,size = (25,1))]) 
                        elif field == "File size":
                            layout.append([sg.Text(fields[field], size=(10,1)),sg.Text(image_path.stat().st_size,size = (25,1))]) 
                        else:
                            layout.append([sg.Text(fields[field], size=(10,1)),sg.Text(exif_data.get(field, "No data"),size = (25,1))]) 

                    window = sg.Window("Second Window", layout, modal=True)
                    while True:
                        event = window.read()
                        if event == "Exit" or event == sg.WIN_CLOSED:
                            break
                    window.close()
                else:
                    print("Sem IMG")
            
#---------------------------Usando transpose e filter para gerar as imagens-------------------------------------
            if event == "Transpose":
                image = image.transpose(Image.TRANSPOSE)
                show(image)

            if event == 'Flip-Direita':
                image = image.transpose(Image.FLIP_LEFT_RIGHT)
                show(image)

            if event == "Baixo-Cima":
                image = image.transpose(Image.FLIP_TOP_BOTTOM)
                show(image)

            if event == "S-Blur":
                image = image.filter(ImageFilter.BLUR)
                show(image)

            if event == "Box-Blur":
                image = image.filter(ImageFilter.BoxBlur(radius=10))
                show(image)
                
            if event == "Gaussian-Blur":
                image = image.filter(ImageFilter.GaussianBlur)
                show(image)
            if event ==  'Contour' or event == 'Detail' or event == 'Edge Enhance' or event == 'Emboss' or event ==  'Find Edges' or event ==  'Sharpen' or event == 'Smooth':
                evento = event.upper()
                if " " in evento:
                    evento = evento.replace(" ", "_")
                
                palavra = {
                    'CONTOUR': ImageFilter.CONTOUR,
                    'DETAIL': ImageFilter.DETAIL,
                    'EDGE_ENHANCE': ImageFilter.EDGE_ENHANCE,
                    'EMBOSS': ImageFilter.EMBOSS,
                    'FIND_EDGES': ImageFilter.FIND_EDGES,
                    'SHARPEN': ImageFilter.SHARPEN,
                    'SMOOTH': ImageFilter.SMOOTH
                }
                image = image.filter(palavra[evento])
                show(image)
        else:
            print("Nenhuma imagem foi carregada, por favor CARREGUE UMA IMAGEM")
    window.close()                

if __name__ == "__main__":
    main()
