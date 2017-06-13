import pygame
from vectors import Vector2D
from constants import *
from stacks import Stack
from numpy import loadtxt

class Node(object):
    def __init__(self, row, column):
        self.row, self.column = row, column
        self.position = Vector2D(column*WIDTH, row*HEIGHT)
        self.neighbors = {UP:None, DOWN:None, LEFT:None, RIGHT:None}
        self.portalNode = None
        
    def render(self, screen):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                pygame.draw.line(screen, WHITE, self.position.toTuple(),
                                 self.neighbors[n].position.toTuple(), 4)
                pygame.draw.circle(screen, RED, self.position.toTuple(), 12)


class NodeGroup(object):
    def __init__(self, level):
        self.level = level
        self.nodeList = []
        self.grid = None
        self.nodeStack = Stack()
        self.createNodeList(MAZEDATA[level]["file"], self.nodeList)
        
    def createNodeList(self, textFile, nodeList):
        self.grid = loadtxt(textFile, dtype=str)
        startNode = self.findFirstNode(*self.grid.shape)
        self.nodeStack.push(startNode)
        while not self.nodeStack.isEmpty():
            node = self.nodeStack.pop()
            self.addNode(node, nodeList)
            leftNode = self.getPathNode(LEFT, node.row, node.column-1, nodeList)
            rightNode = self.getPathNode(RIGHT, node.row, node.column+1, nodeList)
            upNode = self.getPathNode(UP, node.row-1, node.column, nodeList)
            downNode = self.getPathNode(DOWN, node.row+1, node.column, nodeList)
            node.neighbors[LEFT] = leftNode
            node.neighbors[RIGHT] = rightNode
            node.neighbors[UP] = upNode
            node.neighbors[DOWN] = downNode
            self.addNodeToStack(leftNode, nodeList)
            self.addNodeToStack(rightNode, nodeList)
            self.addNodeToStack(upNode, nodeList)
            self.addNodeToStack(downNode, nodeList)
        self.setupPortalNodes()
        
    def getNode(self, x, y, nodeList=[]):
        for node in nodeList:
            if node.position.x == x and node.position.y == y:
                return node
        return None

    def getNodeFromNode(self, node, nodeList):
        if node is not None:
            for inode in nodeList:
                if node.row == inode.row and node.column == inode.column:
                    return inode
        return node

    def getPathNode(self, direction, row, col, nodeList):
        tempNode = self.followPath(direction, row, col)
        return self.getNodeFromNode(tempNode, nodeList)

    def findFirstNode(self, rows, cols):
        nodeFound = False
        for row in range(rows):
            for col in range(cols):
                if self.grid[row][col] == "+":
                    return Node(row, col)
        return None

    def addNode(self, node, nodeList):
        nodeInList = self.nodeInList(node, nodeList)
        if not nodeInList:
            nodeList.append(node)

    def addNodeToStack(self, node, nodeList):
        if node is not None and not self.nodeInList(node, nodeList):
            self.nodeStack.push(node)

    def nodeInList(self, node, nodeList):
        for inode in nodeList:
            if (node.position.x == inode.position.x and
                node.position.y == inode.position.y):
                return True
        return False

    def followPath(self, direction, row, col):
        if direction == LEFT and col >= 0:
            return self.pathToFollow(LEFT, row, col, "-")
        elif direction == RIGHT and col < self.grid.shape[1]:
            return self.pathToFollow(RIGHT, row, col, "-")
        elif direction == UP and row >= 0:
            return self.pathToFollow(UP, row, col, "|")
        elif direction == DOWN and row < self.grid.shape[0]:
            return self.pathToFollow(DOWN, row, col, "|")
        else:
            return None

    def pathToFollow(self, direction, row, col, path):
        if self.grid[row][col] == path or self.grid[row][col] == "+":
            while self.grid[row][col] != "+":
                if direction is LEFT: col -= 1
                elif direction is RIGHT: col += 1
                elif direction is UP: row -= 1
                elif direction is DOWN: row += 1
            return Node(row, col)
        else:
            return None

    def setupPortalNodes(self):
        for pos1 in MAZEDATA[self.level]["portal"].keys():
            node1 = self.getNode(*pos1, nodeList=self.nodeList)
            node2 = self.getNode(*MAZEDATA[self.level]["portal"][pos1],
                                 nodeList=self.nodeList)
            node1.portalNode = node2
            node2.portalNode = node1
            
    def render(self, screen):
        for node in self.nodeList:
            node.render(screen)