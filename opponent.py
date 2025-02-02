
import copy

from itertools import combinations

from main import remove_unusable_companion_cards, house_card_count

def calculate_adaptive_depth(cards, companion_cards, base_depth=6, max_depth=10):

    num_moves = len(get_valid_moves(cards))


    if num_moves > 7:
        return base_depth
    elif num_moves > 5:
        return min(base_depth + 1, max_depth)
    elif num_moves > 3:
        return min(base_depth + 2, max_depth)
    else:
        return max_depth

def heuristic2(player1, player2):

    family_max_count = {'Stark': 8, 'Greyjoy': 7, 'Lannister': 6, 'Targaryen': 5, 'Baratheon': 4, 'Tyrell': 3,
                        'Tully': 2}
    p1cards = player1.get_cards()
    p2cards = player2.get_cards()
    p1banners = player1.get_banners()
    p2banners = player2.get_banners()
    p1wins = 0
    p2wins = 0
    p1close = 0
    p2close = 0
    p1p2_house_wise_card_difference = 0

    for key, (value1, value2) in zip(p1cards.keys(), zip(p1cards.values(), p2cards.values())):
        len1 = len(value1)
        len2 = len(value2)
        dist1_to_win = len1 - (family_max_count[key] // 2)  # - (1 * len1 % 2)
        dist2_to_win = len2 - (family_max_count[key] // 2)  # - (1 * len1 % 2)

        if dist1_to_win > 0:
            p1wins += 1
        elif dist2_to_win > 0:
            p2wins += 1

        elif dist1_to_win == dist2_to_win == 0 and family_max_count[key] % 2 == 0:
            if p1banners[key] == 1:
                p1wins += 1
            else:
                p2wins += 1

        elif (family_max_count[key] % 2 == 0 and dist1_to_win == -1 and dist2_to_win < -1) or (
                family_max_count[key] % 2 == 1 and dist1_to_win == 0 and dist2_to_win < 0):
            p1close += 1
        elif (family_max_count[key] % 2 == 0 and dist2_to_win == -1 and dist1_to_win < -1) or (
                family_max_count[key] % 2 == 1 and dist2_to_win == 0 and dist1_to_win < 0):
            p2close += 1
        else:
            p1p2_house_wise_card_difference += (len1 - len2)

    s1 = p1wins - p2wins
    s2 = p1close - p2close
    w1 = 10
    w2 = 7

    return (s1 * w1) + (s2 * w2) + p1p2_house_wise_card_difference

def find_card(cards, location):
    for card in cards:
        if card.get_location() == location:
            return card


def make_move(cards, move, player):
    varys_location = find_varys(cards)

    varys_row, varys_col = varys_location // 6, varys_location % 6

    move_row, move_col = move // 6, move % 6

    selected_card = find_card(cards, move)

    removing_cards = []

    for i in range(len(cards)):
        if cards[i].get_name() == 'Varys':
            varys_index = i
            continue

        if varys_row == move_row and varys_col < move_col:
            if cards[i].get_location() // 6 == varys_row and varys_col < cards[i].get_location() % 6 < move_col and \
                    cards[i].get_house() == selected_card.get_house():
                removing_cards.append(cards[i])

                player.add_card(cards[i])

        elif varys_row == move_row and varys_col > move_col:
            if cards[i].get_location() // 6 == varys_row and move_col < cards[i].get_location() % 6 < varys_col and \
                    cards[i].get_house() == selected_card.get_house():
                removing_cards.append(cards[i])

                player.add_card(cards[i])

        elif varys_col == move_col and varys_row < move_row:
            if cards[i].get_location() % 6 == varys_col and varys_row < cards[i].get_location() // 6 < move_row and \
                    cards[i].get_house() == selected_card.get_house():
                removing_cards.append(cards[i])

                player.add_card(cards[i])

        elif varys_col == move_col and varys_row > move_row:
            if cards[i].get_location() % 6 == varys_col and move_row < cards[i].get_location() // 6 < varys_row and \
                    cards[i].get_house() == selected_card.get_house():
                removing_cards.append(cards[i])

                player.add_card(cards[i])

    player.add_card(selected_card)

    cards[varys_index].set_location(move)

    for card in removing_cards:
        cards.remove(card)

    cards.remove(selected_card)

    return selected_card.get_house()


def set_banners(player1, player2, last_house, last_turn):
    player1_cards = player1.get_cards()
    player2_cards = player2.get_cards()

    player1_banners = player1.get_banners()
    player2_banners = player2.get_banners()

    for house in player1_cards.keys():
        selected_player = None

        if len(player1_cards[house]) > len(player2_cards[house]):
            selected_player = 1

        elif len(player2_cards[house]) > len(player1_cards[house]):
            selected_player = 2

        else:
            if last_house == house:
                if last_turn == 1:
                    selected_player = 1

                else:
                    selected_player = 2

            else:
                if player1_banners[house] > player2_banners[house]:
                    selected_player = 1

                elif player2_banners[house] > player1_banners[house]:
                    selected_player = 2

        if selected_player == 1:
            player1.get_house_banner(house)
            player2.remove_house_banner(house)

        elif selected_player == 2:
            player1.remove_house_banner(house)
            player2.get_house_banner(house)


def find_varys(cards):
    varys = [card for card in cards if card.get_name() == 'Varys']

    varys_location = varys[0].get_location()

    return varys_location


def get_valid_moves(cards):
    varys_location = find_varys(cards)

    varys_row, varys_col = varys_location // 6, varys_location % 6

    moves = []

    for card in cards:
        if card.get_name() == 'Varys':
            continue

        row, col = card.get_location() // 6, card.get_location() % 6

        if row == varys_row or col == varys_col:
            moves.append(card.get_location())

    return moves


def alpha_beta_search(cards, player1, player2, companion_cards, depth, alpha, beta, is_maximizing):
    moves = get_valid_moves(cards)
    if depth == 0 or not moves:
        return heuristic2(player1, player2), None
    best_move = None
    if is_maximizing:
        max_value = float('-inf')
        for move in moves:
            new_cards, new_player1, new_player2, new_companion_cards = copy.deepcopy(cards), copy.deepcopy(
                player1), copy.deepcopy(player2), copy.deepcopy(companion_cards)
            selected_house = make_move(new_cards, move, new_player1)
            remove_unusable_companion_cards(new_cards, new_companion_cards)
            set_banners(new_player1, new_player2, selected_house, 1)
            if house_card_count(cards, selected_house) == 0 and len(companion_cards) != 0:
                move_value, _ = companion_get_move(new_cards, new_player1, new_player2, new_companion_cards)
            else:
                move_value, _ = alpha_beta_search(new_cards, new_player1, new_player2, new_companion_cards,
                                                  depth - 1,
                                                  alpha,
                                                  beta, False)

            if move_value > max_value:
                max_value, best_move = move_value, move
            alpha = max(alpha, move_value)
            if beta <= alpha:
                break
        return max_value, best_move

    else:
        min_value = float('inf')
        for move in moves:
            new_cards, new_player1, new_player2, new_companion_cards = copy.deepcopy(cards), copy.deepcopy(
                player1), copy.deepcopy(player2), copy.deepcopy(companion_cards)
            selected_house = make_move(new_cards, move, new_player2)
            remove_unusable_companion_cards(new_cards, new_companion_cards)
            set_banners(new_player1, new_player2, selected_house, 2)
            if house_card_count(cards, selected_house) == 0 and len(companion_cards) != 0:
                move_value, _ = companion_get_move(new_cards, new_player1, new_player2, new_companion_cards)
            else:
                move_value, _ = alpha_beta_search(new_cards, new_player1, new_player2, new_companion_cards,
                                                  depth - 1,
                                                  alpha,
                                                  beta, True)
            if move_value < min_value:
                min_value, best_move = move_value, move
            beta = min(beta, move_value)
            if beta <= alpha:
                break
        return min_value, best_move


def companion_get_move(cards, player1, player2, companion_cards):
    if companion_cards:
        available_companions = companion_cards
        best_move = None
        best_eval = float('-inf')


        for companion in available_companions:
            new_companion_cards = copy.deepcopy(available_companions)
            if companion == 'Jon':
                valid_targets = [card for card in cards if card.get_name() != 'Varys']
                for card in valid_targets:
                    loc = card.get_location()
                    house = card.get_house()
                    new_p1 = copy.deepcopy(player1)
                    new_p1.get_cards()[house].extend([None, None])
                    current_eval = heuristic2(new_p1, player2)
                    if current_eval > best_eval:
                        best_eval = current_eval
                        best_move = ['Jon', loc]

            elif companion == 'Gendry':
                new_p1 = copy.deepcopy(player1)
                new_p1.get_cards()['Baratheon'].append(None)  # Add one Baratheon
                current_eval = heuristic2(new_p1, player2)
                if current_eval > best_eval:
                    best_eval = current_eval
                    best_move = ['Gendry']

            elif companion == 'Ramsay':
                del new_companion_cards['Ramsay']
                valid_locations = [c.get_location() for c in cards]
                for loc1, loc2 in combinations(valid_locations, 2):
                    new_cards = copy.deepcopy(cards)
                    c1 = next(c for c in new_cards if c.get_location() == loc1)
                    c2 = next(c for c in new_cards if c.get_location() == loc2)
                    c1.set_location(loc2)
                    c2.set_location(loc1)
                    remove_unusable_companion_cards(new_cards, new_companion_cards)

                    current_eval, _ = alpha_beta_search(new_cards, player1, player2, new_companion_cards, 2,
                                                        float("-inf"), float("inf"),
                                                        False)
                    if current_eval > best_eval:
                        best_eval = current_eval
                        best_move = ['Ramsay', loc1, loc2]

            elif companion == 'Sandor':
                del new_companion_cards['Sandor']
                valid_targets = [c for c in cards if c.get_name() != 'Varys']
                for card in valid_targets:
                    loc = card.get_location()
                    new_cards = copy.deepcopy(cards)
                    new_cards.remove(next(c for c in new_cards if c.get_location() == loc))

                    remove_unusable_companion_cards(new_cards, new_companion_cards)

                    current_eval, _ = alpha_beta_search(new_cards, player1, player2, new_companion_cards, 3,
                                                        float("-inf"), float("inf"),
                                                        False)
                    if current_eval > best_eval:
                        best_eval = current_eval
                        best_move = ['Sandor', loc]

            elif companion == 'Jaqen':
                del new_companion_cards['Jaqen']
                valid_kills = [c.get_location() for c in cards if c.get_name() != 'Varys']
                for kill1, kill2 in combinations(valid_kills, 2):
                    for comp_remove in companion_cards.keys():
                        new_cards = copy.deepcopy(cards)
                        new_cards = [c for c in new_cards if c.get_location() not in (kill1, kill2)]
                        new_comp = copy.deepcopy(companion_cards)
                        new_comp[comp_remove]['Choice'] = 0  # Remove companion
                        remove_unusable_companion_cards(new_cards, new_companion_cards)

                        current_eval, _ = alpha_beta_search(new_cards, player1, player2, new_companion_cards, 1,
                                                            float("-inf"), float("inf"),
                                                            False)

                        if current_eval > best_eval:
                            best_eval = current_eval
                            best_move = ['Jaqen', kill1, kill2, comp_remove]

            elif companion == 'Melisandre':
                del new_companion_cards['Melisandre']
                current_eval, _ = alpha_beta_search(cards, player1, player2, new_companion_cards, 3, float("-inf"),
                                                    float("inf"), True)
                if current_eval > best_eval:
                    best_eval = current_eval
                    best_move = ['Melisandre']

        return best_eval, best_move
    else:
        return []


def get_move(cards, player1, player2, companion_cards, choose_companion):
    if choose_companion:
        _, move = companion_get_move(cards, player1, player2, companion_cards)
        return move

    else:
        depth = calculate_adaptive_depth(cards, companion_cards)
        _, move = alpha_beta_search(cards, player1, player2, companion_cards, depth, float('-inf'), float('inf'), True)
        return move
