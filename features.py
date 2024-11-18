from board import Board


def piece_score(state, color):
    """
    Returns piece score advantage, KING not included in scoring

    Args:
        state (Board): board state under evaluation
        color (str): player color
    Returns:
        int: score between -1 and 1
    """
    # white_count = len(state.color_coords["WHITE"])
    # black_count = len(state.color_coords["BLACK"])
    #
    # # NOTE: Assumption white piece score is 2 and black piece 1.
    # score = 2 * white_count - black_count
    #
    # normalized_score = score / 16
    #
    # if color == "WHITE":
    #     return normalized_score
    # return -normalized_score

    w_score = 0
    for w in state.color_coords["WHITE"]:
        # w_score += (abs(w[0] - 4)+abs(w[1] - 4))/8 * 2 - 1
        cnt = 0
        if (
            state.coords_color.get((w[0], w[1] + 1), None) is None
            or state.coords_color.get((w[0], w[1] + 1), None) == "BLACK"
        ):
            cnt += 1
        if (
            state.coords_color.get((w[0] + 1, w[1]), None) is None
            or state.coords_color.get((w[0] + 1, w[1]), None) == "BLACK"
        ):
            cnt += 1
        if (
            state.coords_color.get((w[0], w[1] - 1), None) is None
            or state.coords_color.get((w[0], w[1] - 1), None) == "BLACK"
        ):
            cnt += 1
        if (
            state.coords_color.get((w[0] - 1, w[1]), None) is None
            or state.coords_color.get((w[0] - 1, w[1]), None) == "BLACK"
        ):
            cnt += 1

        w_score += cnt / 3 * 2 - 1
    print(w_score)

    b_score = 0
    k = state.get_king_coords()
    for b in state.color_coords["BLACK"]:
        b_score += 1 - (abs(b[0] - k[0]) + abs(b[1] - k[1])) / 7

    normalized_score = (w_score - b_score) / 8

    if color == "WHITE":
        return normalized_score
    return -normalized_score


# WHITE features
def king_safety(state, color):
    """
    Returns safety score: number of black pieces missing for king capture

    Args:
        state (Board): board state under evaluation

    Returns:
        int: score between -1 and 1
    """
    king_position = state.get_king_coords()

    if king_position == (4, 4):  # king oh throne
        required_for_capture = 4

    elif king_position in ((4, 5), (5, 4), (4, 3), (3, 4)):  # king next to throne
        required_for_capture = 3

    else:
        required_for_capture = 2

    close_blacks = 0
    if (
        state.coords_color.get((king_position[0] - 1, king_position[1]), None)
        == "BLACK"
        or Board.coords_noenter.get((king_position[0] - 1, king_position[1]), "EMPTY")
        in "LRUD"
    ):  # Up square check
        close_blacks += 1
    if (
        state.coords_color.get((king_position[0] + 1, king_position[1]), None)
        == "BLACK"
        or Board.coords_noenter.get((king_position[0] + 1, king_position[1]), "EMPTY")
        in "LRUD"
    ):  # Down square check
        close_blacks += 1
    if (
        state.coords_color.get((king_position[0], king_position[1] - 1), None)
        == "BLACK"
        or Board.coords_noenter.get((king_position[0], king_position[1] - 1), "EMPTY")
        in "LRUD"
    ):  # Left square check
        close_blacks += 1
    if (
        state.coords_color.get((king_position[0], king_position[1] + 1), None)
        == "BLACK"
        or Board.coords_noenter.get((king_position[0], king_position[1] + 1), "EMPTY")
        in "LRUD"
    ):  # Right square check
        close_blacks += 1

    normalized_score = (required_for_capture - close_blacks) / 2 - 1
    if color == "BLACK":
        return -normalized_score
    return normalized_score


def capture_king(state, color):
    if state.get_king_coords() is None:
        print("king is dead")
        if color == "WHITE":
            return float("-inf")
        else:
            return float("inf")
    return 0


def win_move_king(state, color):
    king_position = state.get_king_coords()
    found = False
    if king_position[1] in (0, 8) or king_position[0] in (0, 8):
        if color == "WHITE":
            return float("inf")
        else:
            return float("-inf")

    if king_position[0] not in (2, 6) and king_position[1] not in (2, 6):
        return 0

    if king_position[0] in (2, 6):
        for col in range(9):
            if state.coords_color.get((king_position[0], col), None) is not None and (
                king_position[0],
                col,
            ) != (king_position[0], king_position[1]):
                found = True
                break
    elif king_position[1] in (2, 6):
        for row in range(9):
            if state.coords_color.get((row, king_position[1]), None) is not None and (
                row,
                king_position[1],
            ) != (king_position[0], king_position[1]):
                found = True
                break

    if not found:  # not found
        if color == "WHITE":
            return 100
        else:
            return -100
    return 0


def king_distance(state, color):

    black_coords = state.color_coords["BLACK"]
    king_position = state.get_king_coords()

    tr_angle = (0, 8)
    tl_angle = (0, 0)
    bl_angle = (8, 0)
    br_angle = (8, 8)

    # top right quadrant
    q_tr = ((1, 6), (1, 7), (2, 6), (2, 7))
    vq_tr = ((0, 6), (0, 7))
    hq_tr = ((1, 8), (2, 8))
    dict_q_tr = {"row1": 0, "row2": 0, "col6": 0, "col7": 0}

    # top left quadrant
    q_tl = ((1, 1), (1, 2), (2, 1), (2, 2))
    vq_tl = ((0, 1), (0, 2))
    hq_tl = ((1, 0), (2, 0))
    dict_q_tl = {"row1": 0, "row2": 0, "col1": 0, "col2": 0}

    # bottom left quadrant
    q_bl = ((6, 1), (6, 2), (7, 1), (7, 2))
    vq_bl = ((6, 0), (7, 0))
    hq_bl = ((8, 1), (8, 2))
    dict_q_bl = {"row6": 0, "row7": 0, "col1": 0, "col2": 0}

    # bottom right quadrant
    q_br = ((6, 6), (6, 7), (7, 6), (7, 7))
    vq_br = ((6, 8), (7, 8))
    hq_br = ((8, 6), (8, 7))
    dict_q_br = {"row6": 0, "row7": 0, "col6": 0, "col7": 0}

    # final for
    for b in black_coords:
        if b in q_tr:
            dict_q_tr["row" + str(b[0])] = 1
            dict_q_tr["col" + str(b[1])] = 1
        elif b in q_tl:
            dict_q_tl["row" + str(b[0])] = 1
            dict_q_tl["col" + str(b[1])] = 1
        elif b in q_bl:
            dict_q_bl["row" + str(b[0])] = 1
            dict_q_bl["col" + str(b[1])] = 1
        elif b in q_br:
            dict_q_br["row" + str(b[0])] = 1
            dict_q_br["col" + str(b[1])] = 1
        elif b in vq_tr:
            dict_q_tr["col" + str(b[1])] = 1
        elif b in vq_bl:
            dict_q_bl["col" + str(b[1])] = 1
        elif b in vq_tl:
            dict_q_tl["col" + str(b[1])] = 1
        elif b in vq_br:
            dict_q_br["col" + str(b[1])] = 1
        elif b in hq_tr:
            dict_q_tr["row" + str(b[0])] = 1
        elif b in hq_tl:
            dict_q_tl["row" + str(b[0])] = 1
        elif b in hq_bl:
            dict_q_bl["row" + str(b[0])] = 1
        elif b in hq_br:
            dict_q_br["row" + str(b[0])] = 1

        count_q_tr = sum(dict_q_tr.values())
        count_q_tl = sum(dict_q_tl.values())
        count_q_bl = sum(dict_q_bl.values())
        count_q_br = sum(dict_q_br.values())

    # manhattan distance from king to angles
    dist_tr = abs(king_position[0] - tr_angle[0]) + abs(king_position[1] - tr_angle[1])
    dist_tl = abs(king_position[0] - tl_angle[0]) + abs(king_position[1] - tl_angle[1])
    dist_br = abs(king_position[0] - br_angle[0]) + abs(king_position[1] - br_angle[1])
    dist_bl = abs(king_position[0] - bl_angle[0]) + abs(king_position[1] - bl_angle[1])

    # distance/4 -> to test
    final_score = min(
        (
            dist_tr / 4 + count_q_tr,
            dist_tl / 4 + count_q_tl,
            dist_br / 4 + count_q_br,
            dist_bl / 4 + count_q_bl,
        )
    )

    # normalize the final_score between -1 and 1
    # max valuer count_q = 4, min value = 0
    # distance min value = 0, max value = 14/4
    # max value final_score = 7,5, min value = 0.25
    normalized_score = ((final_score - 0.25) / 7.25) * 2 - 1
    if color == "BLACK":
        return normalized_score
    return -normalized_score
