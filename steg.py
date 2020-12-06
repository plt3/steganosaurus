from stegClass import Decoder, Encoder
from testMessages import bigMes

"""
TODO: Make ArgParser, rearrange everything in package structure?

oh and make ersatz unit tests by downloading photos and then checking that a message gets correctly read and stuff
"""

if __name__ == "__main__":
    # coder = Encoder(bigMes)

    # coder.createCodeImage("../ss.png", outputFile="../ssTest.png")
    # coder.createCodeImage("../Whiteboard[1]-01.png")
    # coder.setMessage(bigMes)
    # coder.createCodeImage("../republic_wireless_app.png", outputFile="../appYolo.png")

    decode = Decoder("../app.png")
    mes = decode.decodeImage()
    print(mes)
    decode.setFilename("../Whiteboard[1]-01_message.png")
    mes = decode.decodeImage()
    print("---------------------------")
    print(mes)
