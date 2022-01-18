#ifndef UNTITLED_CNODE_H
#define UNTITLED_CNODE_H

#include <vector>
#include <array>
#include <map>

class CNode {
private:
    std::map<int, CNode*> children;
    std::vector<int> board;
    std::array<std::vector<int>, 2> players_ranges;

    bool game_over = false;
    int player;

public:
    CNode(const CNode &node);
    CNode(std::vector<int> board, int player);
    ~CNode() {for (auto & it : children) delete it.second;}
    void make_move(int pit_index);
    bool is_game_over();
    int get_player();
    std::map<int, CNode*> get_children();
    std::vector<int> get_board();
    int get_utility(int player);

    void set_players_ranges(std::array<std::vector<int>, 2> players_ranges);
    std::array<std::vector<int>, 2> get_players_ranges();
    void add_child(int pit_index, CNode *cnode);
};


#endif //UNTITLED_CNODE_H
