#include <Python.h>
#include <vector>
#include <array>

#include "CNode.h"


struct Move {
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


static Move calculate_minimax(CNode *node, int maximizing_player, int alpha_beta, int alpha, int beta, int depth) {
    if (depth == 0 || node->is_game_over()) {
        Move move{};
        move.index = -1;
        move.util = node->get_utility(maximizing_player);
        return move;
    }

    // make copy of node
//    auto* node_copy = new CNode(*node);

    // get players ranges
    auto players_ranges = node->get_players_ranges();

    for (int pit_index : players_ranges[node->get_player()]) {
        // for each pit, if it is not empty and child is not yet created, create it and make move
        if (node->get_board()[pit_index] != 0 && node->get_children().count(pit_index) == 0) {
            auto* child = new CNode(*node);
            child->make_move(pit_index);
            node->add_child(pit_index, child);
        }
    }
//    delete node_copy;

    int best_index = -1;
    if (node->get_player() == maximizing_player) {
        int best_util = INT_MIN;
        for (auto& child : node->get_children()) {
            Move move = calculate_minimax(child.second, maximizing_player, alpha_beta, alpha, beta, depth - 1);
            if (move.util >= best_util) {
                best_util = move.util;
                best_index = child.first;
            }
            alpha = std::max(alpha, move.util);
            if (beta <= alpha && alpha_beta == 1) {
                break;
            }
        }
        return {best_util, best_index};
    }
    else {
        int best_util = INT_MAX;
        for (auto& child : node->get_children()) {
            Move move = calculate_minimax(child.second, maximizing_player, alpha_beta, alpha, beta, depth - 1);
            if (move.util <= best_util) {
                best_util = move.util;
                best_index = child.first;
            }
            beta = std::min(beta, move.util);
            if (beta <= alpha && alpha_beta == 1) {
                break;
            }
        }
        return {best_util, best_index};
    }
}


static Move calculate_iterative_deepening(CNode *node, int maximizing_player, int alpha_beta, int minimax_depth) {
    // vector of moves
    minimax_depth += 1;
    Move best_move{};
    best_move.index = -1;
    best_move.util = INT_MIN;
    for (int i = 0; i < minimax_depth; i++) {
        Move move = calculate_minimax(node, maximizing_player, alpha_beta, INT_MIN, INT_MAX, i);
        if (move.index != -1 && move.util > best_move.util) {
            best_move = move;
        }
    }
    return best_move;
}


static Move run(std::vector<int> board, int maximizing_player, int minimax_depth, int alpha_beta, int iterative_deepening) {
    if (board.empty()) {
        return {0, -1};
    }
    auto* root = new CNode(board, maximizing_player);
    root->set_players_ranges(get_available_indexes(board));
    if (minimax_depth > 0) {
        if (iterative_deepening == 1) {
            // run iterative deepening
            return calculate_iterative_deepening(root, maximizing_player, alpha_beta, minimax_depth);
        }
        else {
            // calculate minimax
            return calculate_minimax(root, maximizing_player, alpha_beta, INT_MIN, INT_MAX, minimax_depth);
        }
    }
    else {
        // random index from allowed indexes
        return {0, root->get_players_ranges()[maximizing_player][rand() % root->get_players_ranges()[maximizing_player].size()]};
    }
}


static PyObject* run(PyObject *self, PyObject *args) {
    int minimax_depth;
    int alpha_beta;
    int iterative_deepening;

    PyObject * python_board;
    std::vector<int> board;
    int player;

    if (!PyArg_ParseTuple(args, "Oiipp", &python_board, &player, &minimax_depth,
                          &alpha_beta, &iterative_deepening)) {
        return nullptr;
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
    Move move = run(board, player, minimax_depth, alpha_beta, iterative_deepening);
    return PyLong_FromLong(move.index);
}


static PyObject * get_verbose_flag(PyObject *self, PyObject *args) {
    return PyLong_FromLong(Py_VerboseFlag);
}


static PyMethodDef module_methods[] = {
    {
        "run", run, METH_VARARGS,
        "Calculate best move for a given board and player"
    },
    {
        "get_verbose_flag", get_verbose_flag, METH_NOARGS,
        "Return the Py_Verbose flag"
    },
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef module_definition = {
    PyModuleDef_HEAD_INIT,
    "CMinimax",
    "A minimax implementation in C++",
    0,
    module_methods,
};


PyMODINIT_FUNC PyInit_CMinimax() {
    return PyModule_Create(&module_definition);
}
