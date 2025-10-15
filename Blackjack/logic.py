import random as rnd

if __name__="__main__":

houses = ["♠", "♥", "♦", "♣"]
values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
deck = [(house, value) for house in houses for value in values]
rnd.shuffle(deck)


def deal_card():
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
                print("Player's score went over 21! Player loses.")
                return False
        elif action == "s":
            return True
        else:
            print("Invalid input. Please enter 'h' or 's'.")


def dealer_turn(dealer_hand):
    score = calculate_score(dealer_hand)
    while calculate_score(dealer_hand) < 17:
        dealer_hand.append(deal_card())
        score = calculate_score(dealer_hand)
    print("Dealer's final hand: ", dealer_hand)
    print("Dealer's final score: ", score)
    if score > 21:
        print("Dealer's score went over 21! Dealer loses.")
        return False
    return True


player_hand = [deal_card(), deal_card()]
dealer_hand = [deal_card(), deal_card()]

print("Player:", player_hand)
print("Dealer:", dealer_hand[0], "??")

player_result = player_turn(player_hand)
if player_result:
    print("Dealer's Hand:", dealer_hand)
    dealer_result = dealer_turn(dealer_hand)
    if dealer_result:
        player_score = calculate_score(player_hand)
        dealer_score = calculate_score(dealer_hand)
        if player_score > dealer_score:
            print("Player wins!")
        elif player_score < dealer_score:
            print("Dealer wins!")
        else:
            print("It's a tie!")
