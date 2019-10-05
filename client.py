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
availableCircuits = possibleCircuits

def possibeCircuit(circuits, endpoints):
    for circuit in circuits:
        if(circuit in availableCircuits and (circuit[0] == endpoints[0] and circuit[-1] == endpoints[1]) or (circuit[0] == endpoints[1] and circuit[-1] == endpoints[0])):
            return circuit

def deleteFromConnections(connections, connection):
    for conn in connections:
        if connection == conn:
            connections.remove(connection)

action = 1
for i in range(duration):
    for elem in demands:
        connection = possibeCircuit(possibleCircuits, elem['end-points'])
        if elem['start-time'] == i and len(connection) > 0:
            connections.append(connection)
            deleteFromConnections(availableCircuits, connection)
            print(str(action) + ". igény foglalás: " + elem['end-points'][0] + "<->" + elem['end-points'][1] + " st:" + str(i) + " - sikeres")
            action += 1
        elif elem['start-time'] == i and not(possibeCircuit(possibleCircuits, elem['end-points'])):
            print(str(action) + ". igény foglalás: " + elem['end-points'][0] + "<->" + elem['end-points'][1] + " st:" + str(i) + " - sikertelen")
            action += 1

        if elem['end-time'] == i:
            deleteFromConnections(connections,connection)
            availableCircuits.append(connection)
            print(str(action) + ". igény felszabadítás: " + elem['end-points'][0] + "<->" + elem['end-points'][1] + " st:" + str(i))
            action += 1