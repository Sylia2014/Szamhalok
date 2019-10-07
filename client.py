import json
import sys


with open(sys.argv[1], "r") as file:
    data = json.load(file)

endPoints = data['end-points']
switches = data['switches']
possibleCircuits = data['possible-circuits']
simulation = data['simulation']
duration = simulation['duration']

links: list
links = data['links']

demands: list
demands = simulation['demands']

link: dict
for link in links:
    link.update({'used-capacity': 0})

demand: dict
for demand in demands:
    demand.update({'started': False})
    demand.update({'connection': None})

connections = []
usedLinks = []
availableCircuits = possibleCircuits


def validLink(point1, point2):
    return (point1[0] == point2[0] and point1[-1] == point2[1]) or (point1[0] == point2[1] and point1[-1] == point2[0])

def checkIsPossibleCircuit(circuits, endpoints, demand): #ezzel megnézzük van-e egyáltalán olyan áramkör, aminek a két vége a nekünk kellő két pont
    needToTest, result = [], []
    for circuit in circuits:
        if validLink(circuit, endpoints):
            isUseableCircuit(circuit, demand)

    return result

def isUseableCircuit(circuit, demand): #ezzel megnézzük hogy a lehetséges áramkörök közül tudjuk-e bármelyiket ténylegesen használni
    for i in range(len(circuit) - 1):
        for j in range(len(links)):
            actualLinks = links[j]
            if validLink(circuit[i:i+2], actualLinks['points']) and demand <= actualLinks['capacity'] - actualLinks['used-capacity']:
                break
            # if (i == len(circuit) - 1 and j == range(len(links))
            #         and not(validLink(circuit[i:i+2], actualLinks['points']) and demand <= actualLinks['capacity'] - actualLinks["used-capacity"])):
            #     return False


    # for conn in possConns:
    #     useableRoute = True
    #     maybeDelLinks = []
    #
    #     if useableRoute:
    #         deleteFromLinks(availableLinks, maybeDelLinks)
    #         print(availableLinks)
    #         return conn
    # return []


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
        # connection = possibleCircuit(availableCircuits, elem['end-points'], elem['demand'])
        if elem['start-time'] == i:
            checkIsPossibleCircuit(possibleCircuits, elem['end-points'], elem['demand'])
            # connections.append(connection)
            # deleteFromConnections(availableCircuits, connection)
            print(str(action) + ". igény foglalás: " + elem['end-points'][0] + "<->" + elem['end-points'][1] + " st:" + str(i) + " - sikeres")
            action += 1
        # elif elem['start-time'] == i and not(connection):
        #     print(str(action) + ". igény foglalás: " + elem['end-points'][0] + "<->" + elem['end-points'][1] + " st:" + str(i) + " - sikertelen")
        #     action += 1

        if elem['end-time'] == i and elem['started']:
            # felszabadít
            # deleteFromConnections(connections, connection)
            # availableCircuits.append(connection)
            # # vissza kell tenni a linkeket is az availableLinksbe
            # backToAvaliableLinks(availableLinks,connection)
            print(str(action) + ". igény felszabadítás: " + elem['end-points'][0] + "<->" + elem['end-points'][1] + " st:" + str(i))
            action += 1