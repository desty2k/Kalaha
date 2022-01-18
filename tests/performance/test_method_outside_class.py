import timeit

setup = """
class Node:
    def __init__(self, board, player):
        super(Node, self).__init__()
        self.board = board
        self.player = player

    def copy(self):
        node = Node(self.board.copy(), self.player)
        return node
        
def copy(self):
    node = Node(self.board.copy(), self.player)
    return node

node = Node([5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 0], 0)
"""

# method inside class: 10.752
# method outside class: 10.383

if __name__ == '__main__':
    number = 20000000
    print('method inside class: %.3f' % timeit.timeit('node.copy()', setup=setup, number=number))
    print('method outside class: %.3f' % timeit.timeit('copy(node)', setup=setup, number=number))
