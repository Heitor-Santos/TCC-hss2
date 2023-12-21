from typing import List

class Node:
    def __init__(self, occupied: bool, element: int):
        self.occupied = occupied
        self.rank = 0
        self.parent: Node = None
        self.element = element
        self.children :List[Node] = []
        self.children_with_children :List[Node] = []

def isLeaf(node: Node):
    return len(node.children) == 0

def isRoot(node: Node):
    return node.parent is None

def removeNodeFromParentChildren(node: Node):
    if not isRoot(node):
        node.parent.children.remove(node)
        if node in node.parent.children_with_children:
            node.parent.children_with_children.remove(node)
    

def find_aux(node: Node):
    if isRoot(node):
        return node
    else:
        return find_aux(node.parent)
    

def find(uf: List[Node], index: int):
    return find_aux(uf[index])

def makeset(uf: List[Node], index: int, element: int):
    newNode = Node(True, element)
    uf[index] = newNode

def union(uf: List[Node], indexA: int, indexB: int):
    rootA = find(uf, indexA)
    rootB = find(uf, indexB)
    if rootA.rank >= rootB.rank:
        removeNodeFromParentChildren(rootB)
        rootB.parent = rootA
        rootA.children.append(rootB)
        if not isLeaf(rootB):
            rootA.children_with_children.append(rootB)
        if rootA.rank == rootB.rank:
            rootA.rank += 1
    else:
        removeNodeFromParentChildren(rootA)
        rootB.children.append(rootA)
        if not isLeaf(rootA):
            rootA.children_with_children.append(rootA)
        rootA.parent = rootB

def delete(uf: List[Node], index: int):
    node = uf[index]
    node.occupied = False
    if not isLeaf(node):
        if not isRoot(node) and len(node.children) == 1:
            only_child = node.children[0]
            only_child.parent = node.parent
            removeNodeFromParentChildren(node)
            node.parent.children.append(only_child)
            if len(only_child.children) > 0:
                node.parent.children_with_children.append(only_child) 
            uf[index] = None
    else:
        removeNodeFromParentChildren(node)
        parent = node.parent
        uf[index] = None
        if not isRoot(node) and isLeaf(parent):
            parent.rank = 0
        if not isRoot(node) and not parent.occupied and len(parent.children) == 1:
            only_child = parent.children[0]
            only_child.parent = parent.parent
            removeNodeFromParentChildren(parent)
            if not isRoot(parent):
                parent.parent.children.append(only_child)
                if len(only_child.children) > 0:
                    parent.parent.children_with_children.append(only_child) 