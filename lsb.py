#! /usr/bin/python3
from PIL import Image
import sys

def getChannelIdx(i, channels):
    c = channels[i]
    if (c == "r"):
        return 0
    elif (c == "g"):
        return 1
    elif (c == "b"):
        return 2
    elif (c == "a"):
        return 3
    else:
        assert False, "Invalid channel char, expected 'rgba' got %s" % c

def main():
    if (len(sys.argv) < 3):
        print("usage: %s <filename> <output-filename> [optional: channels(rgba)]" % sys.argv[0])
        return

    channels = "rgba" if len(sys.argv) == 3 else sys.argv[3]
    channelCount = len(channels)
    
    im = Image.open(sys.argv[1])
    outsize = (im.width * im.height * channelCount) // 4
    print("analazying %d channels (%s) of %s image of size: %s (outputsize: %d)..." %(channelCount, channels, im.format, im.size, outsize))

    out = bytearray(outsize)
    for h in range(im.height):
        for w in range(im.width):
            pixelIdx = h * im.width + w
            p = im.getpixel((w, h))
            for i in range(channelCount):
                chanIdx = getChannelIdx(i, channels)
                lsb = p[chanIdx] & 0x1
                byteIdx = pixelIdx // (5 - channelCount)
                byteOff = pixelIdx % (5 - channelCount)
                out[byteIdx] = out[byteIdx] | (lsb << byteOff)
    outfile = open(sys.argv[2], "wb+")
    outfile.write(out)
    outfile.close()

    print("[done] wrote %d bytes to file %s" % (len(out), sys.argv[2]))

if __name__ == "__main__":
    main()
