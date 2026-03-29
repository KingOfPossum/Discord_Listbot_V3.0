from PIL import Image,ImageDraw,ImageFont

class ImageCreator:
    """
    Class for handling image creation like creating images for metascores.
    """
    @staticmethod
    def create_metascore_image(score) -> Image:
        """
        Create the image for the metascore.
        :param score: The metascore
        :return: The created image
        """
        img = Image.new("RGB", (64,64), (0,0,0,0))
        draw = ImageDraw.Draw(img)

        if int(score) > 74:
            background_color = (0,206,122)
        elif int(score) > 50:
            background_color = (255,189,63)
        else:
            background_color = (255,104,116)

        draw.rounded_rectangle([(0, 0), (64, 64)], 10, background_color, 1, 1)

        font = ImageFont.load_default(40)
        position = (9, 8)

        color = (0, 0, 0)
        draw.text(position, str(score), color, font)

        img.save("../resources/metascore.png")
        return img