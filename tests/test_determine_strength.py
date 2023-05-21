import pytest
import sys

sys.path.insert(1, '../Poker')
from Deck import Combination, Card

#PYTHONPATH=src python3.10 -m pytest --cov src --cov-report=term-missing tests
import pytest
import sys
sys.path.insert(1, '../Poker')
from Deck import Combination, Card

#PYTHONPATH=src python3.10 -m pytest --cov src --cov-report=term-missing tests

def test_determine_strength_high_card():
    board = [Card(11, 0), Card(14, 2), Card(9, 2), Card(12, 3), Card(5, 1)]
    card_values = [11, 10, 9, 12, 5]
    for card in board:
        hand = []
        for card_value_1 in range(2, 15):
            if card_value_1 not in card_values:
                hand.append(Card(card_value_1, 0))
                for card_value_2 in range(2, 15):
                    if card_value_2 not in card_values and card_value_1 != card_value_2:
                        hand.append(Card(card_value_2, 1))
                        break
                break
        comb = Combination(hand + board)
        comb.determine_strength()
        assert "high_card" == comb.name_of_highest_combination


def test_determine_strength_pair():
    board = [Card(11, 0), Card(10, 2), Card(9, 2), Card(12, 3), Card(5, 1)]
    for card in board:
        hand = []
        for i in range(4):
            if i != card.suit:
                hand.append(Card(card.value, i))
                hand.append(Card(3, 3))
                break
        comb = Combination(hand + board)
        comb.determine_strength()
        assert "pair" == comb.name_of_highest_combination


def test_determine_strength_two_pairs():
    board_with_pair = [Card(11, 0), Card(11, 2), Card(9, 2), Card(12, 3), Card(5, 1)]
    pair_value = 11
    for card in board_with_pair:
        for other in board_with_pair:
            if card.value != other.value or card == other:
                continue
            hand = []
            for i in range(2, 15):
                flag = 0
                for check in board_with_pair:
                    if check.value == i:
                        flag = 1
                        break
                if flag == 1:
                    continue
                hand = [Card(i, 0), Card(i, 1)]
            comb = Combination(hand + board_with_pair)
            comb.determine_strength()
            assert "two_pairs" == comb.name_of_highest_combination


def test_determine_strength_three_of_a_kind():
    board = [Card(11, 0), Card(10, 2), Card(9, 2), Card(12, 3), Card(5, 1)]
    for card in board:
        hand = []
        for suit1 in range(4):
            if suit1 != card.suit:
                hand.append(Card(card.value, suit1))
                for suit2 in range(suit1, 4):
                    if suit1 != suit2 and suit2 != card.suit:
                        hand.append(Card(card.value, suit2))
                        break
                break
        comb = Combination(hand + board)
        comb.determine_strength()
        assert "three_of_a_kind" == comb.name_of_highest_combination


def test_determine_strength_straight():
    for suit in range(4):
        board = [Card(11, suit), Card(10, (suit + 1) % 4), Card(9, suit), Card(2, (suit - 1) % 4), Card(3, (suit - 1) % 4)]
        for new_suit in range(4):
            hand = [Card(13, new_suit), Card(12, new_suit)]
            comb = Combination(hand + board)
            comb.determine_strength()
            assert "straight" == comb.name_of_highest_combination
            hand = [Card(12, new_suit), Card(8, new_suit)]
            comb = Combination(hand + board)
            comb.determine_strength()
            assert "straight" == comb.name_of_highest_combination
            hand = [Card(8, new_suit), Card(7, new_suit)]
            comb = Combination(hand + board)
            comb.determine_strength()
            assert "straight" == comb.name_of_highest_combination


def test_determine_strength_flush():
    for suit in range(4):
        board = [Card(11, suit), Card(10, suit), Card(6, suit), Card(2, (suit + 1) % 4), Card(3, (suit + 1) % 4)]
        for value1 in range(2, 15):
            for value2 in range(value1 + 1, 15):
                card1 = Card(value1, suit)
                card2 = Card(value2, suit)
                if card1 not in board and card2 not in board:
                    hand = [card1, card2]
                    comb = Combination(hand + board)
                    comb.determine_strength()
                    assert "flush" == comb.name_of_highest_combination


def test_determine_strength_full_house():
    board = [Card(10, 0), Card(10, 1), Card(9, 0), Card(2, 2), Card(3, 3)]
    board = sorted(board)
    for i in range(len(board)):
        for j in range(i + 1, len(board)):
            board_card1 = board[i]
            board_card2 = board[j]
            if board_card1.value != board_card2.value:
                continue
            for k in range(len(board)):
                if k == i or k == j:
                    continue
                board_card3 = board[k]
                for suit in range(4):
                    if suit == board_card1.suit or suit == board_card2.suit:
                        continue
                    hand = [Card(board_card1.value, suit % 4),
                            Card(board_card3.value, board_card3.suit % 4)]
                    comb = Combination(hand + board)
                    comb.determine_strength()
                    assert "full_house" == comb.name_of_highest_combination


def test_determine_strength_four_of_a_kind():
    board_with_pair = [Card(11, 0), Card(11, 2), Card(9, 2), Card(12, 3), Card(5, 1)]
    for card in board_with_pair:
        for other in board_with_pair:
            if card.value != other.value or card == other:
                continue
            hand = []
            for i in range(4):
                if i != card.suit and i != other.suit:
                    hand.append(Card(card.value, i))
                    for j in range(4):
                        if i != j and j != card.suit and j != other.suit:
                            hand.append(Card(card.value, j))
                            break
                    break
            comb = Combination(hand + board_with_pair)
            comb.determine_strength()
            assert "four_of_a_kind" == comb.name_of_highest_combination


def test_determine_strength_straight_flush():
    for suit in range(4):
        board = [Card(11, suit), Card(10, suit), Card(9, suit), Card(2, suit), Card(3, 1)]
        hand = [Card(13, suit), Card(12, suit)]
        comb = Combination(hand + board)
        comb.determine_strength()
        assert "straight_flush" == comb.name_of_highest_combination
        hand = [Card(12, suit), Card(8, suit)]
        comb = Combination(hand + board)
        comb.determine_strength()
        assert "straight_flush" == comb.name_of_highest_combination
        hand = [Card(8, suit), Card(7, suit)]
        comb = Combination(hand + board)
        comb.determine_strength()
        assert "straight_flush" == comb.name_of_highest_combination


def test_determine_strength_royal_flush():
    for suit in range(4):
        board = [Card(14, suit), Card(13, suit), Card(12, suit), Card(11, suit), Card(5, 1)]
        hand = [Card(10, suit), Card(10, (suit + 1) % 4)]
        comb = Combination(hand + board)
        comb.determine_strength()
        assert "royal_flush" == comb.name_of_highest_combination
