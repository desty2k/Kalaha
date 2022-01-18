#include <Python.h>
#include <vector>
#include <array>

#include "CNode.h"


struct BestMove {
    int util;
    int index;
};


static std::array<std::vector<int>, 2> get_available_indexes(std::vector<int> board) {
    std::array<std::vector<int>, 2> available_indexes{};
    for (int i = 0; i < (board.size() / 2) - 1; i++) {
        available_indexes[0].push_back(i);
    }
    for (int i = board.size() / 2; i < board.size() - 1; i++) {
        available_indexes[1].push_back(i);
    }
    return available_indexes;
}


static BestMove calculate_minimax(CNode *node, int maximizing_player, int alpha_beta, int alpha, int beta, int depth) {
    if (depth == 0 || node->is_game_over()) {
        BestMove move{};
        move.index = -1;
        move.util = node->get_utility(maximizing_player);
        return move;
    }

    // make copy of node
    auto* node_copy = new CNode(*node);

    // get players ranges
    auto players_ranges = node_copy->get_players_ranges();

    for (int pit_index : players_ranges[maximizing_player]) {
        // for each pit, if it is not empty and child is not yet created, create it and make move
        if (node->get_board()[pit_index] != 0 && node->get_children().count(pit_index) == 0) {
            CNode* child = new CNode(*node_copy);
            child->make_move(pit_index);
            // print board
            node->add_child(pit_index, child);
        }
    }
    delete node_copy;

    int best_index = -1;
    if (node->get_player() == maximizing_player) {
        int best_util = INT_MIN;
        for (auto& child : node->get_children()) {
            BestMove move = calculate_minimax(child.second, maximizing_player, alpha_beta, alpha, beta, depth - 1);
            if (move.util >= best_util) {
                best_util = move.util;
                best_index = child.first;
            }
            alpha = std::max(alpha, best_util);
            if (beta <= alpha && alpha_beta == 1) {
                break;
            }
        }
        return {best_util, best_index};
    }
    else {
        int best_util = INT_MAX;
        for (auto& child : node->get_children()) {
            BestMove move = calculate_minimax(child.second, maximizing_player, alpha_beta, alpha, beta, depth - 1);
            if (move.util <= best_util) {
                best_util = move.util;
                best_index = child.first;
            }
            beta = std::min(beta, best_util);
            if (beta <= alpha && alpha_beta == 1) {
                break;
            }
        }
        return {best_util, best_index};
    }
}


static BestMove calculate_iterative_deepening(CNode *node, int maximizing_player, int alpha_beta, int minimax_depth) {
    // vector of moves
    minimax_depth += 1;
    BestMove best_move{};
    best_move.index = -1;
    best_move.util = INT_MIN;
    for (int i = 0; i < minimax_depth; i++) {
        BestMove move = calculate_minimax(node, maximizing_player, alpha_beta, INT_MIN, INT_MAX, i);
        if (move.index != -1 && move.util > best_move.util) {
            best_move = move;
        }
    }
    return best_move;
}


static int calculate_move(std::vector<int> board, int maximizing_player, int minimax_depth, int alpha_beta, int iterative_deepening) {
    if (board.empty()) {
        return -1;
    }

    auto* root = new CNode(board, maximizing_player);
    root->set_players_ranges(get_available_indexes(board));
    if (minimax_depth > 0) {
        if (iterative_deepening == 1) {
            // run iterative deepening
            BestMove best = calculate_iterative_deepening(root, maximizing_player, alpha_beta, minimax_depth);
            return best.index;
        }
        else {
            // calculate minimax
            BestMove best = calculate_minimax(root, maximizing_player, alpha_beta, INT_MIN, INT_MAX, minimax_depth);
            return best.index;
        }
    }
    else {
        // random index from allowed indexes
        return root->get_players_ranges()[maximizing_player][rand() % root->get_players_ranges()[maximizing_player].size()];
    }
}


static PyObject* calculate_move(PyObject *self, PyObject *args) {
    int minimax_depth;
    int alpha_beta;
    int iterative_deepening;

    PyObject * python_board;
    std::vector<int> board;
    int player;

    if (!PyArg_ParseTuple(args, "Oiipp", &python_board, &player, &minimax_depth,
                          &alpha_beta, &iterative_deepening)) {
        return NULL;
    }

    // convert python list to std::vector
    int num_pits = PyList_Size(python_board);
    if (num_pits < 0) return NULL;
    for (int i = 0; i < num_pits; i++) {
        PyObject * pit = PyList_GetItem(python_board, i);
        if (pit == NULL) return NULL;
        int pit_value = PyLong_AsLong(pit);
        if (pit_value == -1 && PyErr_Occurred()) return NULL;
        board.push_back(pit_value);
    }

    // create player
    return PyLong_FromLong(calculate_move(board, player, minimax_depth, alpha_beta, iterative_deepening));
}


static PyObject * get_verbose_flag(PyObject *self, PyObject *args) {
    return PyLong_FromLong(Py_VerboseFlag);
}


static PyMethodDef module_methods[] = {
    {
        "calculate_move", calculate_move, METH_VARARGS,
        "calculate best move for a given board and player"
    },
    {
        "get_verbose_flag", get_verbose_flag, METH_NOARGS,
        "Return the Py_Verbose flag"
    },
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef module_definition = {
    PyModuleDef_HEAD_INIT,
    "CAutoPlayer",
    "A Python extension module for Kalaha game AutoPlayer",
    0,
    module_methods,
};


PyMODINIT_FUNC PyInit_CAutoPlayer() {
    return PyModule_Create(&module_definition);
}
