import numpy as np


class Node(object):
    def __init__(self, data=None, lchild=None, rchild=None):
        self.key = data
        self.lchild = lchild
        self.rchild = rchild


class BiTree(object):
    def __init__(self, data_list):
        self.it = iter(data_list)

    def createBiTree(self, bt=None):
        try:
            next_data = next(self.it)
            if next_data is '#':
                bt = None
            else:
                bt = Node(next_data)
                bt.lchild = self.createBiTree(bt.lchild)
                bt.rchild = self.createBiTree(bt.rchild)
        except Exception as e:
            print(e)
        return bt

    def preorder_traverse(self, bt):
        if bt is not None:
            print(bt.key, end=" ")
            self.preorder_traverse(bt.lchild)
            self.preorder_traverse(bt.rchild)

    # 中序遍历函数
    def inorder_traverse(self, bt):
        if bt is not None:
            self.inorder_traverse(bt.lchild)
            print(bt.key, end=" ")
            self.inorder_traverse(bt.rchild)

    # 后序遍历函数
    def postorder_traverse(self, bt):
        if bt is not None:
            self.postorder_traverse(bt.lchild)
            self.postorder_traverse(bt.rchild)
            print(bt.key, end=" ")

    # 综合打印
    def print_traverse(self, bt):
        print("先序遍历: ", end="")
        self.preorder_traverse(bt)
        print()
        print("中序遍历: ", end="")
        self.inorder_traverse(bt)
        print()
        print("后序遍历: ", end="")
        self.postorder_traverse(bt)
        print()


if __name__ == '__main__':
    a = np.random.randint(1, 100, size=12).astype(np.int)
    bt = BiTree(a)
    root = bt.createBiTree()
    bt.print_traverse(root)
