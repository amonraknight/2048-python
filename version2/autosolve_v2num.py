import random
from functools import lru_cache
import numpy as np

import constants as c
from version2 import logic_v2num

commands = {
    c.KEY_UP: logic_v2num.up,
    c.KEY_DOWN: logic_v2num.down,
    c.KEY_LEFT: logic_v2num.left,
    c.KEY_RIGHT: logic_v2num.right
}


def convert_matrix_to_string(mat):
    # print(mat)
    return str(mat)

# '[[0 2 0 0]
#  [0 0 0 0]
#  [0 0 0 0]
#  [0 0 2 0]]'


def convert_string_to_matrix(mat_string):
    mat_string = mat_string.replace('[[', '').replace(']]', '')
    rows = mat_string.split(']\n [')
    mat = np.zeros((c.GRID_LEN, c.GRID_LEN), dtype=np.int)
    for index, each_row_str in enumerate(rows):
        mat[index] = np.fromstring(each_row_str, dtype=np.int, sep=' ')
    return mat


def get_comprehensive_score(mat):
    return logic_v2num.score_monotone(mat) * 50 + logic_v2num.score_weighted_squares(mat)


@lru_cache
def get_comprehensive_score_cache(mat_string):
    return get_comprehensive_score(convert_string_to_matrix(mat_string))


def get_solution_2(mat):
    # The setting here defines the depth of predictions. The deeper the prediction goes, the slower the moves.

    highest_score, high_score_moves = get_recur_best_score(mat, 0, c.RECUR_DEPTH)

    if len(high_score_moves) == 0:
        return 'STOP'
    elif len(high_score_moves) == 1:
        return high_score_moves.pop()
    else:
        return high_score_moves[random.randint(0, len(high_score_moves) - 1)]


@lru_cache
def get_solution_2_cache(mat_str):
    # The setting here defines the depth of predictions. The deeper the prediction goes, the slower the moves.
    mat = convert_string_to_matrix(mat_str)
    highest_score, high_score_moves = get_recur_best_score(mat, 0, c.RECUR_DEPTH)

    if len(high_score_moves) == 0:
        return 'STOP'
    elif len(high_score_moves) == 1:
        return high_score_moves.pop()
    else:
        return high_score_moves[random.randint(0, len(high_score_moves) - 1)]


# Predict the best score in the next n steps.
def get_recur_best_score(mat, current_step, max_depth):
    # End the search when reaching the depth limit.
    if current_step >= max_depth:
        # return get_comprehensive_score(mat), []
        return get_comprehensive_score_cache(convert_matrix_to_string(mat)), []

    # Actually the less the better. If there is no move possible, of course give it the worse score.
    highest_score = 99999
    high_score_moves = []
    for each_possible_move in [c.KEY_UP, c.KEY_DOWN, c.KEY_LEFT, c.KEY_RIGHT]:
        next_matrix, done = commands[each_possible_move](mat)
        if done:
            # Calculate the average score of the random filling.
            current_score = calculate_average_of_sampled_filling(next_matrix, current_step + 1, max_depth)
            if highest_score == current_score:
                high_score_moves.append(each_possible_move)
            elif highest_score > current_score:
                highest_score = current_score
                high_score_moves.clear()
                high_score_moves.append(each_possible_move)

    return highest_score, high_score_moves


# Instead of calculating all possible fillings of “2” or “4”, choose randomly 4 samples to fill and get the score.
def calculate_average_of_sampled_filling(mat, current_step, max_depth):
    total_score = 0

    # Is it wiser to move in more caution when there are many squares but boldly when there are less.
    empty_cells = logic_v2num.score_number_of_empty_squares(mat)
    sample_amount = round(min(empty_cells, 16 - empty_cells) / 2, 0) + 1

    sample_count = 0
    while sample_count < sample_amount:
        a = random.randint(0, len(mat) - 1)
        b = random.randint(0, len(mat) - 1)
        while mat[a][b] != 0:
            a = random.randint(0, len(mat) - 1)
            b = random.randint(0, len(mat) - 1)

        # If to be filled with 2.
        mat_fill_2 = mat[:]
        mat_fill_2[a][b] = 2
        best_score_2, high_score_moves_2 = get_recur_best_score(mat_fill_2, current_step, max_depth)
        # If to be filled with 4.
        mat_fill_4 = mat[:]
        mat_fill_4[a][b] = 4
        best_score_4, high_score_moves_4 = get_recur_best_score(mat_fill_4, current_step, max_depth)

        total_score = total_score + best_score_2 * 0.9 + best_score_4 * 0.1
        sample_count += 1

    return total_score / sample_amount
