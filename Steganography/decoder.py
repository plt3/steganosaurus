import os

from PIL import Image

from Steganography.errors import BinaryStringLengthError, NonPngImageError
from Steganography.utils import getHeaderLength


class Decoder:

    """
    Decoder class has decodeImage method to return hidden message from image with
    specified filename
    """

    def __init__(self, filename):
        """Initialize Decoder object with given filename

        :filename: path to/name of file with hidden image

        """

        self.filename = filename

    def getFilename(self):
        return self.filename

    def setFilename(self, filename):
        self.filename = filename

    @staticmethod
    def binaryToMessage(binaryStr):
        """Convert a binary string that can be split up into bytes back into a message.

        :binaryStr: a binary string that can be split up into bytes
        :returns: the decoded message as a string of ASCII characters
        :raises BinaryStringLengthError: if binaryStr's length is not a multiple of 8

        """
        if len(binaryStr) % 8:
            raise BinaryStringLengthError(
                "Binary string length is not a multiple of 8."
            )

        message = ""

        for i in range(8, len(binaryStr) + 1, 8):
            byteAsDecimal = int(binaryStr[i - 8 : i], 2)
            message += chr(byteAsDecimal)

        return message

    def decodeImage(self):
        """Extract message hidden in image with provided filename.

        :filename: name of image holding secret message
        :returns: extracted message from image

        """
        if os.path.splitext(self.filename)[1] != ".png":
            raise NonPngImageError("Image to decode must be a .png")

        img = Image.open(self.filename)

        headLength = getHeaderLength(img.width, img.height, img.mode)
        tupLength = len(img.mode)
        binLength = ""

        for i in range(headLength):
            coordTup = (i // tupLength % img.width, i // tupLength // img.width)
            value = img.getpixel(coordTup)[i % tupLength]
            binLength += bin(value)[-1]

        intLength = int(binLength, 2)

        binMes = ""

        for i in range(headLength, intLength + headLength):
            coordTup = (i // tupLength % img.width, i // tupLength // img.width)
            colorInt = img.getpixel(coordTup)[i % tupLength]
            binMes += bin(colorInt)[-1]

        return Decoder.binaryToMessage(binMes)
