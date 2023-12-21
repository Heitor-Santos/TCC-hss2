from typing import List

class Node:
    def __init__(self, occupied: bool, element: int):
        self.occupied = occupied
        self.rank = 0
        self.parent: Node = None
        self.element = element
        self.prev_sibling:Node = None
        self.next_sibling:Node = None
        self.prev_sibling_with_children:Node = None
        self.next_sibling_with_children:Node = None
        self.children_count = 0
        self.children_with_children_count = 0
        self.children_tail:Node = None
        self.children_with_children_tail:Node = None

def isLeaf(node: Node):
    return node.children_count == 0

def isRoot(node: Node):
    return node.parent is None

def hasPrevChildren(node: Node):
    return not node.prev_sibling is None

def hasPrevChildrenWithChildren(node: Node):
    return not node.prev_sibling_with_children is None

def isTailOfTheChildrenList(node: Node):
    return node.next_sibling is None

def isTailOfTheChildrenWithChildrenList(node: Node):
    return node.next_sibling_with_children is None

def removeNodeFromParentChildren(node: Node):
    if not isRoot(node):
        if hasPrevChildren(node):
            node.prev_sibling.next_sibling = node.next_sibling
        if isTailOfTheChildrenList(node):
            node.parent.children_tail = node.prev_sibling
        node.parent.children_count -= 1

        if hasPrevChildrenWithChildren(node):
            node.prev_sibling_with_children.next_sibling_with_children = node.next_sibling_with_children
        if isTailOfTheChildrenWithChildrenList(node):
            node.parent.children_with_children_tail = node.prev_sibling_with_children
        node.parent.children_with_children_count -=1
    
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

def addToParentChildren(parent: Node, child: Node):
    if parent.children_tail is not None:
        parent.children_tail.next_sibling = child
        child.prev_sibling = parent.children_tail 
    parent.children_tail = child
    parent.children_count += 1

def addToParentChildrenWithChildren(parent: Node, child:Node):
    if parent.children_with_children_tail is not None:
        parent.children_with_children_tail.next_sibling_with_children = child
        child.prev_sibling_with_children = parent.children_with_children_tail
    parent.children_with_children_tail = child
    parent.children_with_children_count +=1
    
def union_aux(parent: Node, child: Node):
    removeNodeFromParentChildren(child)
    child.parent = parent
    addToParentChildren(parent, child)
    if not isLeaf(child):
        addToParentChildrenWithChildren(parent, child)

def union(uf: List[Node], indexA: int, indexB: int):
    rootA = find(uf, indexA)
    rootB = find(uf, indexB)
    if rootA.rank >= rootB.rank:
        union_aux(rootA, rootB)    
        if rootA.rank == rootB.rank:
            rootA.rank += 1
    else:
        union_aux(rootB, rootA)

def delete(uf: List[Node], index: int):
    node = uf[index]
    node.occupied = False
    if not isLeaf(node):
        if not isRoot(node) and node.children_count == 1:
            only_child = node.children_tail
            grandpa = node.parent
            only_child.parent = grandpa
            removeNodeFromParentChildren(node)
            addToParentChildren(grandpa, only_child)
            if only_child.children_count > 0:
                addToParentChildrenWithChildren(grandpa, only_child) 
            uf[index] = None
    else:
        removeNodeFromParentChildren(node)
        parent = node.parent
        uf[index] = None
        if not isRoot(node) and isLeaf(parent):
            parent.rank = 0
        if not isRoot(node) and not parent.occupied and parent.children_count == 1:
            only_child = parent.children_tail
            grandpa = parent.parent
            only_child.parent = grandpa
            removeNodeFromParentChildren(parent)
            if not isRoot(parent):
                addToParentChildren(grandpa, only_child)
                if only_child.children_count > 0:
                    addToParentChildrenWithChildren(grandpa, only_child) 