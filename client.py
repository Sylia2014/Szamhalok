# coding=utf-8
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
    demand.update({'served': False})


def validLink(point1, point2):
    return (point1[0] == point2[0] and point1[-1] == point2[1]) or (point1[0] == point2[1] and point1[-1] == point2[0])


def checkIsPossibleCircuit(circuits, endpoints, demand):
    needToTest, result = [], []
    for index, circuit in enumerate(circuits):
        if validLink(circuit, endpoints):
            if isUseableCircuit(circuit, demand):
                allocateResource(circuit, demand)
                # print(index)
                return index
            else:
                return None

    return result


def isUseableCircuit(circuit, demand):
    for i in range(len(circuit) - 1):
        length = len(circuit) - 2
        arr = circuit[i:i + 2]
        find = False

        actualLinks = findInLinks(circuit[i:i + 2], links)
        if demand <= actualLinks['capacity'] - actualLinks['used-capacity']:
            find = True
        if i == len(circuit) - 2 and find:
            return True
        elif i == len(circuit) - 1 and not (find):
            return False

        # régi mo eleje
        # for j in range(len(links)):
        #     arr = circuit[i:i+2]
        #     actualLinks = links[j]
        #     if validLink(arr, actualLinks['points']) and demand <= actualLinks['capacity'] - actualLinks['used-capacity']:
        #         find = True
        #         break
        # if i == len(circuit) - 2 and find:
        #     return True
        # elif i == len(circuit) - 1 and not(find):
        #     return False
        # régi mo vége


def findInLinks(linkPair, links):
    for link in links:
        if validLink(linkPair, link['points']):
            return link


def allocateResource(circuit, demand):
    for i in range(len(circuit) - 1):
        actualLinks = findInLinks(circuit[i:i + 2], links)
        actualLinks['used-capacity'] += demand

def releaseResource(index, demand):
    circuit = possibleCircuits[index]
    for i in range(len(circuit) - 1):
        actualLinks = findInLinks(circuit[i:i + 2], links)
        actualLinks['used-capacity'] -= demand


action = 1
for i in range(duration):
    for elem in demands:
        if elem['start-time'] == i and not(elem['started'] and not(elem['served'])):
            result = checkIsPossibleCircuit(possibleCircuits, elem['end-points'], elem['demand'])
            if result != None:
                elem['connection'] = result
                elem['started'] = True
                print(str(action) + ". igény foglalás: " + elem['end-points'][0] + "<->" +
                      elem['end-points'][1] + " st:" + str(i) + " - sikeres")
            else:
                print(str(action) + ". igény foglalás: " + elem['end-points'][0] + "<->" +
                      elem['end-points'][1] + " st:" + str(i) + " - sikertelen")
            action += 1

        if elem['end-time'] == i and elem['started']:
            releaseResource(elem['connection'], elem['demand'])
            elem['connection'] = None
            elem['started'] = False
            elem['served'] = True

            print(str(action) + ". igény felszabadítás: " + elem['end-points'][0] + "<->" +
                  elem['end-points'][1] + " st:" + str(i))
            action += 1
