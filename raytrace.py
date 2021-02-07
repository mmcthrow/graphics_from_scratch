# raytrace.py -- Build a basic raytracer as described in Chapter 2 of
# Computer Graphics from Scratch by Gabriel Gambetta
import canvas
import math

class Sphere:
    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color

def dot(u, v):
    total = 0
    for i in range(len(u)):
        total += u[i] * v[i]
    return total

def main():
    width = 600
    height = 600
    imageCanvas = canvas.Canvas(width, height)

    spheres = []
    spheres.append(Sphere((0, -1, 3), 1, canvas.Color(255, 0, 0)))
    spheres.append(Sphere((2, 0, 4), 1, canvas.Color(0, 0, 255)))
    spheres.append(Sphere((-2, 0, 4), 1, canvas.Color(0, 255, 0)))

    viewportWidth = 1
    viewportHeight = 1
    viewportZ = 1

    def canvasToViewport(x, y):
        return (x * viewportWidth / width, y * viewportHeight / height,
                viewportZ)

    def intersectRaySphere(origin, direction, sphere):
        r = sphere.radius
        circle_direction = (origin[0] - sphere.center[0],
                            origin[1] - sphere.center[1],
                            origin[2] - sphere.center[2])

        a = dot(direction, direction)
        b = 2 * dot(circle_direction, direction)
        c = dot(circle_direction, circle_direction) - r * r

        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return (float('inf'), float('inf'))

        t1 = (-b + math.sqrt(discriminant)) // (2 * a)
        t2 = (-b - math.sqrt(discriminant)) // (2 * a)

        return (t1, t2)

    def traceRay(origin, direction, tMin, tMax):
        closestT = float('inf')
        closestSphere = None

        for sphere in spheres:
            t1, t2 = intersectRaySphere(origin, direction, sphere)
            if t1 >= tMin and t1 <= tMax and t1 < closestT:
                closestT = t1
                closestSphere = sphere
            if t2 >= tMin and t2 <= tMax and t2 < closestT:
                closestT = t2
                closestSphere = sphere

        if not closestSphere:
            return canvas.Color(255, 255, 255)

        return closestSphere.color

    origin = (0, 0, 0)
    for x in range(-width // 2, width // 2):
        for y in range(-height // 2, height // 2):
            direction = canvasToViewport(x, y)
            color = traceRay(origin, direction, 1, float('inf'))
            imageCanvas.putPixel(x, y, color)

    imageCanvas.convertToXPM("raytracer.xpm")

if __name__ == '__main__':
    main()
