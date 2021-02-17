# canvas.py -- Provides a bitmap canvas for drawing purposes.  This canvas
# can be converted to XPM (and perhaps other formats in the future.)

class Color:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __str__(self):
        return "{:02x}{:02x}{:02x}".format(int(self.red), int(self.green), int(self.blue))

    def vector(self):
        return (self.red, self.green, self.blue)

    def clamp(self):
        self.red = min(255, max(0, self.red))
        self.green = min(255, max(0, self.green))
        self.blue = min(255, max(0, self.blue))

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

        print("Number of Unique Colors: {}".format(colorCount))
        print("Colors: {}".format(list(map(lambda c: "#{}".format(c), colors.keys()))))

        return (colors, namesToColors)

    def putPixel(self, x, y, color):
        #print("x = {}, y = {}".format(x,y))
        index = self.toSy(y) * self.height + self.toSx(x)
        #print("index = {}".format(index))
        self.pixels[index].color = color

    def computeCharsNeeded(self, colorsToNames):
        charsNeeded = 0
        currentLength = len(colorsToNames)
        while currentLength > 0:
            charsNeeded += 1
            currentLength = currentLength // 10

        return charsNeeded

    def makePixelsStr(self, charsNeeded, colorsToNames, xpmVersion):
        pixels = []
        for y in range(self.height):
            row = "";
            for x in range(self.width):
                row += str(colorsToNames[str(self.pixels[y * self.height + x].color)]).zfill(charsNeeded)
            if xpmVersion == 1:
                pixels.append("\"{}\"".format(row))
            else:
                pixels.append("{}".format(row))
        if xpmVersion == 1:
            pixelsStr = ",\n".join(pixels)
        else:
            pixelsStr = "\n".join(pixels)
        return pixelsStr

    def convertToXPM1(self, filename):
        formatHeader = "#define XFACE_format 1"
        widthHeader = "#define XFACE_width {}".format(self.width)
        heightHeader = "#define XFACE_height {}".format(self.height)
        colorsToNames, namesToColors = self.colors()
        numColorsHeader = "#define XFACE_ncolors {}".format(len(colorsToNames))
        charsNeeded = self.computeCharsNeeded(colorsToNames)
        charsPerPixelHeader = "#define XFACE_chars_per_pixel {}".format(charsNeeded)
        colorsEntry = "static char *XFACE_colors[] = {{\n{}\n}};".format(",\n".join(["\"{}\", \"#{}\"".format(str(name).zfill(charsNeeded), code) for name, code in namesToColors.items()]))
        pixelsEntryFormat = "static char *XFACE_pixels[] = {{\n{}\n}};"
        pixelsStr = self.makePixelsStr(charsNeeded, colorsToNames, 1)
        pixelsEntry = pixelsEntryFormat.format(pixelsStr)

        outputFile = open(filename, 'w')
        outputFile.write(formatHeader + '\n' + widthHeader + '\n' +
                         heightHeader + '\n' + numColorsHeader + '\n' +
                         charsPerPixelHeader + '\n' + colorsEntry + '\n' +
                         pixelsEntry)
        outputFile.close()

    def convertToXPM2(self, filename):
        formatHeader = "! XPM2"
        colorsToNames, namesToColors = self.colors()
        charsNeeded = self.computeCharsNeeded(colorsToNames)
        defHeader = "{} {} {} {}".format(self.width, self.height, len(colorsToNames), charsNeeded)
        colorsEntry = "\n".join(["{} c #{}".format(str(name).zfill(charsNeeded), code) for name, code in namesToColors.items()])
        pixelsStr = self.makePixelsStr(charsNeeded, colorsToNames, 2)
        
        outputFile = open(filename, 'w')
        outputFile.write(formatHeader + '\n' + defHeader + '\n' +
                         colorsEntry + '\n' + pixelsStr)
        outputFile.close()
