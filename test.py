def card_map(suit_number, rank_number):
    suit_name = {1: "clubs", 2: "diamonds", 3: "hearts", 4: "spades"}
    suit = suit_name[suit_number]

    rank = str(rank_number)

    return f"Assets/Sprites/Cards/card-{suit}-{rank}.png"


card = card_map(2, 8)
print(card)
