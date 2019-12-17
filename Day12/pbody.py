import re
import numpy as np

class Moon:
    position = [0, 0, 0]
    velocity = [0, 0, 0]

    def __init__(self, position):
        self.position = position
        self.velocity = [0, 0, 0]

    def ApplyGravity(self, otherMoon):
        for i in range(3):
            ApplyGravityAxis(otherMoon, i)

    def ApplyGravityAxis(self, otherMoon, axis):
        if self.position[axis] < otherMoon.position[axis]:
            self.velocity[axis] += 1
        elif self.position[axis] > otherMoon.position[axis]:
            self.velocity[axis] -= 1

    def ApplyVelocity(self):
        for i in range(3):
            ApplyVelocityAxis(i)

    def ApplyVelocityAxis(self, axis):
        self.position[axis] += self.velocity[axis]

    def ComputeEnergy(self):
        potentialEnergy = 0
        kineticEnergy = 0

        for i in range(3):
            potentialEnergy += abs(self.position[i])
            kineticEnergy += abs(self.velocity[i])
        
        return potentialEnergy * kineticEnergy

nbSteps = [0, 0, 0]
inputFile = open("input", "r")
moons = []
for line in inputFile.readlines():
    match = re.match(r'^<x=(?P<x>.*), y=(?P<y>.*), z=(?P<z>.*)>$', line)
    moons.append(Moon([int(match.group('x')), int(match.group('y')), int(match.group('z'))]))

for axis in range(3):
    stepCatalog = set()
    notFound = True

    step = 0
    while notFound:
        # Apply gravity.
        for moon in moons:
            for otherMoon in moons:
                if otherMoon is moon:
                    continue
                moon.ApplyGravityAxis(otherMoon, axis)
        
        # Apply Velocity
        for moon in moons:
            moon.ApplyVelocityAxis(axis)

        currentStepStatus = []
        for moon in moons:
            currentStepStatus.append(moon.position[axis])
            currentStepStatus.append(moon.velocity[axis])            

        exp = 1
        key = 0
        for nb in currentStepStatus:
            nb *= exp
            key += nb
            exp *= 1000

        #key = frozenset(currentStepStatus)
        #key = currentStepStatus#int.from_bytes(byteNumber, byteorder='big', signed=False)
        if key in stepCatalog:
            print("THIS IS THE ONE", step)
            notFound = False
            nbSteps[axis] = step
            break

        stepCatalog.add(key)
        step += 1

totalEnergy = 0

for moon in moons:
    totalEnergy += moon.ComputeEnergy()

print("Total energy", totalEnergy)
print("STEPS : ", nbSteps)


print("Total number of steps before exact position :", np.lcm.reduce([np.int64(nbSteps[0]),np.int64(nbSteps[1]), np.int64(nbSteps[2])]))

