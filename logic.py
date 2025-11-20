import pickle
import random as rnd


# [----------------------------------------IMPORTING Q TABLE FOR DEALER AI----------------------------------------------------------]
class DealerAI:
    def __init__(self, difficulty="medium"):
        self.difficulty = difficulty
        self.Q = None
        if difficulty == "hard":
            try:
                with open("dealer_brain_real.pkl", "rb") as f:
                    self.Q = pickle.load(f)
            except FileNotFoundError:
                print("⚠️ Q-table not found! Run train_dealer_ai.py first.")

        self.epsilon = {"easy": 0.8, "medium": 0.3, "hard": 0.05}[difficulty]

    def get_state(self, dealer_score, player_score):
        return (dealer_score, player_score)

    def get_q(self, state):
        if self.Q and state in self.Q:
            return self.Q[state]
        return [0.0, 0.0]

    def choose_action(self, dealer_hand, player_hand):
        dealer_score = calculate_score(dealer_hand)
        player_score = calculate_score(player_hand)
        state = self.get_state(dealer_score, player_score)

        if rnd.random() < self.epsilon:
            return rnd.choice([0, 1])
        q_values = self.get_q(state)
        return q_values.index(max(q_values))


# [----------------------------------------BLACKJACK GAME LOGIC----------------------------------------------------------]
houses = ["♣", "♦", "♥", "♠"]
values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
deck = [(house, value) for house in houses for value in values]
rnd.shuffle(deck)

house_map = {"♣": 1, "♦": 2, "♥": 3, "♠": 4}
value_map = {
    "A": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
}


def reset_deck():
    global deck
    deck = [(house, value) for house in houses for value in values]
    rnd.shuffle(deck)


def deal_card():
    global deck
    if len(deck) == 0:
        reset_deck()

    house, value = deck.pop()
    house, value = deck.pop()
    house_num = house_map[house]
    value_num = value_map[value]

    return house_num, value_num


def calculate_score(hand):
    total = 0
    aces = 0

    for _, value in hand:
        if value == 1:  # Ace
            total += 11
            aces += 1
        elif 2 <= value <= 10:  # Number cards
            total += value
        else:  # Face cards 11=J, 12=Q, 13=K
            total += 10

    # Fix Aces if score is too high
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1

    return total
