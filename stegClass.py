import os

from PIL import Image

from errors import (BinaryStringLengthError, MessageLengthError,
                    NonAsciiCharacterError, NonPngImageError)
from utils import getHeaderLength


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
