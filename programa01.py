from PIL import Image 

def image_convert(input_file, output_file, format, optimize=True, quality=75):
    image = Image.open(input_file)
    image.save(output_file, format=format)
    image.thumbnail((75, 75))
    image.save("thumbnaildog.jpg")

def image_format(input_file):
    image = Image.open(input_file)
    print(f"Formato: {image.format_description}")

if __name__ == "__main__":
    image_convert("dog.png", "dog.jpg", "jpeg")
    image_format("dog.jpg")
    image_format("dog.png")
