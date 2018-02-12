#!/usr/bin/env python

#Imports
import argparse
import copy

#Defining Node class
class Node:

    def __init__(self, name):
        self.name = name
        #linkMap will store the distance from this node to another in map form
        self.linkMap = {}
        #shortestPath will build as Dijkstra's Algorithm computes
        #source tree will be calculated by concatenating the shortest path
        #each iteration
        self.shortestPath = ""

    #This function maps the list of costs in the CSV to map form based on
    #which node they refer to
    def map_links(self, linkList):

        for i in range(0, len(nameList)):
            self.linkMap[ nameList[i] ] = linkList[i]

#Input
#read file
f = open("LinkStates.csv", "r")
#format top line to get list of node names
nameList = f.readline().replace("\r\n", "").split(",")
for item in nameList:
    if item == "":
        nameList.remove(item)

#format map of nodes and their links
nodeList = {}
for line in f:
    line = line.replace("\r\n", "").split(",")
    newNode = Node(line[0])
    newNode.map_links( line[1:] )
    nodeList[ line[0] ] = newNode

#let user designate source node
toFind = str(raw_input("Please type the node name and click Enter (case sensitive):\n"))
if toFind not in nameList:
    print ("Node is not in list")

#Algorithm execution
#initializing cost to connect to each node
costMap = {}
for name in nameList:
    costMap[name] = 1000
#cost from initial node to itself is zero
costMap[toFind] = 0
#initialize shortest path for first node
nodeList[toFind].shortestPath = nodeList[toFind].name

#make copies of node list that I can delete from
unvisitedNodeList = nodeList.keys()

#designate first node to work from
workingNode = nodeList[toFind]

#function to find the node with the smallest cost in the cost map that hasn't been visited yet
#determines starting node for next iteration in Dijkstra's Algorithm
def findMinNode(unvisitedList, costMap):
    minVal = 1001
    minNode = None
    for nodeName in unvisitedList:
        if costMap[nodeName] < minVal:
            minVal = costMap[nodeName]
            minNode = nodeName
    return minNode

#Dijkstra's Algorithm
while(unvisitedNodeList): #while list contains unvisited nodes
    workingNodeName = findMinNode(unvisitedNodeList, costMap) #get the lowest cost node in the list
    unvisitedNodeList.remove(workingNodeName) #and now remove it from the list of unvisited nodes

    for name in unvisitedNodeList: #look over the remaining unvisited nodes
        newLinkCost = int(nodeList[workingNodeName].linkMap[name]) + costMap[workingNodeName]
        if (newLinkCost < costMap[name] ): #if the cost from the current node is less than the cost in the cost map
            #update the cost map with new shorter cost
            costMap[name] = newLinkCost
            #update shortest path for the node
            nodeList[name].shortestPath = nodeList[workingNodeName].shortestPath + nodeList[name].name

#Formatting response
costLine = ""
sourceTreeList = []
for i in range(0, len(nameList)):
    #cost
    name = nameList[i]
    costLine += name + ":" + str(costMap[name])
    if (i != len(nameList) - 1):
        costLine = costLine + ", "

    #source tree
    sourceTreeList.append(nodeList[name].shortestPath)

#print sourceTreeList
#trimming the source tree
originalSourceTreeList = copy.deepcopy(sourceTreeList)
for path in originalSourceTreeList:
    for otherPath in sourceTreeList:
        if (path != otherPath) and (path in otherPath):
            sourceTreeList.remove(path)
            break

sourceTreeLine = ", ".join( sourceTreeList )

#Printing response
print "Source tree for node " + toFind + ":"
print sourceTreeLine
print "Cost for node " + toFind + ":"
print costLine
