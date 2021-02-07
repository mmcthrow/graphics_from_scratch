# canvas.py -- Provides a bitmap canvas for drawing purposes.  This canvas
# can be converted to XPM (and perhaps other formats in the future.)

class Color:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __str__(self):
        return "{:02x}{:02x}{:02x}".format(self.red, self.green, self.blue)

class Pixel:
    def __init__(self, color):
        self.color = color

class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = [Pixel(Color(255, 255, 255)) for x in range(0, width * height)]

    def toSx(self, x):
        return (self.width // 2) + x

    def toSy(self, y):
        return (self.height // 2) - y - 1

    def colors(self):
        colors = {}
        namesToColors = {}
        colorCount = 0
        for pixel in self.pixels:
            colorStr = str(pixel.color)
            if colorStr not in colors:
                colors[colorStr] = colorCount
                namesToColors[colorCount] = colorStr
                colorCount += 1

        return (colors, namesToColors)

    def putPixel(self, x, y, color):
        print("x = {}, y = {}".format(x,y))
        index = self.toSy(y) * self.height + self.toSx(x)
        print("index = {}".format(index))
        self.pixels[index].color = color

    def convertToXPM(self, filename):
        formatHeader = "#define XFACE_format 1"
        widthHeader = "#define XFACE_width {}".format(self.width)
        heightHeader = "#define XFACE_height {}".format(self.height)
        colorsToNames, namesToColors = self.colors()
        numColorsHeader = "#define XFACE_ncolors {}".format(len(colorsToNames))
        charsNeeded = 0
        currentLength = len(colorsToNames)
        while currentLength > 0:
            charsNeeded += 1
            currentLength = currentLength // 10

        charsPerPixelHeader = "#define XFACE_chars_per_pixel {}".format(charsNeeded)
        colorsEntry = "static char *XFACE_colors[] = {{\n{}\n}};".format(",\n".join(["\"{}\", \"#{}\"".format(str(name).zfill(charsNeeded), code) for name, code in namesToColors.items()]))
        pixelsEntryFormat = "static char *XFACE_pixels[] = {{\n{}\n}};"
        pixels = []
        for y in range(self.height):
            row = "";
            for x in range(self.width):
                row += str(colorsToNames[str(self.pixels[y * self.height + x].color)]).zfill(charsNeeded)
            pixels.append("\"{}\"".format(row))
        pixelStr = ",\n".join(pixels)
        pixelsEntry = pixelsEntryFormat.format(pixelStr)

        outputFile = open(filename, 'w')
        outputFile.write(formatHeader + '\n' + widthHeader + '\n' +
                         heightHeader + '\n' + numColorsHeader + '\n' +
                         charsPerPixelHeader + '\n' + colorsEntry + '\n' +
                         pixelsEntry)
        outputFile.close()
