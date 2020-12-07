import argparse

from Steganography import Decoder, Encoder

DESCRIPTION = "Python implementation of least significant bit steganography technique"


def parserSetup():
    """Create argparse.ArgumentParser object with correct arguments for CLI.

    :returns: argparse.ArgumentParser instance with all arguments already set

    """
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        "filename", help="Path of file to encode message into/decode message from"
    )

    encodeDecode = parser.add_mutually_exclusive_group(required=True)
    encodeDecode.add_argument(
        "-e",
        "--encode",
        help="Flag to encode a message into an image",
        action="store_true",
    )
    encodeDecode.add_argument(
        "-d",
        "--decode",
        help="Flag to extract hidden message from an image",
        action="store_true",
    )

    parser.add_argument(
        "-m", "--message", help="Message to hide if encoding into image"
    )
    parser.add_argument(
        "-o",
        "--outputfile",
        help="File path to save encoded image to or to write decoded message to",
    )
    parser.add_argument(
        "-i",
        "--inputfile",
        help="File path to plaintext file holding message to encode",
    )

    return parser


def main():
    """Get argparse.ArgumentParser instance and execute correct actions based on
    command line arguments.

    """
    cliParser = parserSetup()
    args = cliParser.parse_args()

    if args.encode:
        # this means that program should encode a message into image
        if args.inputfile:
            with open(args.inputfile) as f:
                fullMessage = f.read()
        elif args.message:
            fullMessage = args.message
        else:
            cliParser.error("Use either --message or --inputfile with --encode.")

        coder = Encoder(fullMessage)
        imagePath = coder.createCodeImage(args.filename, args.outputfile)

        print(f"Message successfully hidden in {imagePath}.")
    elif args.decode:
        # this means that program should decode message from image
        if args.message or args.inputfile:
            cliParser.error("Cannot use --message or --inputfile with --decode.")

        decode = Decoder(args.filename)
        foundMessage = decode.decodeImage()

        if args.outputfile:
            with open(args.outputfile, "w") as f:
                f.write(foundMessage)

            print(f"Message successfully written to {args.outputfile}.")
        else:
            print(foundMessage)


if __name__ == "__main__":
    main()
