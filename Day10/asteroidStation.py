def RetrieveWidthHeight(f):
    width, height = 0,0
    for line in f.readlines():
        height += 1
        width = len(line)
    return(width, height)


def AnnotateMap(f, width, height):
    annotatedMap = [[0 for x in range(width)] for y in range(height)]
    asteroids = []
    
    x, y = 0, 0
    for line in f.readlines():
        for char in list(line):
            if char == '#':
                annotatedMap[y][x] = 1
                asteroids.append((x, y))
            x += 1
        x = 0
        y += 1

    return (annotatedMap, asteroids)

def IsAsteroidBlocking(a, b, asteroid, otherAsteroid, possiblyBlockingAsteroid):
    minX, maxX, minY, maxY = min(asteroid[0], otherAsteroid[0]), max(asteroid[0], otherAsteroid[0]), min(asteroid[1], otherAsteroid[1]), max(asteroid[1], otherAsteroid[1])
    return abs(a * float(possiblyBlockingAsteroid[0]) - float(possiblyBlockingAsteroid[1]) + b) < 0.01 and minX <= possiblyBlockingAsteroid[0] and possiblyBlockingAsteroid[0] <= maxX and minY <= possiblyBlockingAsteroid[1] and possiblyBlockingAsteroid[1] <= maxY

# Vertical case
def IsVerticalAsteroidBlocking(asteroid, otherAsteroid, possiblyBlockingAsteroid):
    minY, maxY = min(asteroid[1], otherAsteroid[1]), max(asteroid[1], otherAsteroid[1])
    return possiblyBlockingAsteroid[0] == otherAsteroid[0] and minY <= possiblyBlockingAsteroid[1] and possiblyBlockingAsteroid[1] <= maxY

def ComputeAsteroidsVisible(annotatedMap, asteroid, asteroids):
    nbAsteroid = 0
    visibilityMap = annotatedMap

    for otherAsteroid in asteroids:
        # = (x, y)
        if otherAsteroid == asteroid:
            visibilityMap[otherAsteroid[1]][otherAsteroid[0]] = '#'
            continue

        # Vertical case...
        if otherAsteroid[0] == asteroid[0]:
            for possiblyBlockingAsteroid in asteroids:
                if possiblyBlockingAsteroid == asteroid or possiblyBlockingAsteroid == otherAsteroid:
                    continue
                if IsVerticalAsteroidBlocking(asteroid, otherAsteroid, possiblyBlockingAsteroid):
                    visibilityMap[otherAsteroid[1]][otherAsteroid[0]] = " "
                    break
            else:
                #Asteroid visible
                nbAsteroid += 1
        else:
            # Compute segment y = ax + b
            a = float(otherAsteroid[1] - asteroid[1]) / float(otherAsteroid[0] - asteroid[0])
            b = float(asteroid[1]) - a * float(asteroid[0])

            for possiblyBlockingAsteroid in asteroids:
                if possiblyBlockingAsteroid == asteroid or possiblyBlockingAsteroid == otherAsteroid:
                    continue
                if IsAsteroidBlocking(a, b, asteroid, otherAsteroid, possiblyBlockingAsteroid):
                    visibilityMap[otherAsteroid[1]][otherAsteroid[0]] = " "
                    break
            else:
                # Asteroid visible !
                nbAsteroid += 1
        

    #print("This is ", asteroid, "With visible : ", nbAsteroid)
    return(nbAsteroid, visibilityMap)



width, height = RetrieveWidthHeight(open("input", "r"))
annotatedMap, asteroids = AnnotateMap(open("input", "r"), width, height)

print(annotatedMap, asteroids, len(asteroids))

maxAsteroid = 0
bestAsteroid = (0,0)
for asteroid in asteroids:
    nbAsteroid, visibilityMap = ComputeAsteroidsVisible(annotatedMap, (asteroid), asteroids)
    if asteroid == (11, 13):
        print("THE ONE :", nbAsteroid)
    if nbAsteroid > maxAsteroid:
        maxAsteroid = nbAsteroid
        bestAsteroid = asteroid

#maxAsteroid, visibilityMap = ComputeAsteroidsVisible(annotatedMap, bestAsteroid, asteroids, width, height)

w = open("output", "w")
for y in range(height):
    for x in range(width):
        w.write(str(visibilityMap[y][x]))
    w.write('\n')

print("Best is :", bestAsteroid, "with asteroids visibles : ", maxAsteroid)