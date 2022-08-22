#
# CS1010FC --- Programming Methodology
#
# Mission N Solutions
#
# Note that written answers are commented out to allow us to run your
# code easily while grading your problem set.

import random

import numpy as np

import constants as c


#######
# Task 1a #
#######

# [Marking Scheme]
# Points to note:
# Matrix elements must be equal but not identical
# 1 mark for creating the correct matrix


def new_game(n):
    matrix = np.zeros((n, n), dtype=np.int)

    matrix = add_two_or_four(matrix)
    matrix = add_two_or_four(matrix)

    return matrix


###########
# Task 1b #
###########

# [Marking Scheme]
# Points to note:
# Must ensure that it is created on a zero entry
# 1 mark for creating the correct loop

def add_two_or_four(mat):
    a = random.randint(0, len(mat) - 1)
    b = random.randint(0, len(mat) - 1)
    # Find a random cell, if not blank, find next.
    while mat[a][b] != 0:
        a = random.randint(0, len(mat) - 1)
        b = random.randint(0, len(mat) - 1)

    if random.randint(0, 9) < 9:
        mat[a][b] = 2
    else:
        mat[a][b] = 4

    return mat


###########
# Task 1c #
###########

# [Marking Scheme]
# Points to note:
# Matrix elements must be equal but not identical
# 0 marks for completely wrong solutions
# 1 mark for getting only one condition correct
# 2 marks for getting two of the three conditions
# 3 marks for correct checking

def game_state(mat):
    # check for win cell
    if np.any(mat == 2048):
        return 'win'
    elif np.any(mat == 0):
        return 'not over'
    else:
        # check for same cells that touch each other
        for i in range(len(mat) - 1):
            # intentionally reduced to check the row on the right and below
            # more elegant to use exceptions but most likely this will be their solution
            for j in range(len(mat[0]) - 1):
                if mat[i][j] == mat[i + 1][j] or mat[i][j + 1] == mat[i][j]:
                    return 'not over'
        for k in range(len(mat) - 1):  # to check the left/right entries on the last row
            if mat[len(mat) - 1][k] == mat[len(mat) - 1][k + 1]:
                return 'not over'
        for j in range(len(mat) - 1):  # check up/down entries on last column
            if mat[j][len(mat) - 1] == mat[j + 1][len(mat) - 1]:
                return 'not over'

    return 'lose'


###########
# Task 2a #
###########

# [Marking Scheme]
# Points to note:
# 0 marks for completely incorrect solutions
# 1 mark for solutions that show general understanding
# 2 marks for correct solutions that work for all sizes of matrices
# Reverse horizontally

def reverse(mat):
    return mat[:, ::-1]


###########
# Task 2b #
###########

# [Marking Scheme]
# Points to note:
# 0 marks for completely incorrect solutions
# 1 mark for solutions that show general understanding
# 2 marks for correct solutions that work for all sizes of matrices

def transpose(mat):
    return mat.transpose()


##########
# Task 3 #
##########

# "done" is true when any cell moved or merged. Otherwise, false.
def shuffle_to_left(mat):
    done = False
    for i in range(c.GRID_LEN):
        pos_l, pos_r = 0, 1
        while pos_r < c.GRID_LEN:
            # m,n>0; m!=n
            # 0, 0
            if mat[i][pos_l] == mat[i][pos_r] and mat[i][pos_r] == 0:
                pos_r += 1
            # 0, m
            elif mat[i][pos_l] == 0 and mat[i][pos_r] > 0:
                mat[i][pos_l] = mat[i][pos_r]
                mat[i][pos_r] = 0
                pos_l = pos_r
                pos_r += 1
                done = True
            # m, m
            elif mat[i][pos_l] == mat[i][pos_r] and mat[i][pos_r] > 0:
                mat[i][pos_l] *= 2
                mat[i][pos_r] == 0
                pos_l = pos_r
                pos_r += 1
                done = True
            # m, 0
            # m, n
            elif mat[i][pos_l] > 0 and mat[i][pos_r] == 0:
                pos_l += 1
                pos_r += 1

    return mat, done


def up(game):
    # print("up")
    # return matrix after shifting up
    game = transpose(game)
    game, done = shuffle_to_left(game)
    game = transpose(game)
    return game, done


def down(game):
    # print("down")
    # return matrix after shifting down
    game = reverse(transpose(game))
    game, done = shuffle_to_left(game)
    game = transpose(reverse(game))
    return game, done


def left(game):
    # print("left")
    # return matrix after shifting left
    game, done = shuffle_to_left(game)
    return game, done


def right(game):
    # print("right")
    # return matrix after shifting right
    game = reverse(game)
    game, done = shuffle_to_left(game)
    game = reverse(game)
    return game, done


# This is the scoring according to how many times the matrix breaks the monotone in all rows and columns.
# The larger the score is, the worse the matrix is.
def score_monotone(mat):
    return score_monotone_for_rows(mat) + score_monotone_for_rows(transpose(mat))


# For each column

def score_monotone_for_rows(mat):
    rst_score = 0
    # For each row
    for each_row in mat:
        previous_item = 0
        previous_tone = 'unknown'
        for index, each_item in enumerate(each_row):
            if each_item != 0 and index > 0:
                if previous_item != 0 and previous_tone == 'unknown':
                    if previous_item > each_item:
                        previous_tone = 'dec'
                    elif previous_item < each_item:
                        previous_tone = 'inc'
                elif previous_tone == 'inc':
                    if previous_item > each_item:
                        rst_score += 1
                        previous_tone = 'dec'
                elif previous_tone == 'dec':
                    if previous_item < each_item:
                        rst_score += 1
                        previous_tone = 'inc'

            if each_item != 0:
                previous_item = each_item

    return rst_score


def score_number_of_squares(mat):
    rst_score = 0
    for each_row in mat:
        rst_score += (len(each_row) - each_row.count(0))

    return rst_score


def score_number_of_empty_squares(mat):
    cnt_array = np.where(mat, 0, 1)
    return np.sum(cnt_array)


def score_weighted_squares(mat):
    rst_score = 0
    for each_row in mat:
        for each_item in each_row:
            if each_item != 0:
                rst_score += np.log2(each_item)

    return rst_score
