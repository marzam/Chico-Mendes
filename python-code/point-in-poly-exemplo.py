#! /home/mzamith/Apps/anaconda3/bin/python
import numpy as np
'''
p1 and p2 are polygon Coordinate
p4x is maximum value used to cal if point in or out
b2 is b value of second line
'''
def point_in_poly_faster(p1x, p1y, p2x, p2y, p4x, b2):
    is_in = True
    print('\t\t point_in_poly_faster:')
    # first line
    if abs(p2x - p1x) < 1E-20:
        a1 = 0
    else:
        a1 = (p2y - p1y) / (p2x - p1x)

    b1 = (p1y +(-p1x * a1)) * -1

#    print('b1: ', b1)#
#    print('b2: ', b2)
#    print('a1: ', a1)
#    print('b1+b2: ', (b1 + b2))

    x = (b1 + b2) / (a1)
    y = b2

    scale_x = (p2x - x) / (p2x - p1x)
    scale_y =  (p2y - y) /  (p2y - p1y)
    scale_xx = (p4x - x) / (p4x - p3x)

    if scale_x < 0 or scale_x > 1:
        is_in = False

    if scale_y < 0 or scale_y > 1:
        is_in = False

    if scale_xx < 0 or scale_xx > 1:
        is_in = False


    print('\t point: ', x, ' ', y)
    print('\t scale: ', scale_x, ' ', scale_y)

    return is_in

'''
p1 and p2 are polygon Coordinate
p4x is maximum value used to cal if point in or out
b2 is b value of second line
'''
def point_in_poly_fast(p1x, p1y, p2x, p2y, p4x, b2):
    is_in = True
    # first line
    if abs(p2x - p1x) < 1E-20:
        a1 = 0
    else:
        a1 = (p2y - p1y) / (p2x - p1x)

    b1 = p1y +(-p1x * a1)


#a2 value is always zero, there is no angle
    A = np.array([[a1,-1],[0,-1]])
    B = np.array([[-b1],[-b2]])
    A_I = np.linalg.inv(A) #Função que encontra a matriz inversa
    X = np.dot(A_I,B)
    x = X[0][0]
    y = X[1][0]

    scale_x = (p2x - x) / (p2x - p1x)
    scale_y =  (p2y - y) /  (p2y - p1y)
    scale_xx = (p4x - x) / (p4x - p3x)

    if scale_x < 0 or scale_x > 1:
        is_in = False

    if scale_y < 0 or scale_y > 1:
        is_in = False

    if scale_xx < 0 or scale_xx > 1:
        is_in = False

    print('\t point: ', x, ' ', y)
    print('\t scale: ', scale_x, ' ', scale_y)

    return is_in
#-------------------------------------------------------------------------------

def point_in_poly(p1x, p1y, p2x, p2y, p3x, p3y, p4x, p4y):
    is_in = True
    # first line
    if abs(p2x - p1x) < 1E-20:
        a1 = 0
    else:
        a1 = (p2y - p1y) / (p2x - p1x)

    #second line
    #if abs(p4x - p3x) < 1E-20:
    a2 = 0
    #else:
#        a2 = (p4y - p3y) / (p4x - p3x)

    b1 = p1y +(-p1x * a1)
    b2 = p3y +(-p3x * a2)

    A = np.array([[a1,-1],[a2,-1]])
    B = np.array([[-b1],[-b2]])
    A_I = np.linalg.inv(A) #Função que encontra a matriz inversa
    X = np.dot(A_I,B)

    #print(A)
    #print(B)

    x = X[0][0]
    y = X[1][0]

    scale_x = (p2x - x) / (p2x - p1x)
    scale_y =  (p2y - y) /  (p2y - p1y)
    scale_xx = (p4x - x) / (p4x - p3x)

    if scale_x < 0 or scale_x > 1:
        is_in = False

    if scale_y < 0 or scale_y > 1:
        is_in = False

    if scale_xx < 0 or scale_xx > 1:
        is_in = False

    print('\t point: ', x, ' ', y)
    print('\t scale: ', scale_x, ' ', scale_y)

    return is_in
#-------------------------------------------------------------------------------
# first line
p1x = 5
p1y = 3
p2x = 2
p2y = 1
a1 = (p2y - p1y) / (p2x - p1x)


#second line
p3x = 5.001
p3y = 3.00
p4x = -p3x
p4y = p3y
a2 = 0 #(p4x - p3x) / (p4y - p3y)
#b2 = p3y +(-p3x * a2)
#def point_in_poly_fast(p1x, p1y, p2x, p2y, p4x, b2):
#print('>    fast:  ', point_in_poly_fast(p1x, p1y, p2x, p2y, p4x, p3y))
print('>   usual: ', point_in_poly(p1x, p1y, p2x, p2y, p3x, p3y, p4x, p4y))
print('> faster:  ',  point_in_poly_faster(p1x, p1y, p2x, p2y, p4x, p3y))
