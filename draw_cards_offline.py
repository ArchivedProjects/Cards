from typing import Generator

import random

# This isn't a "true" generator as it first has to build the deck first.
# What this means is, if you want 6 million decks of cards and 12 million jokers,
# the program will take a while and potentially crash depending on RAM

# I'll be rewriting this generator to have 54 cards in a dictionary and
#  apply a counter to each card in order to produce decks on the fly
#  without using much RAM at all.


# Interestingly Enough, The First Letters Of Each Non-Number Word Is Unique (Except For Joker)
# A, J, Q, K, S, H, C, D
card_values: list = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
card_suits: list = [{"name": "Spade", "color": "Black"},
                    {"name": "Heart", "color": "Red"},
                    {"name": "Club", "color": "Black"},
                    {"name": "Diamond", "color": "Red"}]

# I'm not sure why I put Joker in "Special Cards" when it's the only special card
special_cards: list = ["Joker"]

# It's "impossible" to find an order for Jokers since they aren't standard
# So, I just decided to alternate suits from the standard cards.
# What I mean is, Diamonds are last and as they are red, I start with a black Joker
joker_colors: list = ["Black", "Red"]


def draw_cards(decks: int = 1, shuffle: bool = True, jokers: int = 0) -> Generator:

    # Build My Deck Of Cards
    deck: list = []
    for i in range(1, decks+1):
        for suit in card_suits:
            for card in card_values:
                # print(f"{card} {suit['name']}")
                deck.append({
                    "suit": suit['name'],
                    "value": card
                })

    # Add Joker Cards
    for i in range(1, jokers+1):
        joker_color = joker_colors[0] if i % 2 == 0 else joker_colors[1]

        deck.append({
            "suit": joker_color,
            "value": "Joker"
        })

    # Shuffle Cards
    if shuffle:
        random.shuffle(deck)

    # Yield Cards For Program
    total_cards = len(deck)
    cards_remaining = total_cards
    for card in deck:
        cards_remaining -= 1
        card["remaining"] = cards_remaining
        card["starting"] = total_cards

        yield card


if __name__ == "__main__":
    cards = draw_cards(decks=1, jokers=2, shuffle=True)

    # Demo For Why This Generator Needs Improvement
    # cards = draw_cards(decks=6000000, jokers=6000000*2, shuffle=True)

    for card in cards:
        suit = card["suit"]
        value = card["value"]
        remaining = card["remaining"]
        starting = card["starting"]

        percentage = 100 - ((remaining/starting)*100)

        print(f"{value} of {suit} - Remaining: {remaining} - Percentage Drawn: {percentage}")
