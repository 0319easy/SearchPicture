from anytree import Node, RenderTree
from HierarchyTree.FilePath import filePathGetter

class HierarchyTree:
    def __init__(self):
        self.file_name = filePathGetter.getFilePath()
        self.node_set = []
        self.content = []

    def makeContent(self):
        f = open(self.file_name, 'r', encoding='UTF8')
        while True:
            line = f.readline()
            if not line : break
            self.content.append((line.count("\t") ,line.replace("\n","").replace("\t","", len(line))))
        f.close()

    def makeTree(self):
        self.makeContent()
        self.node_set.append(Node(f'node_{0}', data = self.content[0][1]))
        self.makeTree_sub(0)

    def makeTree_sub(self, nodeNum):
        while True:
            if (len(self.content) == len(self.node_set)) or (self.content[nodeNum][0] > self.content[len(self.node_set)][0] - 1):
                return
            elif self.content[nodeNum][0] == self.content[len(self.node_set)][0]- 1:
                self.node_set.append(Node(f'node_{len(self.node_set)}', parent = self.node_set[nodeNum], data = self.content[len(self.node_set)][1]))
            elif self.content[nodeNum][0] < self.content[len(self.node_set)][0] - 1:
                self.makeTree_sub(len(self.node_set) - 1)

    def searchKeyword(self, keyword):
        for row in RenderTree(self.node_set[0]):
            pre, fill, node = row
            if keyword in node.data:
                return self.getRelatedNodes(node)

    def getRelatedNodes(self, node):
        result = []
        result.append(self.getParents(node))
        result.append(self.getChildren(node))
        return result

    def getChildren(self, node):
        children = []
        for row in RenderTree(node):
            pre, fill, node = row
            children.append(node.data)
        return children

    def getParents(self, node):
        parents = []
        while True:
            if node.parent:
                parents.append(node.parent.data)
                node = node.parent
            else:
                break
        return parents

    def showTree(self):
        print("==" * 20)
        for row in RenderTree(self.node_set[0]):
            pre, fill, node = row
            print(f"{pre}{node.name}, data: {node.data}")
        print("==" * 20)

if __name__ == "__main__":
    ht = HierarchyTree()
    ht.makeTree()
    print(f'keyword : 패션의류 result : {ht.searchKeyword("패션의류")}')
    print(f'keyword : 러닝 result : {ht.searchKeyword("러닝")}')
    print(f'keyword : 신발 result : {ht.searchKeyword("신발")}')

