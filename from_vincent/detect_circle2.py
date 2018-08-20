import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import scipy.signal as sig
from skimage import filter
import scipy.ndimage as ndimage
import scipy.ndimage.interpolation as ndii
from scipy import optimize
import scipy
from numpy.linalg import eig, inv
from matplotlib.patches import Ellipse
from PIL import Image
import cv2

def fit_ellipse(x,y):
    """Fit an ellipse through a set of points x[i], y[i]. 
    Returns the coefficients of the ellipse 
    (as a quadric a_0*x*x + a_1*x*y+a_2*y*y+a_3*x+a_4*y+a_5)."""
    x = x[:,np.newaxis]
    y = y[:,np.newaxis]
    D =  np.hstack((x*x, x*y, y*y, x, y, np.ones_like(x)))
    S = np.dot(D.T,D)
    C = np.zeros([6,6])
    C[0,2] = C[2,0] = 2; C[1,1] = -1
    E, V =  eig(np.dot(inv(S), C))
    n = np.argmax(np.abs(E))
    a = V[:,n]
    return a

def ellipse_center(a):
    """Given the coefficients of the ellipse, returns the center."""
    b,c,d,f,g,a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
    num = b*b-a*c
    x0=(c*d-b*f)/num
    y0=(a*f-b*d)/num
    return np.array([x0,y0])

def ellipse_angle_of_rotation( a ):
    """Given the coefficients of the ellipse, returns the angle of rotation."""
    b,c,d,f,g,a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
    return 0.5*np.arctan(2*b/(a-c))

def ellipse_axis_length( a ):
    """Given the coefficients of the ellipse, returns the length of the axes."""
    b,c,d,f,g,a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
    up = 2*(a*f*f+c*d*d+g*b*b-2*b*d*f-a*c*g)
    down1 = (b*b-a*c)*( (c-a)*np.sqrt(1+4*b*b/((a-c)*(a-c)))-(c+a))
    down2 = (b*b-a*c)*( (a-c)*np.sqrt(1+4*b*b/((a-c)*(a-c)))-(c+a))
    res1 = np.sqrt(up/down1)
    res2 = np.sqrt(up/down2)
    return np.array([res1, res2])

def find_center( initial_guess, edges, threshold ):
    """Given an initial guess for the center initial_guess and a list of points edges, 
    returns a cleaned list of edges where all edgepoints that are more than threshold*median away,
    Where median is the median distance of all given edges to the inital guess.
    """ 
    point_list =  np.transpose(np.where(edges==1))-initial_guess
    dist_list = np.sqrt(point_list[:,0]*point_list[:,0] + point_list[:,1]*point_list[:,1])
    avg = np.average(dist_list),np.std(dist_list), np.median(dist_list)
    point_indices =  np.where( np.abs(dist_list-np.median(dist_list))<threshold*np.median(dist_list))
    indices = point_list[point_indices] + initial_guess
    new_edges = np.zeros(edges.shape)
    for i in indices:
        new_edges[i[0],i[1]] = 1
    return new_edges, indices


def check_points(x,y,a, threshold):
    """Remove points that are far away from an ellipse with parameters a"""
    dist = (a[0]*x*x+a[1]*x*y+a[2]*y*y+a[3]*x+a[4]*y)/a[5]
    points = dist[np.where(np.abs(dist+1)<threshold)]
    indices = np.where(dist<-0.92)
    return x[indices], y[indices]

def find_ellipse(x,y):
    """
    center_estimate = 1024,1024 
    center_2, ier = optimize.leastsq(f_2, center_estimate)
    """
    treshold = 1.
    for i in range(2):
        a=fit_ellipse(x,y)
        xc_2, yc_2 = ellipse_center(a)
        treshold = treshold/(i+1)
        x,y = check_points(x,y,a, treshold)
    center = ellipse_center(a)
    axis = ellipse_axis_length(a)
    rotation_angle = ellipse_angle_of_rotation(a)
    print "Center: " + str(center)
    print "Axes: " + str(axis)
    print "Rotation angle: " + str(rotation_angle)
    return center, axis, rotation_angle

def find_circle(filename, show_image = True):
    im = np.asarray(Image.open(filename))
    ori = im
    im = im.copy()
    im = im[:, :, 0:1]
    im = im.reshape((im.shape[0], im.shape[1]))
    im = im[0:im.shape[1], 0:im.shape[1]]
    edges = cv2.Canny(im,150,350)
    edges[np.where(edges>0)]=1
    new_edges,point_indices =  find_center((im.shape[0]/2.0, im.shape[0]/2.0), np.copy(edges), .3)
    y = point_indices[:,0]
    x = point_indices[:,1]
    center, axis, rotation_angle = find_ellipse(x,y)
    for i in range(0,80):
        new_edges,point_indices =  find_center((center[1], center[0]), np.copy(new_edges), .5/(1+2*i))
        y = point_indices[:,0]
        x = point_indices[:,1]
        center, axis, rotation_angle = find_ellipse(x,y)
    if show_image:
        plt.subplot(131)
        plt.imshow(ori, cmap=plt.cm.rainbow)#, vmin=0)#,vmax=np.max(im))
        circle1=plt.Circle((center[0],center[1]),np.max(axis),ec='r',fc='none')
        ell = Ellipse(xy=center, width=2*axis[0], height=2*axis[1], fc='none', ec='b', angle=rotation_angle)
        fig = plt.gcf()
        fig.gca().add_artist(ell)
        fig.gca().add_artist(circle1)
        plt.axis('off')
        plt.title('noisy image', fontsize=20)

        plt.subplot(132)
        plt.imshow(edges, cmap=plt.cm.gray)
        plt.axis('off')
        plt.title('Rough filter', fontsize=20)
        plt.subplot(133)
        plt.imshow(new_edges, cmap=plt.cm.gray)
        ell = Ellipse(xy=center, width=2*axis[0], height=2*axis[1], fc='none', ec='r', angle=rotation_angle)
        fig = plt.gcf()
        plt.axis('off')
        plt.title('Finer filter', fontsize=20)


        plt.subplots_adjust(wspace=0.02, hspace=0.02, top=0.9,
                            bottom=0.02, left=0.02, right=0.98)

        plt.show()
    return center, axis[0],axis[1], rotation_angle

if __name__ == "__main__":
    print find_circle("sp.jpg")
