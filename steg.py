from stegClass import Decoder, Encoder
from testMessages import bigMes

"""
TODO: fix docstrings in stegClass, add encoded filename option to createCodeImage, make ArgParser
rearrange everything in package structure?

oh and make ersatz unit tests by downloading photos and then checking that a message gets correctly read and stuff
"""

if __name__ == "__main__":
    coder = Encoder(bigMes)

    coder.createCodeImage("../ysengrin_hersant_accusation.png")

    decode = Decoder("../ysengrin_hersant_accusation_message.png")
    mes = decode.decodeImage()
    print(mes)
