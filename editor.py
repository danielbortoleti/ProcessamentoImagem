from ast import If
import io 
import os
from turtle import width
import requests
import numpy as np
import PySimpleGUI as sg
from PIL  import Image
from PIL.ExifTags import TAGS, GPSTAGS
from pathlib import Path

sg.theme("DarkGreen3")

file_types = [("(JPEG (.jpg)",".jpg"),
              ("All files (.)", ".")]

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

    def get_exif_data(path):
        exif_data = {}
        try:
            image = Image.open(path)
            info = image._getexif()
        except OSError:
            info = {}

        #Se nÃ£o encontrar o arquivo
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

        
    def show(image):
        image.thumbnail((500,500))
        bio = io.BytesIO()
        image.save(bio, format="PNG")
        window["-IMAGE-"].update(data=bio.getvalue(), size=(500,500))


    menu_def = [
            ['File', ['Load Img', 'Load Url', 'Save',['.PNG', '.JPG', 'Thumbnail']]],
            ['Edit', ['Resize', 'Change Quality']],
            ['Filters', ['Black and White', 'Sepia', 'Blue', 'Green', 'Red']],
            ['Infos',['GPS INFO']],
            ]        
         

    layout = [
        [sg.Menu(menu_def)],
        [sg.Image(key="-IMAGE-", size=(500, 500))]
    ]
    window = sg.Window("Image Manager", layout=layout)

    while True:
        event, value = window.read()
        if event == "Exit" or event == sg.WINDOW_CLOSED:
            break
       
        if event == "Load Img":
            filename = sg.popup_get_file('Choose a image: ')
            if os.path.exists(filename):
                image = Image.open(filename)
                thumbnail = image
                thumbnail.thumbnail((500,500))
                bio = io.BytesIO()
                thumbnail.save(bio, format = "PNG")
                window["-IMAGE-"].update(data=bio.getvalue(), size=(500,500))

        if event == "Load Url":
            url = sg.popup_get_text('Insert a url: ')
            image = Image.open(requests.get(url=url, stream=True).raw)
            bio = io.BytesIO()
            image.save(bio, format="png")
            window["-IMAGE-"].update(data=bio.getvalue(), size=(500,500))

        if event == "Thumbnail":
            image.thumbnail((75, 75))
            image.save("thumbnail.jpg")

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
    
        if event == "GPS INFO":
                layout = [[ sg.FileBrowse("Load Image Data", file_types=file_types, key="-LOAD-", enable_events=True) ]]
                for field in fields:
                    layout += [[sg.Text(fields[field], size=(10,1)),
                                sg.Text("", size=(25,1), key=field)]]
                window = sg.Window("Image information", layout)

                while True:
                    event, values = window.read()
                    if event == "Exit" or event == sg.WIN_CLOSED:
                        break
                    if event == "-LOAD-":
                        image_path = Path(values["-LOAD-"])
                        exif_data = get_exif_data(image_path.absolute())
                        for field in fields:
                            if field == "File name":
                                window[field].update(image_path.name)
                            elif field == "File size":
                                window[field].update(image_path.stat().st_size)
                            else:
                                window[field].update(exif_data.get(field, "No data"))


    window.close()                

if __name__ == "__main__":
    main()