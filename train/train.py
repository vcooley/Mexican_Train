"""
A game called Mexican train. Played with dominoes. Game needs to be able to:

Set up:
    *Create blank board.
    *Create a 'train' for each player and one Mexican train.
    *Create dominoes given the maximum value on a domino.
    *Determine amount of dominoes in a hand given number of players
    *Deal dominoes at random to each player until hand size is reached
    *Only allow a player to play on his train on the first move
    Know when to block a player's train from other players(but not that player)
    Find the highest double value dealt and begin play with the owner of that tile given the first turn


First turn:
      Check if last play was a double that was not 'backed up'(player MUST play on that domino then play his turn)
      Check if player has a legal move
      If player cannot move only option is draw
      Allow player to draw even if he has a legal move
      If player draws, he can only play the domino drawn if it is valid
      While player can continue train, allow player to continue train or end turn
      Add train marker to block other players from playing on player's train.
      Mark first_turn = done


Gameplay (later turns):
    Remove train marker from player's train
    Check if a double has been played and not backed up (if so player must play on that domino)
    Check if a move is available for the current player
    Draw for the player if no move is available (Check if move is available after drawing)
    If move is available allow player to place domino.
    If player places double, player must 'back it up' or draw (can play drawn domino if it matches the double)
    Check if the player won (ran out of dominoes)
    Check if player played on his own train. If so, place train marker.
    Handle an empty boneyard


AI:
    Find maximum dominoes playable on first turn.
    Always plays if possible (Maybe change to make smart draw decisions even if a move is available.)
    Steps to choose where to play:
        Always play on own train if valid move.
        Always play double if you have something to back it up.
        Check future turns and try to play something that will allow you to move in the future(implement later)
        If you can't back a double up, but someone else has one domino left, play the double anyway

GUI:
    future

"""

__author__ = 'Vince'

from copy import copy
import random


class Board(object):
    """
    Contains all methods needed to set up and store a game board. Board is represented by list of lists
    """

    def __init__(self, num_players, max_domino=12):
        self.num_players = num_players
        self.max_domino = max_domino
        self.boneyard = []
        self.domino_set = []
        self.board = []
        self.hands = []
        self.empty_hands()
        self.last_played = ((-2, -1), -1)  # Once any player moves, will be a tuple of the form ((0,0), train_number)
        self.current_player = 0
        self.make_dom_set()

    def __str__(self):
        string = '\nBoard:'
        for player, train in enumerate(self.board):
            string += "\nPlayer %d Train: " % player
            string += ", ".join(str(x) for x in train if not isinstance(x[1], str))
            if train[0][1] == 'closed':
                string += ' XX'
            else:
                string += " OO"
        string += "\n\nHands:"
        for player, hand in enumerate(self.hands):
            string += "\nPlayer %d hand: " % player
            string += ", ".join(str(x) for x in hand)
        return string

    def create_board(self):
        """
        Creates a list of lists representing each players train and one additional train that anyone may play upon.
        Each inner array represents a players train, where the first value is a tuple (player, 'closed'/'open')
        which states whether other players can play on that train. The first value for the mexican train is
        always ('mex', 'open'). Other tuple values will later be appended. The second value in a tuple always represents
        the value that may be played upon.
        """
        self.board = []
        for player in range(self.num_players):
            self.board.append([(player, 'closed')])
        self.board.append([('mex', 'open')])

    def set_board(self, board):
        """
        Creates a board for testing purposes.
        :param board:
        :return:
        """
        self.board = board

    def make_dom_set(self):
        """
        Creates a set of dominoes.
        """
        self.domino_set = []
        for side1 in range(self.max_domino + 1):
            for side2 in range(side1, self.max_domino + 1):
                self.domino_set.append((side1, side2))

    def get_hand_size(self):
        """
        Gets the appropriate size for the beginning hand.
        :return hand_size:
        """
        # Dictionary for standard double-12 set.
        hand_size = {
            2: 12,
            3: 12,
            4: 12,
            5: 11,
            6: 11,
            7: 10,
            8: 10
        }
        if self.max_domino == 12 and self.num_players <= 8:
            return hand_size[self.num_players]
        # An ok made-up approximation of a good hand size.
        else:
            return int(len(self.domino_set) / 1.5 / self.num_players)

    def empty_hands(self):
        """
        Creates a list of empty hands.
        """
        self.hands = []
        for hand in range(self.num_players):
            self.hands.append([])

    def deal(self):
        """
        Deals a beginning hand to each player.
        :return:
        """
        if self.domino_set == []:
            self.make_dom_set()
        self.empty_hands()
        self.boneyard = copy(self.domino_set)
        self.shuffle_boneyard()
        hand_size = self.get_hand_size()
        num_to_deal = self.num_players * hand_size
        player_list = range(self.num_players)
        player = 0
        for dom in range(num_to_deal):
            self.hands[player].append(self.draw())
            player += 1
            if player not in player_list:
                player = 0

    def draw(self):
        """
        Returns a random domino from the boneyard.
        :return domino:
        """
        if len(self.boneyard) > 0:
            return self.boneyard.pop()
        else:
            return None

    def shuffle_boneyard(self):
        """
        Shuffles the boneyard.
        """
        random.shuffle(self.boneyard)

    def check_double(self, domino):
        """
        Returns True if domino is a double; False otherwise.
        """
        if domino[1] == domino[0]:
            return True
        else:
            return False

    def get_first_player(self):
        """
        Finds the first player to move. This player is the player with the highest double in their hand.
        Returns the player and the domino to be played.
        """
        first_player = 0
        max_double = (0, 0)
        for player, hand in enumerate(self.hands):
            if hand == []:
                raise SetupError
            for domino in hand:
                if self.check_double(domino) and domino[0] > max_double[0]:
                    max_double = domino
                    first_player = player
        return first_player, max_double

    def next_player(self):
        """
        Sets self.current_player = to the next player in the queue
        :return:
        """
        if self.current_player + 1 in range(self.num_players):
            self.current_player += 1
        else:
            self.current_player = 0

    def check_move(self, domino, train_num, player):
        """
        Checks if a move is valid. Returns False if move invalid and returns the correct orientation for the domino
        if the move is valid.
        :param domino:
        :param train_num:
        :return:
        """
        train = self.board[train_num]
        if train[0][0] != player and train[0][1] == 'closed':
            return False
        elif domino[0] == train[-1][1]:
            return domino  # Return the domino if it's already in correct orientation
        elif domino[1] == train[-1][1]:
            return domino[1], domino[0]  # Flip domino if it creates valid move
        else:
            return False

    def new_game(self, num_players='unchanged', max_domino='unchanged'):
        """
        Creates new game with the most recent number of players and maximum domino by default.
        :param num_players:
        :param max_domino:
        :return:
        """
        if num_players != 'unchanged':
            self.num_players = num_players
        if max_domino != 'unchanged':
            self.max_domino = max_domino
            self.make_dom_set()
        self.create_board()
        self.boneyard = copy(self.domino_set)
        self.deal()
        self.first_move()

    def first_move(self):
        """
        Find the first player to move and place the highest double from that players hand on each train.
        Does not change current player because this does not count as the player's move.
        :return:
        """
        self.current_player, domino = self.get_first_player()
        for train in self.board:
            train.append(domino)
        self.hands[self.current_player].remove(domino)


class Player(object):
    """

    """

    def __init__(self, board, player_num):
        self.board = board
        self.player_num = player_num
        self.hand = self.board.hands[self.player_num]
        self.own_train_started = False

    def __str__(self):
        """
        String representation of player's hand.
        :return:
        """
        self.update_hand()
        result = "\nYour hand:\n"
        for idx, dom in enumerate(self.hand):
            result += "{}: {},  ".format(idx, dom)
        return result

    def update_hand(self):
        try:
            self.hand = self.board.hands[self.player_num]
        except IndexError:
            return "Player not in current game."

    def get_moves(self):
        """
        Gets a list of lists of valid moves indexed by train number, domino number.
        :return:
        """
        moves = []
        for player in range(self.board.num_players + 1):
            moves.append([])
        # First check for mandatory moves, such as backing up double or playing the first turn
        if self.board.check_double(self.board.last_played[0]):
            for idx, domino in enumerate(self.hand):
                if self.board.check_move(domino, self.board.last_played[1], self.player_num):
                    moves[self.board.last_played[1]].append(idx)
            return moves
        if not self.own_train_started:
            for idx, domino in enumerate(self.hand):
                if self.board.check_move(domino, self.player_num, self.player_num):
                    moves[self.player_num].append(idx)
        # Then check for valid moves on open trains or player's train.
        else:
            for train_idx, train in enumerate(self.board.board):
                for dom_idx, domino in enumerate(self.hand):
                    if self.board.check_move(domino, train_idx, self.player_num):
                        moves[train_idx].append(dom_idx)
        return moves

    def print_moves(self, moves):
        """
        Takes a list of moves and prints it for the player
        :param moves:
        :return:
        """
        move_available = False
        for train_idx, dominoes in enumerate(moves):
            if moves[train_idx] != []:
                move_available = True
                print "You may move on {} with domino(es): {}".format(train_idx, dominoes)
        if not move_available:
            print 'You have no moves available. You must draw!'

    def choose_move(self):
        """
        Asks a player for the domino and train he wishes to play on.
        :return:
        """
        moves = self.get_moves()
        while True:
            print self
            self.print_moves(moves)
            train_selection = raw_input("\nSelect a train to play on or type 'draw' to draw: ")
            if train_selection.lower() == 'draw':
                return train_selection
            else:
                try:
                    train_selection = int(train_selection)
                except ValueError:
                    "\nInvalid choice. Please enter a number for the train you which to play on."
                    continue
            if not moves[train_selection]:
                print "\nYou have no available moves for that train."
            else:
                break
        while True:
            print self
            print "Dominoes that you may play here:", moves[train_selection]
            dom_selection = raw_input("\nSelect a domino to play, type 'draw' to draw, \
or 'back' to select a different train: ")
            if dom_selection.lower() == 'draw':
                return dom_selection.lower()
            elif dom_selection.lower() == 'back':
                return dom_selection.lower()
            else:
                try:
                    dom_selection = int(dom_selection)
                except (ValueError, TypeError):
                    raw_input("\n\nPlease enter the index of the domino you wish to play.")
                    continue
            if dom_selection not in moves[train_selection]:
                print raw_input("\nThat domino is not available to move here.")
            else:
                return dom_selection, train_selection

    def play(self, domino_idx, train_num):
        """
        Places a domino at the end of a train. Closes train if train == player.
        :return:
        """
        domino = self.hand[domino_idx]
        valid_move = self.board.check_move(domino, train_num, self.player_num)
        if valid_move:
            self.board.board[train_num].append(valid_move)
            if train_num == self.player_num:
                self.board.board[train_num][0] = (self.player_num, 'closed')
            self.board.last_played = (valid_move, train_num)
            self.hand.remove(domino)
        else:
            return "Invalid move."


class AI(Player):
    pass


class Engine(object):
    """
    Runs the game using player and board objects
    """

    def __init__(self, human_players, ai_players, max_domino=12):
        self.board = Board(human_players + ai_players, max_domino)
        self.players = []
        self.player_setup(human_players, ai_players)

    def player_setup(self, human_players, ai_players):
        """
        Creates a list of player and ai objects for the engine to use.
        :param human_players:
        :param ai_players:
        :return:
        """
        player_list = []
        for human in range(human_players):
            player_list.append('human')
        for ai in range(ai_players):
            player_list.append('ai')
        while player_list:
            next_to_add = player_list.pop(random.randrange(len(player_list)))
            if next_to_add == 'ai':
                self.players.append(AI(self.board, len(self.players)))
            else:
                self.players.append(Player(self.board, len(self.players)))

    def game_over(self):
        """
        Looks at each players hand and returns the first that is empty, so long as a double
         was not the last played domino. Returns False if the game is not over
        :return:
        """
        for player, hand in enumerate(self.board.hands):
            if len(hand) != 0:
                continue
            elif not self.board.check_double(self.board.last_played[0]):
                return player
        return False

    def play_first_move(self, current_player):
        """
        Handles the first move of a player.
        :return:
        """
        pass

    def start_game(self):
        self.board.new_game()
        winner = self.game_over()
        while not winner:
            current_player = self.players[self.board.current_player]
            if not current_player.own_train_started:
                self.play_first_move(current_player)
            else:
                move = current_player.choose_move()
                if move == 'draw':
                    current_player.hand.append(self.board.draw())
                else:
                    current_player.play(*move)
            if self.board.check_double(self.board.last_played[0]):
                continue
            else:
                winner = self.game_over()
                self.board.next_player()
                current_player = self.players[self.board.current_player]

class SetupError(Exception):
    pass

def main():
    game = Engine(2, 2)
    for player in game.players:
        player.own_train_started = True
    game.start_game()

if __name__ == '__main__':
    main()