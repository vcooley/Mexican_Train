from nose.tools import *
from train.train import *
from copy import copy


def setup_func():
    global test_board1
    global test_board2
    global test_board3
    global test_board4
    global test_board5
    global test_hands1
    test_board1 = [[], [], [], [], []]
    test_board2 = [[(0, 'closed'), (12, 12)],
                   [(1, 'closed'), (12, 12)],
                   [(2, 'closed'), (12, 12)],
                   [(3, 'closed'), (12, 12)],
                   [('mex', 'open'), (12, 12)]
                   ]
    test_board3 = [[(0, 'closed'), (-1, -1)],
                   [(1, 'closed'), (-1, -1)],
                   [(2, 'closed'), (-1, -1)],
                   [(3, 'closed'), (-1, -1)],
                   [('mex', 'open'), (-1, -1)]
                   ]
    test_board4 = [[(0, 'closed'), (12, 12), (12, 11)],
                   [(1, 'closed'), (12, 12), (12, 2)],
                   [(2, 'closed'), (12, 12), (12, 7)],
                   [(3, 'closed'), (12, 12), (12, 5)],
                   [('mex', 'open'), (12, 12), (12, 1)]
                   ]
    test_board5 = [[(0, 'open'), (12, 12), (12, 11)],
                   [(1, 'open'), (12, 12), (12, 2)],
                   [(2, 'open'), (12, 12), (12, 7)],
                   [(3, 'open'), (12, 12), (12, 5)],
                   [('mex', 'open'), (12, 12), (12, 1)]
                   ]

    test_hands1 = [[(2, 4), (8, 11), (0, 7), (0, 8), (11, 12), (5, 12), (7, 8),
                   (8, 10), (3, 10), (1, 7), (2, 5), (3, 9)],
                   [(3, 6), (1, 11), (1, 8), (4, 7), (8, 8), (6, 9), (6, 11),
                   (9, 9), (4, 8), (9, 11), (4, 4), (2, 12)],
                   [(1, 12), (0, 0), (3, 12), (5, 7), (3, 5), (3, 3), (5, 5),
                   (7, 10), (5, 9), (2, 11), (0, 10), (1, 5)],
                   [(4, 10), (10, 10), (1, 9), (5, 6), (0, 2), (9, 12), (0, 9),
                   (7, 7), (10, 12), (3, 7), (6, 12), (2, 8)]
                   ]


def check_double_test():
    board = Board(4)
    assert board.check_double((12, 12)) == True
    assert board.check_double((12, 11)) == False


@with_setup(setup_func)
def check_move_test():
    board = Board(4)
    board.board = test_board1
    try:
        assert_equal(board.check_move((12, 11), 1, 1), False)
        assert_equal(board.check_move((11, 12), 1, 2), False)
    except IndexError:
        pass
    board.board = test_board2
    assert_equal(board.check_move((12, 11), 1, 1), (12, 11))
    assert_equal(board.check_move((11, 11), 1, 1), False)
    assert_equal(board.check_move((12, 11), 3, 1), False)
    assert_equal(board.check_move((12, 11), 4, 1), (12, 11))
    assert_equal(board.check_move((12, 11), 0, 3), False)
    board.board = test_board3
    assert_equal(board.check_move((12, 11), 1, 1), False)
    assert_equal(board.check_move((11, 11), 1, 1), False)
    assert_equal(board.check_move((12, 11), 3, 1), False)
    assert_equal(board.check_move((12, 11), 4, 1), False)
    assert_equal(board.check_move((12, 11), 1, 1), False)


@with_setup(setup_func)
def create_board_test():
    board = Board(0)
    board.create_board()
    assert_equal(board.board, [[('mex', 'open')]])
    board = Board(1)
    board.create_board()
    assert_equal(board.board, [[(0, 'closed')], [('mex', 'open')]])
    board = Board(5)
    board.create_board()
    assert_equal(board.board, [[(0, 'closed')], [(1, 'closed')], [(2, 'closed')],
                               [(3, 'closed')], [(4, 'closed')], [('mex', 'open')]])


def deal_test():
    board = Board(4)
    board.make_dom_set()
    board.boneyard = copy(board.domino_set)
    board.deal()
    assert_equal(len(board.hands[0]), len(board.hands[3]))
    assert_equal(len(board.hands[0]), 12)
    board = Board(8)
    board.make_dom_set()
    board.boneyard = copy(board.domino_set)
    board.deal()
    assert_equal(len(board.hands[0]), len(board.hands[3]))
    assert_equal(len(board.hands[0]), 10)


def draw_test():
    board = Board(4)
    board.make_dom_set()
    board.boneyard = board.domino_set
    hand_len = len(board.hands[0])
    board.hands[0].append(board.draw())
    assert_equal(hand_len, len(board.hands[0]) - 1)


def empty_hands_test():
    board = Board(4)
    assert_equal(len(board.hands[0]), 0)
    board.deal()
    board.empty_hands()
    assert_equal(len(board.hands[0]), 0)


@with_setup(setup_func)
def first_move_test():
    """
    Also tests get_first_player
    """
    board = Board(4)
    board.create_board()
    board.hands = test_hands1
    assert_equal(board.get_first_player(), (3, (10, 10)))
    starting_board = [[(0, 'closed'), (10, 10)],
                      [(1, 'closed'), (10, 10)],
                      [(2, 'closed'), (10, 10)],
                      [(3, 'closed'), (10, 10)],
                      [('mex', 'open'), (10, 10)]
                      ]
    board.first_move()
    assert_equal(board.board, starting_board)


def get_hand_size_test():
    board = Board(4)
    assert_equal(board.get_hand_size(), 12)


def make_dom_set_test():
    board = Board(4)
    board.make_dom_set()
    assert_equal(len(board.domino_set), 91)
    board = Board(4, 6)
    board.make_dom_set()
    assert_equal(len(board.domino_set), 28)
    board = Board(4, 9)
    board.make_dom_set()
    assert_equal(len(board.domino_set), 55)


def new_game_test():
    board = Board(4)
    expected_board = Board(4)
    expected_board.board = [[(0, 'closed'), (10, 10)],
                            [(1, 'closed'), (10, 10)],
                            [(2, 'closed'), (10, 10)],
                            [(3, 'closed'), (10, 10)],
                            [('mex', 'open'), (10, 10)]
                            ]
    board.board = [['Fake board for testing']]
    board.hands = [[(2, 3)], [(4, 5)], [(6, 7)], [(8, 9)]]
    board.new_game()
    assert_equal(len(board.domino_set), 91)
    assert_equal(len(board.hands[0]), 12)
    for idx, train in enumerate(board.board):
        assert_equal(train[0], expected_board.board[idx][0])
        assert_equal(len(train), len(expected_board.board[idx]))


def next_player_test():
    board = Board(5)
    board.current_player = 0
    for player in range(5):
        assert_equal(player, board.current_player)
        board.next_player()
    board.current_player = 2
    turn_order = [2, 3, 4, 0, 1, 2, 3, 4, 0, 1]
    for turn in range(10):
        assert_equal(board.current_player, turn_order[turn])
        board.next_player()


@with_setup(setup_func)
def get_moves_test():
    board = Board(4)
    board.board = test_board2
    board.hands = test_hands1
    player = Player(board, 0)
    assert_equal(player.get_moves(), [[4, 5], [], [], [], []])
    player.own_train_started = True
    assert_equal(player.get_moves(), [[4, 5], [], [], [], [4, 5]])
    board.board[1].append((12, 8))
    board.board[1][0] = (1, 'open')
    assert_equal(player.get_moves(), [[4, 5], [1, 3, 6, 7], [], [], [4, 5]])
    board.board[0].append((8, 8))
    board.last_played = ((8, 8), 0)
    assert_equal(player.get_moves(), [[1, 3, 6, 7], [], [], [], []])


@with_setup(setup_func)
def play_test():
    board = Board(4)
    board.board = test_board2
    board.hands = test_hands1
    player = Player(board, 0)
    player.play(4, 0)
    hand_expected = [(2, 4), (8, 11), (0, 7), (0, 8), (5, 12), (7, 8),
                     (8, 10), (3, 10), (1, 7), (2, 5), (3, 9)]
    board_expected = [[(0, 'closed'), (12, 12), (12, 11)],
                      [(1, 'closed'), (12, 12)],
                      [(2, 'closed'), (12, 12)],
                      [(3, 'closed'), (12, 12)],
                      [('mex', 'open'), (12, 12)]
                      ]
    # Valid domino on own closed train
    assert_equal(player.hand, hand_expected)
    assert_equal(board.board, board_expected)
    # Valid domino on own open train
    board.board[0][0] = (0, 'open')
    player.play(1, 0)
    board_expected[0] = [(0, 'closed'), (12, 12), (12, 11), (11, 8)]
    del hand_expected[1]
    assert_equal(board.board, board_expected)
    assert_equal(player.hand, hand_expected)
    # Valid domino on other closed train
    player.play(3, 1)
    assert_equal(player.hand, hand_expected)
    assert_equal(board.board, board_expected)
    # Valid domino on open mexican train
    player.play(3, 4)
    del hand_expected[3]
    board_expected[4].append((12, 5))
    assert_equal(player.hand, hand_expected)
    assert_equal(board.board, board_expected)




