import json
import sys


with open(sys.argv[1], "r") as file:
    data = json.load(file)

endPoints = data['end-points']
switches = data['switches']
links = data['links']
possibleCircuits = data['possible-circuits']
simulation = data['simulation']
demands = simulation['demands']
duration = simulation['duration']

connections = []
usedLinks = []
availableCircuits = possibleCircuits
availableLinks = links


def validLink(point1, point2):
    return (point1[0] == point2[0] and point1[-1] == point2[1]) or (point1[0] == point2[1] and point1[-1] == point2[0])

def possibleCircuit(circuits, endpoints, demand): #ezzel megnézzük van-e egyáltalán olyan áramkör, aminek a két vége a nekünk kellő két pont
    needToTest, result = [], []
    for circuit in circuits:
        if circuit in availableCircuits and validLink(circuit, endpoints):
            needToTest.append(circuit)
    if needToTest:
        result = useableConnection(needToTest, demand)
    return result

def useableConnection(possConns, demand): #ezzel megnézzük hogy a lehetséges áramkörök közül tudjuk-e bármelyiket ténylegesen használni
    for conn in possConns:
        useableRoute = True
        maybeDelLinks = []
        for i in range(len(conn)-1):
            useableLink = False
            arr = [conn[i], conn[i+1]]
            for j in range(len(availableLinks)):
                actualLinks = availableLinks[j]
                if validLink(arr, actualLinks['points']) and demand == actualLinks['capacity']:
                    maybeDelLinks.append(arr)
                    useableLink |= True
                    useableRoute &= True
                    # deleteFromConnections(availableLinks, arr)
                    break
                if i == len(conn)-1 and not(validLink(arr, actualLinks['points']) and demand == actualLinks['capacity']):
                    useableRoute &= False
                # else:
                #     useable = False
                #     break
        if useableRoute:
            deleteFromLinks(availableLinks, maybeDelLinks)
            print(availableLinks)
            return conn
    return []


def deleteFromConnections(connections, connection):
    for conn in connections:
        if connection == conn:
            connections.remove(connection)

def deleteFromLinks(availableLinks, needToDelLinks):
    for needToDelLink in needToDelLinks:
        deleteFromConnections(availableLinks, needToDelLink)

def backToAvaliableLinks(availableLinks, connection):
    for i in range(len(connection) - 1):
        link = [connection[i], connection[i+1]]
        for j in range(len(links)):
            actualLinks = links[j]
            if validLink(link, actualLinks['points']):
                availableLinks.append(actualLinks)



action = 1
for i in range(duration):
    for elem in demands:
        connection = possibleCircuit(availableCircuits, elem['end-points'], elem['demand'])
        if elem['start-time'] == i and connection:
            connections.append(connection)
            deleteFromConnections(availableCircuits, connection)
            print(str(action) + ". igény foglalás: " + elem['end-points'][0] + "<->" + elem['end-points'][1] + " st:" + str(i) + " - sikeres")
            action += 1
        elif elem['start-time'] == i and not(connection):
            print(str(action) + ". igény foglalás: " + elem['end-points'][0] + "<->" + elem['end-points'][1] + " st:" + str(i) + " - sikertelen")
            action += 1

        if elem['end-time'] == i:
            deleteFromConnections(connections, connection)
            availableCircuits.append(connection)
            # vissza kell tenni a linkeket is az availableLinksbe
            backToAvaliableLinks(availableLinks,connection)
            print(str(action) + ". igény felszabadítás: " + elem['end-points'][0] + "<->" + elem['end-points'][1] + " st:" + str(i))
            action += 1