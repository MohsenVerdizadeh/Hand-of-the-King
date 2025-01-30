import random

import copy

import math

temp = {
    "Stark": 8,
    "Greyjoy": 7,
    "Lannister": 6,
    "Targaryen": 5,
    "Baratheon": 4,
    "Tyrell": 3,
    "Tully": 2,
}
depth = 6


def is_terminal(cards, depth_1, list1, list2):
    global depth
    if len(get_valid_moves(cards, list1, list2)) == 0 or depth == depth_1:
        return True
    return False


def test(player):
    score = 0
    for house, people in player.get_cards().items():
        score += (len(people) / temp[house])
    return score


def heuristic(player1, player2):
    player1_score = test(player1)
    player2_score = test(player2)
    return player1_score - player2_score


def calculate_winner(player1, player2):
    '''
    This function determines the winner of the game.

    Parameters:
        player1 (Player): player 1
        player2 (Player): player 2

    Returns:
        winner (int): 1 if player 1 wins, 2 if player 2 wins
    '''

    player1_banners = player1.get_banners()
    player2_banners = player2.get_banners()

    # Calculate the scores of the players
    player1_score = sum(player1_banners.values())
    player2_score = sum(player2_banners.values())

    if player1_score > player2_score:
        return 1

    elif player2_score > player1_score:
        return 2

    # If the scores are the same, whoever has the banner of the house with the most cards wins
    else:
        if player1_banners['Stark'] > player2_banners['Stark']:
            return 1

        elif player2_banners['Stark'] > player1_banners['Stark']:
            return 2

        elif player1_banners['Greyjoy'] > player2_banners['Greyjoy']:
            return 1

        elif player2_banners['Greyjoy'] > player1_banners['Greyjoy']:
            return 2

        elif player1_banners['Lannister'] > player2_banners['Lannister']:
            return 1

        elif player2_banners['Lannister'] > player1_banners['Lannister']:
            return 2

        elif player1_banners['Targaryen'] > player2_banners['Targaryen']:
            return 1

        elif player2_banners['Targaryen'] > player1_banners['Targaryen']:
            return 2

        elif player1_banners['Baratheon'] > player2_banners['Baratheon']:
            return 1

        elif player2_banners['Baratheon'] > player1_banners['Baratheon']:
            return 2

        elif player1_banners['Tyrell'] > player2_banners['Tyrell']:
            return 1

        elif player2_banners['Tyrell'] > player1_banners['Tyrell']:
            return 2

        elif player1_banners['Tully'] > player2_banners['Tully']:
            return 1

        elif player2_banners['Tully'] > player1_banners['Tully']:
            return 2


def find_card(cards, location):
    '''
    This function finds the card at the location.

    Parameters:
        cards (list): list of Card objects
        location (int): location of the card

    Returns:
        card (Card): card at the location
    '''

    for card in cards:
        if card.get_location() == location:
            return card


def make_move(cards, move, player):
    '''
    This function makes a move for the player.

    Parameters:
        cards (list): list of Card objects
        move (int): location of the card
        player (Player): player making the move
    '''

    # Get the location of Varys
    varys_location = find_varys(cards)

    # Find the row and column of Varys
    varys_row, varys_col = varys_location // 6, varys_location % 6

    # Get the row and column of the move
    move_row, move_col = move // 6, move % 6

    # Find the selected card
    selected_card = find_card(cards, move)

    removing_cards = []

    # Find the cards that should be removed
    for i in range(len(cards)):
        if cards[i].get_name() == 'Varys':
            varys_index = i
            continue

        # If the card is between Varys and the selected card and has the same house as the selected card
        if varys_row == move_row and varys_col < move_col:
            if cards[i].get_location() // 6 == varys_row and varys_col < cards[i].get_location() % 6 < move_col and \
                    cards[i].get_house() == selected_card.get_house():
                removing_cards.append(cards[i])

                # Add the card to the player's cards
                player.add_card(cards[i])

        elif varys_row == move_row and varys_col > move_col:
            if cards[i].get_location() // 6 == varys_row and move_col < cards[i].get_location() % 6 < varys_col and \
                    cards[i].get_house() == selected_card.get_house():
                removing_cards.append(cards[i])

                # Add the card to the player's cards
                player.add_card(cards[i])

        elif varys_col == move_col and varys_row < move_row:
            if cards[i].get_location() % 6 == varys_col and varys_row < cards[i].get_location() // 6 < move_row and \
                    cards[i].get_house() == selected_card.get_house():
                removing_cards.append(cards[i])

                # Add the card to the player's cards
                player.add_card(cards[i])

        elif varys_col == move_col and varys_row > move_row:
            if cards[i].get_location() % 6 == varys_col and move_row < cards[i].get_location() // 6 < varys_row and \
                    cards[i].get_house() == selected_card.get_house():
                removing_cards.append(cards[i])

                # Add the card to the player's cards
                player.add_card(cards[i])

    # Add the selected card to the player's cards
    player.add_card(selected_card)

    # Set the location of Varys
    cards[varys_index].set_location(move)

    # Remove the cards
    for card in removing_cards:
        cards.remove(card)

    # Remove the selected card
    cards.remove(selected_card)

    # Return the selected card's house
    return selected_card.get_house()


def set_banners(player1, player2, last_house, last_turn):
    '''
    This function sets the banners for the players.

    Parameters:
        player1 (Player): player 1
        player2 (Player): player 2
        last_house (str): house of the last chosen card
        last_turn (int): last turn of the player

    Returns:
        player1_status (dict): status of the cards for player 1
        player2_status (dict): status of the cards for player 2
    '''

    # Get the cards of the players
    player1_cards = player1.get_cards()
    player2_cards = player2.get_cards()

    # Get the banners of the players
    player1_banners = player1.get_banners()
    player2_banners = player2.get_banners()

    for house in player1_cards.keys():
        # Flag to keep track of the selected player
        selected_player = None

        # The player with the more cards of a house gets the banner
        if len(player1_cards[house]) > len(player2_cards[house]):
            # Give the banner to player 1
            selected_player = 1

        elif len(player2_cards[house]) > len(player1_cards[house]):
            # Give the banner to player 2
            selected_player = 2

        # If the number of cards is the same, the player who chose the last card of that house gets the banner
        else:
            if last_house == house:
                if last_turn == 1:
                    # Give the banner to player 1
                    selected_player = 1

                else:
                    # Give the banner to player 2
                    selected_player = 2

            else:  # If the last card was not of the same house
                if player1_banners[house] > player2_banners[house]:  # If player 1 has more banners of the house
                    selected_player = 1

                elif player2_banners[house] > player1_banners[house]:  # If player 2 has more banners of the house
                    selected_player = 2

        # If player 1 should get the banner
        if selected_player == 1:
            # Give the banner to player 1
            player1.get_house_banner(house)
            player2.remove_house_banner(house)

        elif selected_player == 2:
            # Give the banner to player 2
            player1.remove_house_banner(house)
            player2.get_house_banner(house)


def find_varys(cards):
    '''
    This function finds the location of Varys on the board.

    Parameters:
        cards (list): list of Card objects

    Returns:
        varys_location (int): location of Varys
    '''

    varys = [card for card in cards if card.get_name() == 'Varys']

    varys_location = varys[0].get_location()

    return varys_location


def get_valid_moves(cards, list1, list2):
    '''
    This function gets the possible moves for the player.

    Parameters:
        cards (list): list of Card objects

    Returns:
        moves (list): list of possible moves
    '''

    # Get the location of Varys
    varys_location = find_varys(cards)

    # Get the row and column of Varys
    varys_row, varys_col = varys_location // 6, varys_location % 6

    moves = []

    # Get the cards in the same row or column as Varys
    for card in cards:
        if card.get_name() == 'Varys' or card.get_house() in list1 or card.get_house() in list2:
            continue

        row, col = card.get_location() // 6, card.get_location() % 6

        if row == varys_row or col == varys_col:
            moves.append(card.get_location())

    return moves


def update_list(player, list, selected_house):
    if len(player.get_cards()[selected_house]) / temp[selected_house] > 0.5:
        list.append(selected_house)


def max_value(cards, player1, player2, move, depth, alpha, beta, list1, list2):
    selected_house = make_move(cards, move, player2)
    set_banners(player1, player2, selected_house, 2)
    update_list(player2, list2, selected_house)

    if is_terminal(cards, depth, list1, list2):
        return heuristic(player1, player2)

    max_eval = -math.inf
    moves = get_valid_moves(cards, list1, list2)
    for move in moves:
        eval = min_value(copy.deepcopy(cards), copy.deepcopy(player1), copy.deepcopy(player2), move, depth + 1,
                         alpha,
                         beta, copy.deepcopy(list1), copy.deepcopy(list2))
        max_eval = max(max_eval, eval)
        alpha = max(alpha, eval)
        if beta <= alpha:
            break
    return max_eval


def min_value(cards, player1, player2, move, depth, alpha, beta, list1, list2):
    selected_house = make_move(cards, move, player1)
    set_banners(player1, player2, selected_house, 1)
    update_list(player1, list1, selected_house)

    if is_terminal(cards, depth, list1, list2):
        return heuristic(player1, player2)

    min_eval = math.inf
    moves = get_valid_moves(cards, list1, list2)
    for move in moves:
        eval = max_value(copy.deepcopy(cards), copy.deepcopy(player1), copy.deepcopy(player2), move, depth + 1,
                         alpha,
                         beta, copy.deepcopy(list1), copy.deepcopy(list2))
        min_eval = min(min_eval, eval)
        beta = min(beta, eval)
        if beta <= alpha:
            break
    return min_eval


def create_list(player):
    result = []
    for house, people in player.get_cards().items():
        if len(people) / temp[house] > 0.5:
            result.append(house)

    return result


def calculate_depth(branch_factor):
    result = 0
    while True:
        if (branch_factor ** result) > 100000 or result == 12:
            break
        result += 1
    global depth
    depth = result - 1
    print(depth)


def alpha_beta_search(cards, player1, player2):
    best_value = -math.inf
    best_move = None
    list1 = create_list(player1)
    list2 = create_list(player2)
    moves = get_valid_moves(cards, list1, list2)
    print(moves)
    calculate_depth(len(moves))
    for move in moves:
        move_value = min_value(copy.deepcopy(cards), copy.deepcopy(player1), copy.deepcopy(player2), move, 0,
                               -math.inf,
                               math.inf, copy.deepcopy(list1), copy.deepcopy(list2))
        if move_value > best_value:
            best_value = move_value
            best_move = move
    return best_move


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


def get_move(cards, player1, player2, companion_cards, choose_companion):
    '''
    This function gets the move of the player.

    Parameters:
        cards (list): list of Card objects
        player1 (Player): the player
        player2 (Player): the opponent
        companion_cards (dict): dictionary of companion cards
        choose_companion (bool): flag to choose a companion card

    Returns:
        move (int/list): the move of the player
    '''

    if choose_companion:
        # Choose a random companion card if available
        if companion_cards:
            selected_companion = random.choice(list(companion_cards.keys()))  # Randomly select a companion card
            move = [selected_companion]  # Add the companion card to the move list
            choices = companion_cards[selected_companion][
                'Choice']  # Get the number of choices required by the companion card

            if choices == 1:  # For cards like Jon Snow
                move.append(random.choice(get_valid_jon_sandor_jaqan(cards)))

            elif choices == 2:  # For cards like Ramsay
                valid_moves = get_valid_ramsay(cards)

                if len(valid_moves) >= 2:
                    move.extend(random.sample(valid_moves, 2))

                else:
                    move.extend(valid_moves)  # If not enough moves, just use what's available


            elif choices == 3:  # Special case for Jaqen with an additional companion card selection
                valid_moves = get_valid_jon_sandor_jaqan(cards)

                if len(valid_moves) >= 2 and len(companion_cards) > 0:
                    move.extend(random.sample(valid_moves, 2))
                    move.append(random.choice(list(companion_cards.keys())))

                else:
                    # If there aren't enough moves or companion cards, just return what's possible
                    move.extend(valid_moves)
                    move.append(random.choice(list(companion_cards.keys())) if companion_cards else None)

            return move

        else:
            # If no companion cards are left, just return an empty list to signify no action
            return []

    else:
        # Normal move, choose from valid moves
        move = alpha_beta_search(cards, player1, player2)
        return move
