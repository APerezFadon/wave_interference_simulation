import random
import math
import numpy as np

PI = 3.141592653589793

class Vector:
    def __init__(self, *args):
        if len(args) > 3 or len(args) < 2:
            raise ValueError("Must pass 2 or 3 arguments but {len(args)} were given")

        self.x = args[0]
        self.y = args[1]
        self.z = 0 if len(args) == 2 else args[2]


    def fromPolar(*args):
        if len(args) > 3 or len(args) < 2:
            raise ValueError("Must pass 2 or 3 arguments but {len(args)} were given")

        if len(args) == 2:
            x = args[0] * math.cos(args[1])
            y = args[0] * math.sin(args[1])
            z = 0
        else:
            x = args[0] * math.cos(args[1]) * math.sin(args[2])
            y = args[0] * math.sin(args[1]) * math.sin(args[2])
            z = args[0] * math.cos(args[2])
        return Vector(x, y, z)

    def fromCylindrical(*args):
        if len(args) > 3 or len(args) < 2:
            raise ValueError("Must pass 2 or 3 arguments but {len(args)} were given")

        if len(args) == 2:
            x = args[0] * math.cos(args[1])
            y = args[0] * math.sin(args[1])
            z = 0
        else:
            x = args[0] * math.cos(args[1])
            y = args[0] * math.sin(args[1])
            z = args[2]
        return Vector(x, y, z)


    def random2D():
        return Vector.fromPolar(1, random.random() * 2 * PI)

    def random3D():
        return Vector.fromPolar(1, random.random() * 2 * PI, random.random() * PI)


    def toString(self):
        return f"Vector({self.x}, {self.y}, {self.z})"

    def toList2D(self):
        return [self.x, self.y]

    def toList3D(self):
        return [self.x, self.y, self.z]

    def copyVector(self):
        return Vector(self.x, self.y, self.z)

    def equals(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def roundVector(self):
        return Vector(round(self.x), round(self.y), round(self.z))

    def constrainVector(self, lower, upper):
        prev_mag = self.getMagnitude()
        new_mag = prev_mag
        if prev_mag < lower:
            new_mag = lower
        elif upper != "infty":
            if prev_mag > upper:
                new_mag = upper
        return self.setMagnitude(new_mag)


    def __mul__(self, other):
        if type(other) == Vector:
            return self.x * other.x + self.y * other.y + self.z * other.z
        else:
            x = self.x * other
            y = self.y * other
            z = self.z * other
        return Vector(x, y, z)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Vector(x, y, z)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Vector(x, y, z)

    def __pow__(this, other):
        return Vector(this.y * other.z - this.z * other.y, this.z * other.x - this.x * other.z, this.x * other.y - this.y * other.x)


    def getMagnitude(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5

    def setMagnitude(self, new_mag):
        prev = self.toPolar()
        return Vector.fromPolar(new_mag, prev[1], prev[2])

    def normalize(self):
        return self.setMagnitude(1)

    def dist(self, other):
        return (self - other).getMagnitude()


    def toPolar(self):
        r = self.getMagnitude()
        phi = math.atan2(self.y, self.x)
        theta = math.atan2((self.x**2 + self.y**2)**0.5, self.z)
        return (r, phi, theta)

    def toCylindrical(self):
        rho = (self.x**2 + self.y**2)**0.5
        phi = math.atan2(self.y, self.x)
        return (rho, phi, self.z)

    def rotation_matrix_3d(axis, theta):
        rot_mat = [[math.cos(theta) + axis.x**2 * (1 - math.cos(theta)), axis.x * axis.y * (1 - math.cos(theta)) - axis.z * math.sin(theta), axis.x * axis.z * (1 - math.cos(theta)) + axis.y * math.sin(theta)], 
                   [axis.y * axis.x * (1 - math.cos(theta)) + axis.z * math.sin(theta), math.cos(theta) + axis.y**2 * (1 - math.cos(theta)), axis.y * axis.z * (1 - math.cos(theta)) - axis.x * math.sin(theta)], 
                   [axis.z * axis.x * (1 - math.cos(theta)) - axis.y * math.sin(theta), axis.z * axis.y * (1 - math.cos(theta)) + axis.x * math.sin(theta), math.cos(theta) + axis.z**2 * (1 - math.cos(theta))]]
        return rot_mat

    def rotateAboutAxis(self, axis, theta):
        rot_mat = Vector.rotation_matrix_3d(axis, theta)
        new = np.matmul(rot_mat, self.toList3D())
        return Vector(new[0], new[1], new[2])


Ihat = Vector(1, 0, 0)
Jhat = Vector(0, 1, 0)
Khat = Vector(0, 0, 1)
