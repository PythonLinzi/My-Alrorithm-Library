import numpy as np


class Node(object):
    def __init__(self, data= None, lchild=None, rchild=None, parent=None):
        self.key = data
        self.left = lchild
        self.right = rchild
        self.parent = parent

    def hasLeftChild(self): return self.left

    def haxRightChild(self): return self.right

    def isLeftChild(self): return self.parent and self.parent.left==self

    def isRightChild(self): return self.parent and self.parent.right==self


class BSTree(object):
    def __init__(self):
        self.root = None
        self.size = 0

    def length(self): return self.size

    def insert(self, data):
        node = Node(data)
        if not self.root:
            self.root = node
            self.size += 1
        else:
            current_node = self.root
            while True:
                if data < current_node.key:
                    if current_node.left:
                        current_node = current_node.left
                    else:
                        current_node.left = node
                        node.parent = current_node
                        self.size += 1
                        break
                elif data > current_node.key:
                    if current_node.right:
                        current_node = current_node.right
                    else:
                        current_node.right = node
                        node.parent = current_node
                        self.size += 1
                        break
                else: break

    def create_bst_tree(self, array):
        for data in array:
            self.insert(data)

    def find(self, key):
        if self.root:
            ans = self._find(self.root, key)
            if ans: return ans
            else: return None
        else: return None

    def _find(self, node, key):
        if not node: return None
        elif node.key == key: return node
        elif key < node.key: return self._find(node.left, key)
        else: return self._find(node.right, key)

    def find_min(self):
        if self.root:
            current = self.root
            while current.left:
                current = current.left
            return current
        else: return None

    def find_max(self):
        if self.root:
            current = self.root
            while current.right:
                current = current.right
            return current
        else: return None

    def delete(self, key):
        if self.size > 1:
            removing_node = self.find(key)
            if removing_node:
                self.remove(removing_node)
                self.size -= 1
            else:
                print('Error, key not in tree')
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size = 0
        else:
            print('Error, key not in tree')

    def _find_min(self, node):
        if node:
            current = node
            while current.left:
                current = current.left
            return current

    def remove(self, node):
        if not node.left and not node.right:
            if node.parent.left == node: #  node is leave
                node.parent.left = None
            else:
                node.parent.right = None

        elif node.left and node.right: #  node has two sons
            replace_node = self._find_min(node.right)
            node.key = replace_node.key
            self.remove(replace_node)

        else: #  node has one son
            if node.hasLeftChild():
                if node.isLeftChild():
                    node.left.parent = node.parent
                    node.parent.left = node.left
                elif node.isRightChild():
                    node.left.parent = node.parent
                    node.parent.right = node.left
                else: #  node is root
                    self.root = node.left
                    node.left.parent = None
                    node.left = None
            else:
                if node.isLeftChild():
                    node.right.parent = node.parent
                    node.parent.left = node.right
                elif node.isRightChild():
                    node.right.parent = node.parent
                    node.parent.right = node.right
                else:  #  node is root
                    self.root = node.right
                    node.right.parent = None
                    node.right = None

    def preorder(self, node):
        if node:
            print(format(node.key, '2d'), end=" ")
            self.preorder(node.left)
            self.preorder(node.right)

    def preorder_traverse(self):
        self.preorder(self.root)
        print()

    def inorder(self, node):
        if node:
            self.inorder(node.left)
            print(format(node.key, '2d'), end=" ")
            self.inorder(node.right)

    def inorder_traverse(self):
        self.inorder(self.root)
        print()

    def postorder(self, node):
        if node:
            self.postorder(node.left)
            self.postorder(node.right)
            print(format(node.key, '2d'), end=" ")

    def postorder_traverse(self):
        self.postorder(self.root)
        print()

    def traverse(self):
        print('先序遍历:', end=" ")
        self.preorder_traverse()
        print('中序遍历:', end=" ")
        self.inorder_traverse()
        print('后序遍历:', end=" ")
        self.postorder_traverse()


if __name__ == '__main__':
    a = np.random.randint(1, 100, size=48).astype(np.int)
    print("array:", a)
    bst = BSTree()
    bst.create_bst_tree(a)
    bst.traverse()
