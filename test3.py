import random
import copy

from main import make_move, set_banners
from itertools import combinations, permutations


def find_varys(cards):
    varys = [card for card in cards if card.get_name() == 'Varys']
    return varys[0].get_location() if varys else None


def get_valid_ramsay(cards):
    '''
    This function gets the possible moves for Ramsay.

    Parameters:
        cards (list): list of Card objects

    Returns:
        moves (list): list of possible moves
    '''

    moves = []

    for card in cards:
        moves.append(card.get_location())

    return moves


def get_valid_jon_sandor_jaqan(cards):
    '''
    This function gets the possible moves for Jon Snow, Sandor Clegane, and Jaqen H'ghar.

    Parameters:
        cards (list): list of Card objects

    Returns:
        moves (list): list of possible moves
    '''

    moves = []

    for card in cards:
        if card.get_name() != 'Varys':
            moves.append(card.get_location())

    return moves


def get_valid_moves(cards):
    varys_location = find_varys(cards)
    if varys_location is None:
        return []
    varys_row, varys_col = divmod(varys_location, 6)
    return [card.get_location() for card in cards if card.get_name() != 'Varys' and (
                card.get_location() // 6 == varys_row or card.get_location() % 6 == varys_col)]


def evaluation(player1, player2):
    # Simple evaluation: maximize player's cards minus opponent's cards
    # return sum(len(v) for v in player1.get_cards().values()) - sum(len(v) for v in player2.get_cards().values())
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


def minimax(cards, player1, player2, depth, alpha, beta, maximizing_player):
    moves = get_valid_moves(cards)
    if depth == 0 or not moves:
        return evaluation(player1, player2), None
    best_move = None
    if maximizing_player:
        max_eval = float('-inf')
        for move in moves:
            new_cards, new_player1, new_player2 = copy.deepcopy(cards), copy.deepcopy(player1), copy.deepcopy(player2)
            selected_house = make_move(new_cards, move, new_player1)
            set_banners(new_player1, new_player2, selected_house, 1)
            eval, _ = minimax(new_cards, new_player1, new_player2, depth - 1, alpha, beta, False)
            if eval > max_eval:
                max_eval, best_move = eval, move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in moves:
            new_cards, new_player1, new_player2 = copy.deepcopy(cards), copy.deepcopy(player1), copy.deepcopy(player2)
            selected_house = make_move(new_cards, move, new_player2)
            set_banners(new_player1, new_player2, selected_house, 2)
            eval, _ = minimax(new_cards, new_player1, new_player2, depth - 1, alpha, beta, True)
            if eval < min_eval:
                min_eval, best_move = eval, move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move


def get_move(cards, player1, player2, companion_cards, choose_companion):
    if choose_companion:
        available_companions = companion_cards
        best_move = None
        best_eval = float('-inf')

        # Helper function to evaluate a simulated state
        def evaluate_simulation(new_cards, new_p1, new_p2):
            # Update banners based on new card positions (if necessary)
            # This might require recalculating banners similar to how set_banners works
            return evaluation(new_p1, new_p2)

        # Check each available companion
        for companion in available_companions:
            if companion == 'Jon':
                # Jon Snow: [companion_name, location]
                valid_targets = [card for card in cards if card.get_name() != 'Varys']
                for card in valid_targets:
                    loc = card.get_location()
                    house = card.get_house()  # Assuming get_house() exists
                    new_p1 = copy.deepcopy(player1)
                    # Simulate adding two to the house (append dummy entries)
                    new_p1.get_cards()[house].extend([None, None])
                    current_eval = evaluation(new_p1, player2)
                    if current_eval > best_eval:
                        best_eval = current_eval
                        best_move = ['Jon', loc]

            elif companion == 'Gendry':
                # Gendry: [companion_name]
                new_p1 = copy.deepcopy(player1)
                new_p1.get_cards()['Baratheon'].append(None)  # Add one Baratheon
                current_eval = evaluation(new_p1, player2)
                if current_eval > best_eval:
                    best_eval = current_eval
                    best_move = ['Gendry']

            elif companion == 'Ramsay':
                # Ramsay: [companion, loc1, loc2]
                valid_locations = [c.get_location() for c in cards]
                for loc1, loc2 in permutations(valid_locations, 2):
                    new_cards = copy.deepcopy(cards)
                    # Swap positions
                    c1 = next(c for c in new_cards if c.get_location() == loc1)
                    c2 = next(c for c in new_cards if c.get_location() == loc2)
                    c1.set_location(loc2)
                    c2.set_location(loc1)
                    # Evaluate new board state
                    current_eval = evaluate_simulation(new_cards, player1, player2)
                    if current_eval > best_eval:
                        best_eval = current_eval
                        best_move = ['Ramsay', loc1, loc2]

            elif companion == 'Sandor':
                # Sandor: [companion, location]
                valid_targets = [c for c in cards if c.get_name() != 'Varys']
                for card in valid_targets:
                    loc = card.get_location()
                    new_cards = copy.deepcopy(cards)
                    new_cards.remove(next(c for c in new_cards if c.get_location() == loc))
                    # Simulate killing the card
                    current_eval = evaluate_simulation(new_cards, player1, player2)
                    if current_eval > best_eval:
                        best_eval = current_eval
                        best_move = ['Sandor', loc]

            elif companion == 'Jaqen':
                # Jaqen: [companion, loc1, loc2, companion_to_remove]
                valid_kills = [c.get_location() for c in cards if c.get_name() != 'Varys']
                for kill1, kill2 in combinations(valid_kills, 2):
                    for comp_remove in companion_cards.keys():
                        new_cards = copy.deepcopy(cards)
                        new_cards = [c for c in new_cards if c.get_location() not in (kill1, kill2)]
                        new_comp = copy.deepcopy(companion_cards)
                        new_comp[comp_remove]['Choice'] = 0  # Remove companion
                        current_eval = evaluate_simulation(new_cards, player1, player2)
                        if current_eval > best_eval:
                            best_eval = current_eval
                            best_move = ['Jaqen', kill1, kill2, comp_remove]

            elif companion == 'Melisandre':
                # Melisandre: [companion]
                current_eval = evaluation(player1, player2)
                if current_eval > best_eval:
                    best_eval = current_eval
                    best_move = ['Melisandre']

        return best_move if best_move else [random.choice(available_companions)]
    else:
        _, move = minimax(cards, player1, player2, 6, float('-inf'), float('inf'), True)
        return move