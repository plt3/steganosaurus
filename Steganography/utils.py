def getHeaderLength(width, height, mode):
    """Get amount of bytes needed to store length of message before message content.

    :width: integer width of image
    :height: integer height of image
    :mode: string of mode of image (such as "RGB", "RGBA", etc.)
    :returns: amount of bytes needed to hide length of message in the "header" number,
        increased to be the next closest multiple of len(mode), which is how many bytes
        are per pixel

    """
    maxBytes = width * height * len(mode)
    rawAmount = len(bin(maxBytes)[2:])

    if rawAmount % len(mode):
        return int(rawAmount - rawAmount % len(mode) + len(mode))
    else:
        return int(rawAmount - rawAmount % len(mode))
