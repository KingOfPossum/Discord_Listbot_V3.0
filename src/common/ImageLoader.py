from urllib import request

class ImageLoader:
    """A class handling image loading from URLs"""

    @staticmethod
    def load_image(url, save_path):
        """Loads an image from a URL and saves it to the specified path."""
        request.urlretrieve(url, save_path)

    @staticmethod
    def convert_image_to_byte_array(image_file):
        """Converts an image file to a byte array."""
        with open(image_file,"rb") as img:
            return img.read()