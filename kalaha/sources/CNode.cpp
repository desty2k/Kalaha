#include "CNode.h"
#include "algorithm"
#include "numeric"

CNode::CNode(const CNode &node) {
    this->board = node.board;
    this->player = node.player;
    this->game_over = node.game_over;
    this->players_ranges = node.players_ranges;
}

CNode::CNode(std::vector<int> board, int player) {
    this->board = board;
    this->player = player;
}

bool CNode::is_game_over() {
    return game_over;
}

void CNode::make_move(int pit_index) {
    int stones = board[pit_index];
    board[pit_index] = 0;
    for (int i = 0; i < stones; i++) {
        pit_index = (pit_index + 1) % board.size();
        board[pit_index]++;
    }
    // last stone in player's base, do not change player
    if (pit_index != (board.size() / (2 - player) - 1)) {
        if (board[pit_index] == 1) {
            int opposite_hole_index = board.size() - 2 - pit_index;
            if (std::find(players_ranges[player].begin(), players_ranges[player].end(), pit_index) != players_ranges[player].end()) {
                board[(board.size()) / (2 - player) - 1] += board[opposite_hole_index];
                board[opposite_hole_index] = 0;
            }
        }
        player = (player + 1) % 2;
    }

     int sum_player_one = 0;
     int sum_player_two = 0;
     for (int i = 0; i < board.size(); i++) {
         if (std::find(players_ranges[0].begin(), players_ranges[0].end(), i) != players_ranges[0].end()) {
             sum_player_one += board[i];
         }
         if (std::find(players_ranges[1].begin(), players_ranges[1].end(), i) != players_ranges[1].end()) {
             sum_player_two += board[i];
         }
     }
     if (sum_player_one == 0 || sum_player_two == 0) {
         board[(board.size() / 2) - 1] += sum_player_one;
         board[(board.size() - 1)] += sum_player_two;
         for (int i = 0; i < players_ranges[0].size(); i++) {
             board[players_ranges[0][i]] = 0;
         }
         for (int i = 0; i < players_ranges[1].size(); i++) {
             board[players_ranges[1][i]] = 0;
         }
         game_over = true;
     }
}

std::vector<int> CNode::get_board() {
    return board;
}

int CNode::get_player() {
    return player;
}

int CNode::get_utility(int maximizing_player) {
    return board[(board.size() / (2 - maximizing_player)) - 1] - board[board.size() / (2 - ((maximizing_player + 1) % 2)) - 1];
}

std::map<int, CNode *> CNode::get_children() {
    return children;
}

void CNode::add_child(int pit_index, CNode *cnode) {
    children[pit_index] = cnode;
}

void CNode::set_players_ranges(std::array<std::vector<int>, 2> new_ranges) {
    players_ranges = std::move(new_ranges);
}

std::array<std::vector<int>, 2> CNode::get_players_ranges() {
    return players_ranges;
}





