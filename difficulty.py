import pickle
import random as rnd

# -----------------------------
# Deck and Score Functions (Your Game Logic)
# -----------------------------
houses = ["♠", "♥", "♦", "♣"]
values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


def create_deck():
    deck = [(h, v) for h in houses for v in values]
    rnd.shuffle(deck)
    return deck


def deal_card(deck):
    return deck.pop()


def calculate_score(hand):
    values_only = [card[1] for card in hand]
    score = 0
    aces = 0
    value_map = {
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
    for v in values_only:
        score += value_map[v]
        if v == "A":
            aces += 1
        while score > 21 and aces > 0:
            score -= 10
            aces -= 1
    return score


def is_soft(hand):
    """Return True if hand is soft (contains ace counted as 11)"""
    total = 0
    aces = 0
    for card in hand:
        val = card[1]
        if val in ["J", "Q", "K", "10"]:
            total += 10
        elif val == "A":
            total += 11
            aces += 1
        else:
            total += int(val)
    return aces > 0 and total <= 21


# -----------------------------
# Q-Learning Setup
# -----------------------------
actions = [0, 1]  # 0 = stand, 1 = hit
Q = {}  # Q-table

alpha = 0.1
gamma = 0.9
epsilon = 0.1  # random exploration


# -----------------------------
# State Helper
# -----------------------------
def get_state(dealer_hand, player_card):
    dealer_total = calculate_score(dealer_hand)
    soft = 1 if is_soft(dealer_hand) else 0
    # Convert face cards to numeric
    face_map = {"J": 10, "Q": 10, "K": 10, "A": 1}
    try:
        player_val = int(player_card[1])
    except:
        player_val = face_map[player_card[1]]
    return (dealer_total, soft, player_val)


def get_q(state):
    if state not in Q:
        Q[state] = [0.0, 0.0]
    return Q[state]


def choose_action(state):
    if rnd.random() < epsilon:
        return rnd.choice(actions)
    q_values = get_q(state)
    return q_values.index(max(q_values))


# -----------------------------
# Simulate One Dealer Episode
# -----------------------------
def simulate_episode():
    deck = create_deck()
    dealer_hand = [deal_card(deck), deal_card(deck)]
    player_hand = [deal_card(deck), deal_card(deck)]
    player_card = player_hand[0]

    state = get_state(dealer_hand, player_card)

    while True:
        action = choose_action(state)
        if action == 1:  # hit
            dealer_hand.append(deal_card(deck))
            new_state = get_state(dealer_hand, player_card)
            dealer_score = calculate_score(dealer_hand)
            if dealer_score > 21:  # dealer bust
                reward = -1
                done = True
            else:
                reward = 0
                done = False
        else:  # stand
            dealer_score = calculate_score(dealer_hand)
            player_score = calculate_score(player_hand)
            if dealer_score > 21:
                reward = -1
            elif dealer_score > player_score:
                reward = 1
            elif dealer_score < player_score:
                reward = -1
            else:
                reward = 0
            new_state = None
            done = True

        # Q-learning update
        old_q = get_q(state)[action]
        if done:
            Q[state][action] = old_q + alpha * (reward - old_q)
        else:
            next_max = max(get_q(new_state))
            Q[state][action] = old_q + alpha * (reward + gamma * next_max - old_q)

        state = new_state
        if done:
            break


# -----------------------------
# Train Dealer AI
# -----------------------------
print("Training dealer AI on full game rules...")

for episode in range(100000):
    simulate_episode()
    if episode % 10000 == 0:
        print(f"Episode {episode}")

# -----------------------------
# Save Q-table
# -----------------------------
with open("dealer_brain_real.pkl", "wb") as f:
    pickle.dump(Q, f)

print("Training complete! Q-table saved as dealer_brain_real.pkl ✅")
