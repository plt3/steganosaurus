import os

import requests

from lorem import lorem
from Steganography import Decoder, Encoder


"""Basic testing suite for Steganography package"""


def downloadPictures():
    """piclist.txt should be a text file with a URL to an image per line"""

    urlFile = open("piclist.txt")

    for index, line in enumerate(urlFile):
        res = requests.get(line.strip())
        res.raise_for_status()

        with open(f"images/pic{index + 1}.jpg", "wb") as f:
            f.write(res.content)

        print(f"Downloaded image {index + 1}")

    urlFile.close()


def testPictures():
    enc = Encoder("placeholder")
    dec = Decoder("placeholder")

    for path in os.listdir("images/"):
        if not os.path.splitext(path)[1]:
            continue
        secretMessage = lorem(10000)
        picNum = os.path.splitext(path)[0][3:]
        fileOut = f"images/messages/message{picNum}.png"

        enc.setMessage(secretMessage)
        enc.createCodeImage("images/" + path, outputFile=fileOut)

        dec.setFilename(fileOut)
        returnedMes = dec.decodeImage()

        if secretMessage == returnedMes:
            print(f"Image {picNum} passed the test.")
        else:
            print(f"Image {picNum} failed :(")
            with open("errors/wrong{picNum}.txt", "w") as f:
                f.write(secretMessage)
                f.write("\n\n\n\n-----------------------\n\n\n\n")
                f.write(returnedMes)


if __name__ == "__main__":
    testPictures()
