import os

from PIL import Image

from Steganography.errors import (MessageLengthError, NonAsciiCharacterError,
                                  NonPngImageError)
from Steganography.utils import getHeaderLength


class Encoder:

    """
    Encoder class has createCodeImage method to hide message in image with specified
    filename.
    """

    def __init__(self, message):
        """Initialize Encoder object with given message and immediately converts it to
        a binary string

        :message: any message made up of ASCII characters

        """

        self.message = message
        self.binaryMessage = Encoder.messageToBinary(message)

    def getMessage(self):
        return self.message

    def setMessage(self, message):
        self.message = message
        self.binaryMessage = Encoder.messageToBinary(message)

    @staticmethod
    def messageToBinary(message):
        """Convert any string of ASCII characters to a binary string.

        :message: any string of ASCII characters
        :returns: a binary string that can be split up into bytes
        :raises NonAsciiCharacterError: if message contains non-ASCII characters

        """
        try:
            message.encode("ascii")
        except UnicodeEncodeError:
            raise NonAsciiCharacterError("Message cannot contain non-ASCII characters.")

        binaryMessage = ""

        for char in message:
            binChar = bin(ord(char))[2:]
            binaryMessage += binChar.zfill(8)

        return binaryMessage

    def createCodeImage(self, filename, outputFile=None):
        """Create copy of image with hidden message inside.

        :filename: name of image to make a copy of with message
        :message: message to hide into the image
        :outputFile: path of file to save encoded image to
        :returns: filepath of newly created image
        :raises MessageLengthError: if message is too long to be hidden in image

        """
        if not outputFile:
            noExt = os.path.splitext(filename)[0]
            # have to save to .png file to avoid JPEG compression issues
            outputFile = f"{noExt}_message.png"
        elif os.path.splitext(outputFile)[1] != ".png":
            raise NonPngImageError("outputFile must be a .png")

        img = Image.open(filename)

        headLength = getHeaderLength(img.width, img.height, img.mode)
        paddedMesLength = bin(len(self.binaryMessage))[2:].zfill(headLength)
        mesWithHeader = paddedMesLength + self.binaryMessage

        if len(mesWithHeader) > img.width * img.height * len(img.mode):
            raise MessageLengthError("Message is too long to hide in image.")

        newPixel = []
        tupLength = len(img.mode)

        for i, bit in enumerate(mesWithHeader):
            coordTup = (i // tupLength % img.width, i // tupLength // img.width)
            oldColorInt = img.getpixel(coordTup)[i % tupLength]
            oldColorBin = bin(oldColorInt)[2:]

            newColorBin = oldColorBin[:-1] + bit
            newColorInt = int(newColorBin, 2)
            newPixel.append(newColorInt)

            if i % tupLength == tupLength - 1:
                img.putpixel(coordTup, tuple(newPixel))
                newPixel.clear()

        # to change last pixel if for loop didn't change it
        if len(newPixel):
            oldPixel = img.getpixel(coordTup)
            newPixel.extend(oldPixel[len(newPixel) :])
            img.putpixel(coordTup, tuple(newPixel))

        img.save(outputFile)

        return outputFile
