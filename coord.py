import math

def from_cartesian_to_spherical(x, y, z):
    
    r = math.sqrt(math.pow(x,2) +
                  math.pow(y,2) +
                  math.pow(z,2))

    theta = math.acos(z/r)
    phi = math.atan(y/x)

    return r, theta, phi


def from_spherical_to_cartesian(r, theta, phi):

    x = r * math.sin(theta*3.14/180) * math.cos(phi*3.14/180)
    y = r * math.sin(theta*3.14/180) * math.sin(phi*3.14/180)
    z = r * math.cos(theta*3.14/180)

    return x, y, z

def put_on_sphere(x, y, radius):

    z = math.sqrt( math.pow(radius, 2) -
                   math.pow(y,2) - math.pow(x,2))
    
    return z


def put_on_sphere_DS(x, y, radius):

    z = (math.tan(math.acos(( math.sqrt(math.pow(x,2) +
                                       math.pow(y,2)))/radius)) *
         (math.sqrt(math.pow(x, 2) +
                    math.pow(y, 2))))
    
    return z




