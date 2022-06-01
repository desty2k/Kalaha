
class Node:
    def __init__(self, board: list[int], player):
        super(Node, self).__init__()
        self.board = board
        self.player = player
        self.game_over = False
        self.children: dict[int, Node] = {}
        self.player_ranges = (range(0, len(board) // 2 - 1), range(len(board) // 2, len(board) - 1))
    __slots__ = ("board", "player", "player_ranges", "game_over", "children")

    # methods are outside of the class to reduce memory usage
    def copy(self) -> 'Node':
        node = Node(self.board.copy(), self.player)
        node.game_over = self.game_over
        node.player_ranges = self.player_ranges
        return node

    def make_move(self, pit_index):
        # pick stones from selected pit and place them in the next player's pits
        stones = self.board[pit_index]
        self.board[pit_index] = 0
        for i in range(stones):
            pit_index = (pit_index + 1) % len(self.board)
            self.board[pit_index] += 1

        # last stone in player's base, do not change player
        if pit_index != (len(self.board) // (2 - self.player)) - 1:
            # stealing stones
            if self.board[pit_index] == 1:
                opposite_hole_index = len(self.board) - 2 - pit_index
                if pit_index in self.player_ranges[self.player]:
                    self.board[(len(self.board) // (2 - self.player)) - 1] += self.board[opposite_hole_index]
                    self.board[opposite_hole_index] = 0
            self.player = (self.player + 1) % 2

        # check if game is over
        if any(sum([self.board[index] for index in self.player_ranges[player]]) == 0 for player in (0, 1)):
            for player in (0, 1):
                self.board[(len(self.board) // (2 - player)) - 1] += sum(
                    [self.board[i] for i in self.player_ranges[player]])
                for i in self.player_ranges[player]:
                    self.board[i] = 0
            self.game_over = True
