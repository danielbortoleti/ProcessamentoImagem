from PIL import ImageColor

def pega_o_valor_rgba(color):
    return ImageColor.getcolor(color, "RGB")


if __name__ == "__main__":
    for color in ImageColor.colormap:
        print(f"{color} = {pega_o_valor_rgba(color)}")