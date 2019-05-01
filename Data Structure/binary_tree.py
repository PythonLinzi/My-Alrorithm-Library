class TreeNode(object):
    def __init__(self, data=None, left=None, right=None):
        self.val = data
        self.left = left
        self.right = right


class BinaryTree(object):
    def __init__(self, data_list):
        self.it = iter(data_list)
        self.root = TreeNode()
        self.create_tree(data_list)

    def inorder_create(self, bt=None):
        try:
            data = next(self.it)
            if data == '#': bt = None
            else:
                bt = TreeNode(data)
                bt.left = self.inorder_create(bt.left)
                bt.right = self.inorder_create(bt.right)
        except Exception as e:
            print(e)
        return bt

    def level_create(self, dl: list):
        if len(dl) == 0:
            self.root = None
            return
        l = len(dl)
        bt = TreeNode(dl[0])
        q = [bt]
        i = 1
        while i < l:
            q2 = []
            if len(q) == 0:
                break
            for j in range(len(q)):
                if dl[i]: q[j].left = TreeNode(dl[i])
                else: q[j].left = None

                if dl[i + 1]: q[j].right = TreeNode(dl[i + 1])
                else: q[j].right = None
                i += 2
                if q[j].left:
                    q2.append(q[j].left)
                if q[j].right:
                    q2.append(q[j].right)
            q = q2
        return bt


    def create_tree(self, data=None):
        # self.root = self.inorder_create()
        self.root = self.level_create(data)
        print('binary tree is succussfully created!')

    def preorder(self, bt: TreeNode):
        if bt:
            self.preorder(bt.left)
            print(bt.val, end=' ')
            self.preorder(bt.right)

    def inorder(self, bt: TreeNode):
        if bt:
            print(bt.val, end=' ')
            self.inorder(bt.left)
            self.inorder(bt.right)

    def postorder(self, bt: TreeNode):
        if bt:
            self.postorder(bt.left)
            self.postorder(bt.right)
            print(bt.val, end=' ')

    def leverl_order(self, bt: TreeNode):
        q = []
        q.append(bt)
        while len(q):
            tmp = q.pop(0)
            print(tmp.val, end=' ')
            if tmp.left:
                q.append(tmp.left)
            if tmp.right:
                q.append(tmp.right)

    def traverse(self):
        print('先序遍历:',end='')
        self.preorder(self.root)
        print('\n中序遍历:', end='')
        self.inorder(self.root)
        print('\n后序遍历:', end='')
        self.postorder(self.root)
        print('\n层序遍历:', end='')
        self.leverl_order(self.root)
        print()


if __name__ == '__main__':
    s = '123##4##56##78##9##'
    data_l = [1,2,3,4,None,None,5,None,None,None,None]
    print(data_l)
    bt = BinaryTree(data_l)
    bt.traverse()
