from visual import *
from random import uniform
from visual.controls import *

# initiate the scene
scene = display(title = 'Solar System Simulation', x = 400, y = 150, width = 1080, height = 720)

# timestep (in seconds)
dt = 60 * 15
# loop counter
step = 5
# limit the simulation to a certain number of iterations
maxstep = 1000000
# number of steps to wait before checking the area
month = 700

# define the gravitational constant for use in Newton's law of gravitation
G = 6.674E-11

# choose the numerical method to use, options are:
# Velocity Verlet = "vv"
# Euler-Cromer = "e-c"
method = "vv" 

# create an array for the planets and their respective curves and labels
planetArray = []
curveArray = []
labelArray = []

# define a function to add a planet to the planet array
def addPlanet(name, mass, position, velocity, radius):

    # generate a random colour for the planet and trail
    randColour = (uniform(0,1), uniform(0,1), uniform(0,1))

    # create the actual visual object
    planetToAdd = sphere(pos = position, lastPos = position, radius = radius, color = randColour)

    # define the planet's mass, acceleration and positions for calculations later
    planetToAdd.v = velocity
    planetToAdd.m = mass
    planetToAdd.a = vector(0, 0, 0)

    # add the planet to the planet array
    planetArray.append(planetToAdd)

    # create a curve for the planet and add this to the curve array
    curveToAdd = curve(color = randColour)
    curveArray.append(curveToAdd)
    
    # create a label for the planet and add it to the label array
    labelToAdd = label(pos = planetToAdd.pos, text = name, xoffset = 20, yoffset = 20, height = 20, border = 3)
    labelArray.append(labelToAdd)

# Sun
addPlanet("Sun", 1.99E30, vector(0, 0, 0), vector(0, 0, 0), 6.96E8)

# Mercury
addPlanet("Mercury", 3.285E23, vector(0, 69.8E9, 0), -vector(38.86E3, 0, 0), 2.44E3)

# Venus
addPlanet("Venus", 4.867E24, vector(0, -108E9, 0), -vector(-34.79E3, 0, 0), 6.3E6)

# Earth
addPlanet("Earth", 5.97E24, vector(0, 152E9, 0), -vector(29.3E3, 0, 0), 6.3E6)

# Moon
addPlanet("Moon", 7.43E22, vector(0, 152E9 + 4E8, 0), -vector(29.3E3 + 0.964E3, 0, 0), 1.7E6)

# Mars
addPlanet("Mars", 6.41E23, vector(0, 249E9, 0), -vector(21.97E3, 0, 0), 3.3E6)

# Jupiter
addPlanet("Jupiter", 1898E24, vector(0, -816E9, 0), -vector(-12.44E3, 0, 0), 66E6)

# Saturn
addPlanet("Saturn", 568E24, vector(0, 1514E9, 0), -vector(9.09E3, 0, 0), 54E6)

# Uranus
addPlanet("Uranus", 86.813E24, vector(0, -3003E9, 0), -vector(-6.49E3, 0, 0), 24E6)

# Neptune
addPlanet("Neptune", 102E24, vector(0, 4545E9, 0), -vector(5.37E3, 0, 0), 24E6)

# Pluto
addPlanet("Pluto", 0.01303E24, vector(0, -7376E9, 0), -vector(-3.71E3, 0, 0), 1.2E6)

# which planet/star to use for testing Kepler's second law
starID = 0

# setup the scene view for easier viewing/navigation
scene.up = vector(0, 0, 1)
scene.autoscale = False

while step <= maxstep:

    # slow down the animation
    rate(96 * 7)

    # loop through all the planets in the array
    for i in range(0, len(planetArray)):

        # define/reset the net force on the planet
        planetArray[i].f = vector(0, 0, 0)

        # loop through the planet array again
        for i2 in range(0, len(planetArray)):

            # stop self interaction
            if i == i2:
                continue

            # determine the vector between the two planets
            r = planetArray[i].pos - planetArray[i2].pos

            # update the net force on the planet using Newton's Law of Gravitation
            planetArray[i].f -=(G * planetArray[i].m * planetArray[i2].m * r) / (mag(r) ** 3)

    # loop through all the planets in the array again
    for i in range(0, len(planetArray)):

        # use the velocity Verlet method to determine new position
        if method == "vv":

            # update the planet's position
            planetArray[i].pos += planetArray[i].v * dt + 0.5 * planetArray[i].a * (dt ** 2)

            # keep the accleration in memory
            lastA = vector(planetArray[i].a)

            # update the acceleration
            planetArray[i].a = planetArray[i].f / planetArray[i].m

            # update the velocity using the average acceleration
            planetArray[i].v += 0.5 * (lastA + planetArray[i].a) * dt

        # use the Euler-Cromer method to determine new position
        elif method == "e-c":

            # determine the acceleration
            a = planetArray[i].f / planetArray[i].m
            
            # update the position using the old velocity
            planetArray[i].pos += planetArray[i].v * dt
            
            # update the velocity
            planetArray[i].v += a * dt

        # update the curve and label for this planet
        curveArray[i].append(planetArray[i].pos)
        labelArray[i].pos = planetArray[i].pos

    # focus the view around a certain planet
    scene.center = planetArray[3].pos
   
    # increment the step counter
    step += 1

    # once a 'month' has passed, calculate the area for testing Kepler's second law
    if step % month == 0:

        # define and reset the total momentum of the system
        totalMomentum = 0

        # loop through all the planets in the array again
        for i in range(1, len(planetArray)):

            # calculate the dot product of the current position and last position
            dotProduct = dot(planetArray[i].pos - planetArray[starID].pos, planetArray[i].lastPos - planetArray[starID].pos)

            # multiply the magnitudes of the current position and last position
            moduli = mag(planetArray[i].pos - planetArray[starID].pos) * mag(planetArray[i].lastPos - planetArray[starID].pos)

            # calculate the angle between the two vectors
            theta = acos(dotProduct / moduli)

            # calculate the area enclosed by the two vectors, which should always be constant using Kepler's second law
##            area = dotProduct * theta / 2.0

##            print "Area for planet ", i, " is ", area, "m**2"

            # update the total momentum with this planet's momentum
            totalMomentum += planetArray[i].m * mag(planetArray[i].v)

        print totalMomentum

