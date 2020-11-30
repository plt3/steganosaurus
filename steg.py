import os

from PIL import Image

"""
TODO: let user choose how many least significant bits to change
provide a function to calculate how much text can be stored in the file
if user doesn't choose amount of LSBs, use minimum that will store the whole thing
"""


def messageToBinary(message):
    """Convert any string of ASCII characters to a binary string.

    :message: any string of ASCII characters
    :returns: a binary string that can be split up into bytes

    """
    binaryMessage = ""

    for char in message:
        binChar = bin(ord(char))[2:]
        binaryMessage += binChar.zfill(8)

    return binaryMessage


def binaryToMessage(binaryStr):
    """Convert a binary string that can be split up into bytes back into a message.

    :binaryStr: a binary string that can be split up into bytes
    :returns: the decoded message as a string of ASCII characters
    :raises Exception: if binaryStr's length is not a multiple of 8

    """
    if len(binaryStr) % 8:
        raise Exception("Binary string length is not a multiple of 8.")

    message = ""

    for i in range(8, len(binaryStr) + 1, 8):
        byteAsDecimal = int(binaryStr[i - 8 : i], 2)
        message += chr(byteAsDecimal)

    return message


def getHeaderLength(width, height, mode):
    """Get amount of bytes needed to store length of message before message content.

    :width: integer width of image
    :height: integer height of image
    :mode: string of mode of image (such as "RGB", "RGBA", etc.)
    :returns: amount of bytes needed to hide length of message in the "header" number,
    increased to be the next closest multiple of len(mode), which is how many bytes are
    per pixel

    """
    maxBytes = width * height * len(mode)
    rawAmount = len(bin(maxBytes)[2:])

    if rawAmount % len(mode):
        return int(rawAmount - rawAmount % len(mode) + len(mode))
    else:
        return int(rawAmount - rawAmount % len(mode))


def createCodeImage(filename, message):
    """Create copy of image with hidden message inside.

    :filename: name of image to make a copy of with message
    :message: message to hide into the image
    :returns: None

    """
    # gonna have to raise some errors if the message is too long for the image
    # and like if the image is a jpg or stuff that pillow can't deal with? Although
    # can't you just save those to png and they will work?

    img = Image.open(filename)

    headLength = getHeaderLength(img.width, img.height, img.mode)
    binMes = messageToBinary(message)
    paddedMesLength = bin(len(binMes))[2:].zfill(headLength)
    mesWithHeader = paddedMesLength + binMes

    if len(mesWithHeader) > img.width * img.height * len(img.mode):
        raise Exception("Message is too long to hide in image.")

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

    noExt = os.path.splitext(filename)[0]
    # need to force image into PNG to avoid JPG compression
    img.save(f"{noExt}_message.png")


def decodeImage(filename):
    """Extract message hidden in image with provided filename.

    :filename: name of image holding secret message
    :returns: extracted message from image

    """
    img = Image.open(filename)

    headLength = getHeaderLength(img.width, img.height, img.mode)
    tupLength = len(img.mode)
    binLength = ""

    # should definitely combine this with the next for loop lol
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

    return binaryToMessage(binMes)


if __name__ == "__main__":
    myMessage = """
alright, so I think that my codé works, although I definitely need to run some
more tests on it. Here is one of them, and I am glad that it looks like my program
is working fine so far. I could definitely hide a lot more text in larger images,
but I am afraid about how "well" Pillow could handle looping through millions of
pixels.
"""
    bigMes = """
lololololool cool, man, very cool!
Just one short sentence to hide in the images...
here is another command prompt.2$ python3 steg.py
NOT A TRACEBACK!!!! (most recent call last):
  File "steg.py", line 175, in <module>
    createCodeImage(fileName, myMessage)
  File "steg.py", line 88, in createCodeImage
    raise Exception("Message is too long to hide in image.")
Exception: Message is too long to hide in image.
xDDDDDD I did it again!

alright, so I think that my codé works, although I definitely need to run some
more tests on it. Here is one of them, and I am glad that it looks like my program
is working fine so far. I could definitely hide a lot more text in larger images,
but I am afraid about how "well" Pillow could handle looping through millions of
pixels.

Alright this is the last one

alright, so I think that my codé works, although I definitely need to run some
more tests on it. Here is one of them, and I am glad that it looks like my program
is working fine so far. I could definitely hide a lot more text in larger images,
but I am afraid about how "well" Pillow could handle looping through millions of
pixels.
"""
    shorterMes = "Just one short sentence to hide in the images..."
    superShort = "x"

    fileName = "../ss.png"
    createCodeImage(fileName, bigMes)
    print(decodeImage(fileName[:-4] + "_message" + ".png"))
