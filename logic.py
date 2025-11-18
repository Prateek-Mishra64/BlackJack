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


def deal_card():
    house, value = deck.pop()
    house_num = house_map[house]
    value_num = value_map[value]

    return deck.pop()


def calculate_score(hand):
    values = [card[1] for card in hand]
    score = 0
    aces = 0
    value = {
        "A": 11,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 10,
        "Q": 10,
        "K": 10,
    }
    for v in values:
        score += value[v]
        if v == "A":
            aces += 1
        while score > 21 and aces > 0:
            score -= 10
            aces -= 1
    return score


def player_turn(player_hand):
    while True:
        action = input("Do you want to hit or stand? (h/s): ").strip().lower()
        if action == "h":
            player_hand.append(deal_card())
            score = calculate_score(player_hand)
            print("Player: ", player_hand)
            print("Player score: ", score)
            if score > 21:
                print("Player busts! Dealer wins.")
                return False
        elif action == "s":
            return True
        else:
            print("Invalid input. Please enter 'h' or 's'.")


def dealer_turn(dealer_hand, player_hand, ai):
    while True:
        dealer_score = calculate_score(dealer_hand)
        player_score = calculate_score(player_hand)

        if dealer_score >= 21:
            break

        action = ai.choose_action(dealer_hand, player_hand)
        if action == 1:
            dealer_hand.append(deal_card())
            print(f"Dealer hits → {dealer_hand}")
        else:
            print(f"Dealer stands  → {dealer_hand}")
            break

    dealer_score = calculate_score(dealer_hand)
    print(f"Dealer's final hand: {dealer_hand} | Score: {dealer_score}")
    if dealer_score > 21:
        print("Dealer busts! Player wins.")
        return False
    return True


# [----------------------------------------RUN GAME----------------------------------------------------------]
if __name__ == "__main__":
    ai = DealerAI(difficulty="hard")

    player_hand = [deal_card(), deal_card()]
    dealer_hand = [deal_card(), deal_card()]

    print("Player:", player_hand)
    print("Dealer:", dealer_hand[0], "??")

    player_result = player_turn(player_hand)
    if player_result:
        print("Dealer's Hand:", dealer_hand)
        dealer_result = dealer_turn(dealer_hand, player_hand, ai)
        if dealer_result:
            player_score = calculate_score(player_hand)
            dealer_score = calculate_score(dealer_hand)
            if player_score > dealer_score:
                print("Player wins!")
            elif player_score < dealer_score:
                print("Dealer wins!")
            else:
                print("It's a tie!")
