'''
This class is used to represent a node in the Monte Carlo Tree Search
'''

import numpy as np

from src.environment.board import Board

class Node:

    def __init__(self, board, parent=None):

        self.board = board

        self.estimated_value = self.board.reward
        self.estimated_policy = None

        self.visit_count = 0
        self.total_outcome = 0.0
        self.average_outcome = 0.0

        self.children = None #actions
        self.parent = parent

        self.search_policy = None

    def set_estimation(self, prediction):

        #Set the policy and the value estimated by the neural network

        global_policy = prediction[0]
        self.estimated_policy = global_policy[self.board.legal_moves["indices"]]

        assert len(self.estimated_policy)==len(self.board.legal_moves["indices"])

        self.estimated_value = prediction[1][0]

    def expand(self):

        #Add a child node for all the possible actions (legal moves)

        self.children = []

        legal_moves = self.board.legal_moves["indices"]

        for action in legal_moves:
            new_board = self.board.move(action)
            child = Node(new_board, self)
            self.children.append(child)

    def backup_update(self, value):

        #Update the current node outcome and backup to parent nodes

        self.visit_count += 1
        self.total_outcome += value
        self.average_outcome = self.total_outcome / self.visit_count

        if self.parent is not None:
            self.parent.backup_update(value)

    def is_evaluated(self):

        return self.estimated_value is not None

    def is_leaf(self):

        return self.visit_count==0

    def is_expanded(self):

        return self.children is not None
