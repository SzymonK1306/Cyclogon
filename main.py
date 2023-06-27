import numpy as np
import matplotlib; matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from matplotlib import animation


# calculate value of given function (curve)
def calculate_function(x):
    return eval(y_string)


# animate single frame in animation
def animation_frame(i):

    # get values from previous frame
    triangle_x = vertices.get_xdata()
    triangle_y = vertices.get_ydata()

    rotation_pointX = rotation_point_plot.get_xdata()
    rotation_pointY = rotation_point_plot.get_ydata()

    radius = radius_plot.get_xdata()

    # calculate angle to rotation
    rotation = np.arctan2(triangle_y - rotation_pointY, triangle_x - rotation_pointX) - step

    # set nev vertices of triangle
    triangle_x = np.cos(rotation)*radius + rotation_pointX
    triangle_y = np.sin(rotation)*radius + rotation_pointY

    # calculate center of triangle
    center_x = (triangle_x[0]+triangle_x[1]+triangle_x[2])/3
    center_y = (triangle_y[0] + triangle_y[1] + triangle_y[2]) / 3

    # add cyclogon points
    cycX.append(triangle_x[1])
    cycY.append(triangle_y[1])

    # calculate sides of rectangle
    a_triangleX = np.linspace(triangle_x[0], triangle_x[1], 100)
    a_triangleY = np.linspace(triangle_y[0], triangle_y[1], 100)
    b_triangleX = np.linspace(triangle_x[1], triangle_x[2], 100)
    b_triangleY = np.linspace(triangle_y[1], triangle_y[2], 100)
    c_triangleX = np.linspace(triangle_x[2], triangle_x[0], 100)
    c_triangleY = np.linspace(triangle_y[2], triangle_y[0], 100)

    full_x = np.concatenate((a_triangleX, b_triangleX, c_triangleX), axis=0)
    full_y = np.concatenate((a_triangleY, b_triangleY, c_triangleY), axis=0)

    # find collision between triangle and curve
    collision_points = list(np.where(full_y <= calculate_function(full_x)))

    if len(collision_points[0]) > 1:
        # change rotation center
        collision_x = np.take(full_x, collision_points[0])
        x_max = np.argmax(collision_x)
        rotation_pointX = full_x[collision_points[0][x_max]]
        rotation_pointY = full_y[collision_points[0][x_max]]
        radius = np.sqrt(np.square(triangle_x - rotation_pointX) + np.square(triangle_y - rotation_pointY))

    # set plots
    triangle.set_xdata(full_x)
    triangle.set_ydata(full_y)

    cyclogon.set_xdata(cycX)
    cyclogon.set_ydata(cycY)

    point.set_xdata(center_x)
    point.set_ydata(center_y)

    line.set_xdata([center_x, triangle_x[1]])
    line.set_ydata([center_y, triangle_y[1]])

    vertices.set_xdata(triangle_x)
    vertices.set_ydata(triangle_y)

    rotation_point_plot.set_xdata(rotation_pointX)
    rotation_point_plot.set_ydata(rotation_pointY)

    radius_plot.set_xdata(radius)

    return cyclogon, triangle, point, line, vertices, rotation_point_plot, radius,


if __name__ == '__main__':
    a = input('Enter a value: ')
    b = input('Enter b value: ')
    c = input('Enter c value: ')

    a = float(a)
    b = float(b)
    c = float(c)

    x_low = input('Enter lower bound of x: ')
    x_upp = input('Enter upper bound of x: ')
    x = np.arange(float(x_low), float(x_upp), 0.005)
    y_string = input('Enter function: ')
    y = calculate_function(x)

    # cyclogon lists
    cycX = []
    cycY = []

    alfa = np.arccos((c**2+b**2-a**2)/(2*c*b))

    step = np.pi/100

    triangle_x = np.array([0, -c * np.sin(alfa), 0]) + x[0]
    triangle_y = np.array([b, c * np.cos(alfa), 0]) + y[0]

    center_x = (triangle_x[0] + triangle_x[1] + triangle_x[2]) / 3
    center_y = (triangle_y[0] + triangle_y[1] + triangle_y[2]) / 3

    rotation_pointX = triangle_x[2]
    rotation_pointY = triangle_y[2]

    radius = np.sqrt(np.square(triangle_x-rotation_pointX)+np.square(triangle_y-rotation_pointY))

    # plots
    fig, ax = plt.subplots()
    triangle, = plt.plot(0, 0, color='g')
    point, = ax.plot(center_x, center_y, marker='o', color='r')
    cyclogon, = plt.plot(0, 0, color='m')
    curve, = plt.plot(x, y, color='b')
    line, = plt.plot(0, 0, color='r')
    vertices, = plt.plot(triangle_x, triangle_y, marker='o', markerfacecolor='None', linestyle='None', color='g')
    rotation_point_plot, = plt.plot(rotation_pointX, rotation_pointY, marker='o', color='g')
    radius_plot, = plt.plot(radius, [0, 0, 0], linestyle='None')
    ax.set_aspect('equal')
    ax.set_xlim(min(x)-max(radius), max(x))
    ax.set_ylim(min(y)-1, max(y)+max(radius)+3)

    animation = animation.FuncAnimation(fig, func=animation_frame, frames=int(len(x)/step), interval=1, repeat=False)
    plt.show()
