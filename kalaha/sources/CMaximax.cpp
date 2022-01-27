#include <Python.h>
#include <vector>
#include <array>

#include "CNode.h"


struct Move {
    int util;
    int index;
};


static std::array<std::vector<int>, 2> get_available_indexes(const std::vector<int>& board) {
    std::array<std::vector<int>, 2> available_indexes{};
    for (int i = 0; i < (board.size() / 2) - 1; i++) {
        available_indexes[0].push_back(i);
    }
    for (int i = board.size() / 2; i < board.size() - 1; i++) {
        available_indexes[1].push_back(i);
    }
    return available_indexes;
}


static Move calculate_maximax(CNode *node, int maximizing_player, int depth) {
    if (depth == 0 || node->is_game_over()) {
        return {node->get_utility(maximizing_player), -1};
    }

    int best_index = -1;
    int best_util = INT_MIN;
    // get players ranges
    auto players_ranges = node->get_players_ranges();
    for (int pit_index : players_ranges[node->get_player()]) {
        // for each pit, if it is not empty and child is not yet created, create it and make move
        if (node->get_board()[pit_index] != 0 && node->get_children().count(pit_index) == 0) {
            auto* child = new CNode(*node);
            child->make_move(pit_index);
            // add child to node, so it won't be created again
            node->add_child(pit_index, child);
            // get best move for child
            Move move = calculate_maximax(child, maximizing_player, depth - 1);
            if (move.util >= best_util) {
                best_util = move.util;
                best_index = pit_index;
            }
        }
    }
    return {best_util, best_index};
}


static Move calculate_iterative_deepening(CNode *node, int maximizing_player, int maximax_depth) {
    // vector of moves
    maximax_depth += 1;
    Move best_move{};
    best_move.index = -1;
    best_move.util = INT_MIN;
    for (int i = 0; i < maximax_depth; i++) {
        Move move = calculate_maximax(node, maximizing_player, i);
        if (move.index != -1 && move.util > best_move.util) {
            best_move = move;
        }
    }
    return best_move;
}


static Move run(const std::vector<int>& board, int maximizing_player, int maximax_depth, int iterative_deepening) {
    if (board.empty()) {
        return {0, -1};
    }
    auto* root = new CNode(board, maximizing_player);
    root->set_players_ranges(get_available_indexes(board));
    if (maximax_depth > 0) {
        if (iterative_deepening == 1) {
            // run iterative deepening
            return calculate_iterative_deepening(root, maximizing_player, maximax_depth);
        }
        else {
            // calculate maximax
            return calculate_maximax(root, maximizing_player, maximax_depth);
        }
    }
    else {
        // random index from allowed indexes
        return {0, root->get_players_ranges()[maximizing_player][rand() % root->get_players_ranges()[maximizing_player].size()]};
    }
}


static PyObject* run(PyObject *self, PyObject *args) {
    int maximax_depth;
    int iterative_deepening;

    PyObject * python_board;
    std::vector<int> board;
    int player;

    if (!PyArg_ParseTuple(args, "Oiip", &python_board, &player, &maximax_depth,
                          &iterative_deepening)) {
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
    Move move = run(board, player, maximax_depth, iterative_deepening);
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
    "CMaximax",
    "A maximax implementation in C++",
    0,
    module_methods,
};


PyMODINIT_FUNC PyInit_CMaximax() {
    return PyModule_Create(&module_definition);
}
