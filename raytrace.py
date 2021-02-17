# raytrace.py -- Build a basic raytracer as described in Chapter 2 of
# Computer Graphics from Scratch by Gabriel Gambetta
import canvas
import math

class Sphere:
    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color

class Light:
    def __init__(self, lightType, intensity, position=None, direction=None):
        self.lightType = lightType
        self.intensity = intensity
        self.position = position
        self.direction = direction

def dot(u, v):
    total = 0
    for i in range(len(u)):
        total += u[i] * v[i]
    return total

def scalarMultiply(k, v):
    newV = [0] * len(v)

    for i in range(len(v)):
        newV[i] = v[i] * k

    return tuple(newV)

# Perform x - y on vectors
def vectorSum(x, y, difference=False):
    assert len(x) == len(y), "Vectors don't have the same length"

    vSum = [0] * len(x)

    for i in range(len(x)):
        if difference:
            vSum[i] = x[i] - y[i]
        else:
            vSum[i] = x[i] + y[i]

    return tuple(vSum)
    
def main():
    width = 600
    height = 600
    imageCanvas = canvas.Canvas(width, height)

    spheres = []
    spheres.append(Sphere((0, -1, 3), 1, canvas.Color(255, 0, 0)))
    spheres.append(Sphere((2, 0, 4), 1, canvas.Color(0, 0, 255)))
    spheres.append(Sphere((-2, 0, 4), 1, canvas.Color(0, 255, 0)))
    spheres.append(Sphere((0, -5001, 0), 5000, canvas.Color(255, 255, 0)))

    viewportWidth = 1
    viewportHeight = 1
    viewportZ = 1

    lights = []
    lights.append(Light("ambient", 0.2))
    lights.append(Light("point", 0.6, (2, 1, 0)))
    lights.append(Light("directional", 0.2, None, (1, 4, 4)))

    def canvasToViewport(x, y):
        return (x * viewportWidth / width, y * viewportHeight / height,
                viewportZ)

    def intersectRaySphere(origin, direction, sphere):
        r = sphere.radius
        circle_direction = vectorSum(origin, sphere.center, True)

        a = dot(direction, direction)
        b = 2 * dot(circle_direction, direction)
        c = dot(circle_direction, circle_direction) - r * r

        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return (float('inf'), float('inf'))

        t1 = (-b + math.sqrt(discriminant)) / (2 * a)
        t2 = (-b - math.sqrt(discriminant)) / (2 * a)

        return (t1, t2)

    def computeLighting(position, normal):
        i = 0.0

        for light in lights:
            if light.lightType == "ambient":
                i += light.intensity
            else:
                if light.lightType == "point":
                    L = vectorSum(light.position, position, True)
                else:
                    L = light.direction
 
                nDotL = dot(normal, L)
                if nDotL > 0:
                    i += light.intensity * nDotL / (len(normal) * len(L))

        return i

    def traceRay(origin, direction, tMin, tMax):
        closestT = float('inf')
        closestSphere = None

        for sphere in spheres:
            t1, t2 = intersectRaySphere(origin, direction, sphere)
            if t1 > tMin and t1 < tMax and t1 < closestT:
                closestT = t1
                closestSphere = sphere
            if t2 > tMin and t2 < tMax and t2 < closestT:
                closestT = t2
                closestSphere = sphere

        if not closestSphere:
            return canvas.Color(255, 255, 255)

        position = vectorSum(origin, scalarMultiply(closestT, direction))
        normal = vectorSum(position, closestSphere.center, True)
        normal = scalarMultiply(1.0 / len(normal), normal)

        finalColor = scalarMultiply(computeLighting(position, normal),
                                    closestSphere.color.vector())

        return canvas.Color(finalColor[0], finalColor[1], finalColor[2])

    origin = (0, 0, 0)
    for x in range(-width // 2, width // 2):
        for y in range(-height // 2, height // 2):
            direction = canvasToViewport(x, y)
            color = traceRay(origin, direction, 1, float('inf'))
            color.clamp()
            imageCanvas.putPixel(x, y, color)

    imageCanvas.convertToXPM2("raytracer_v2.xpm")

if __name__ == '__main__':
    main()
