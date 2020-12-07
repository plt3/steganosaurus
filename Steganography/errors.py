class NonAsciiCharacterError(Exception):
    """
    Error to indicate that string contains non-ASCII character(s), meaning that it
    cannot be hidden into an image.
    """

    pass


class BinaryStringLengthError(Exception):
    """
    Error to indicate that binary string's length is not a multiple of 8, meaning that
    it cannot be decoded using ASCII.
    """

    pass


class MessageLengthError(Exception):
    """
    Error to indicate that message is too long to hide in chosen image.
    """

    pass


class NonPngImageError(Exception):
    """
    Error to indicate that specified output filename for Encoder.createCodeImage() or
    input file for Decoder.decodeImage() is not a PNG, which is only accepted message
    image filetype.
    """

    pass
