# This module lifts the triangulated locations of Mars onto the estimated
# Orbital Plane, and then fits both a circle and an ellipse for the Mars
# orbit in order to compare the two. 

# Developed by Pulkit Singh, Niheshkumar Rathod & Rajesh Sundaresan
# Copyright lies with the Robert Bosch Center for Cyber-Physical Systems,
# Indian Institute of Science, Bangalore, India.

#----------------------------------------------------------------------------#

import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Ellipse

# importing custom module to run gradient descent on elliptical mars orbit
import ellipseGradientDescent 

#----------------------------------------------------------------------------#

def liftCoordinates(planeParams, marsTriLocations):

	a, b = planeParams

	# x-y coordinates of Mars will be the same as the projections
	# to calculate z coordinates, we must use the formula as follows:
	# zMars = (-a * xMars) + (-b * yMars), where a and b are the parameters
	# of the best-fit plane
	liftedLocations = []
	for location in marsTriLocations:
		xMars, yMars = location
		zMars = (-1 * a * xMars) + (-1 * b * yMars)
		liftedLocations.append([xMars, yMars, zMars])
	
	return liftedLocations

#----------------------------------------------------------------------------#

def fitCircle(coordinates):

	# Finding the distance of each point from the origin
	rMars = []
	for location in coordinates:
		xMars, yMars, zMars = location
		sqDist = math.pow(xMars, 2) + math.pow(yMars, 2) + math.pow(zMars, 2)
		rMars.append(math.sqrt(sqDist))

	# Finding the average radius, which is the radius of the best fit circle
	r = sum(rMars) / len(rMars)

	# Computing the sum of losses
	loss = 0.0 
	for radius in rMars:
		loss = loss + math.pow((r - radius), 2)

	return r, loss

#----------------------------------------------------------------------------#

def fitEllipse(coordinates):
	xMars, yMars, zMars = [], [], []
	for location in coordinates:
		x, y, z = location
		xMars.append(x); yMars.append(y); zMars.append(z)

	# initialising parameters for x-y coordinates of focus major axis length
	xf1, yf1, axis1 = 0.0, 0.0, 0.0

	# finding the best fit ellipse
	xf, yf, axis, cost = ellipseGradientDescent.findEllipse(xMars, yMars, 
		xf1, yf1, axis1)

	ellipseParameters = [xf, yf, axis]
	return ellipseParameters, cost[-1]

#----------------------------------------------------------------------------#

def plotBoth(coordinates, circleRadius, ellipseParameters):

	xMars, yMars, zMars = [], [], []
	for location in coordinates:
		x, y, z = location
		xMars.append(x); yMars.append(y); zMars.append(z)

	# unpacking ellipse parameters
	xf, yf, axis = ellipseParameters

	# calculating values to plot ellipse
	centerX = xf / 2.0
	centerY = yf / 2.0
	interFocii = math.sqrt(math.pow(xf, 2) + math.pow(yf, 2))
	minorAxis = math.sqrt(math.pow(axis, 2) - math.pow(interFocii, 2))
	rotationAngle = 360 - math.degrees(math.atan(yf / abs(xf)))

	# plotting cost as a function of number of iterations 
	#plt.plot(cost)
	#plt.show()

	# creating a plot
	fig, ax = plt.subplots()

	# plotting mars locations and the focii
	ax.plot(xMars, yMars, "ro")
	ax.plot(0.0, 0.0, "yo", label="Sun")
	ax.plot(xf, yf, "go", label="Ellipse Focus #2")

	# adding best fit circle
	fit_c = plt.Circle((0,0), circleRadius, color='c', fill=False, 
		label="Best-fit Circle")
	ax.add_artist(fit_c)

	# adding best fit ellipse
	fit_e = Ellipse((centerX, centerY), axis, minorAxis, rotationAngle, 
		color='b', fill=False)
	ax.add_artist(fit_e)

	# setting dimensions of the plot
	ax.set_xlim(-2.2, 2.2)
	ax.set_ylim(-2.2, 2.2)
	ax.set_aspect('equal')

	# updating legend 
	ax.legend([fit_c, fit_e], ['Best-fit Circle', 'Best-fit Ellipse'], 
		fontsize='x-small')

	plt.show()
#----------------------------------------------------------------------------#
