import random
import numpy as np
import math


class AI:
    def stack(board):
        new_matrix = [[0] * 4 for _ in range(4)]

        for i in range(4):
            fill_position = 0
            for j in range(4):
                if board[i][j] != 0:
                    new_matrix[i][fill_position] = board[i][j]
                    fill_position += 1
        return new_matrix

    def combine(board):
        score = 0
        for i in range(4):
            for j in range(3):
                if board[i][j] != 0 and board[i][j] == board[i][j + 1]:
                    board[i][j] *= 2
                    board[i][j + 1] = 0
                    score += board[i][j]
        return score, board

    def reverse(board):
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(board[i][3 - j])
        return new_matrix

    def transpose(board):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = board[j][i]
        return new_matrix

    def left(board):
        board = AI.stack(board)
        score, board = AI.combine(board)
        board = AI.stack(board)
        board = AI.new_tile(board)
        return score, board

    def right(board):
        board = AI.reverse(board)
        board = AI.stack(board)
        score, board = AI.combine(board)
        board = AI.stack(board)
        board = AI.reverse(board)
        board = AI.new_tile(board)
        return score, board

    def up(board):
        board = AI.transpose(board)
        board = AI.stack(board)
        score, board = AI.combine(board)
        board = AI.stack(board)
        board = AI.transpose(board)
        board = AI.new_tile(board)
        return score, board

    def down(board):
        board = AI.transpose(board)
        board = AI.reverse(board)
        board = AI.stack(board)
        score, board = AI.combine(board)
        board = AI.stack(board)
        board = AI.reverse(board)
        board = AI.transpose(board)
        board = AI.new_tile(board)
        return score, board

    # def new_tile(board):
    #     while True:
    #         row = random.randint(0, 3)
    #         col = random.randint(0, 3)
    #         if board[row][col] == 0:
    #             if random.randint(1, 10) == 5:
    #                 board[row][col] = 4
    #             else:
    #                 board[row][col] = 2
    #             return board

    def new_tile(board):
        for i in range(4):
            for j in range(4):
                if board[i][j] == 0:
                    board[i][j] = 2
                    return board
        return board

    def minmax(board, depth, maximize):
        if depth == 8:
            return 0
        l_score, tmpboard = AI.left(board)
        l_score = l_score + AI.minmax(tmpboard, depth + 1, not maximize)

        r_score, tmpboard = AI.right(board)
        r_score = r_score + AI.minmax(tmpboard, depth + 1, not maximize)

        u_score, tmpboard = AI.up(board)
        u_score = u_score + AI.minmax(tmpboard, depth + 1, not maximize)

        d_score, tmpboard = AI.down(board)
        d_score = d_score + AI.minmax(tmpboard, depth + 1, not maximize)
        if maximize:
            return np.max([u_score, d_score, r_score, l_score])
        else:
            return np.min([u_score, d_score, r_score, l_score])

    def main(board):
        # global board
        # board = np.zeros((4, 4), dtype=np.int64)
        score = 0
        l_score, tmpboard = AI.left(board)
        l_score = l_score + AI.minmax(tmpboard, 1, False)
        score = l_score
        move = "left"

        r_score, tmpboard = AI.right(board)
        r_score = r_score + AI.minmax(tmpboard, 1, False)
        if score < r_score:
            score = r_score
            move = "right"

        u_score, tmpboard = AI.up(board)
        u_score = u_score + AI.minmax(tmpboard, 1, False)
        if score < u_score:
            score = u_score
            move = "up"

        d_score, tmpboard = AI.down(board)
        d_score = d_score + AI.minmax(tmpboard, 1, False)
        if score < d_score:
            score = d_score
            move = "down"

        return move
