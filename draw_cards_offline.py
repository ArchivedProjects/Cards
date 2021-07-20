from typing import Generator

import random

# TODO: Determine if I should add unique ids to the cards or if I should let the game do that (for multiple decks).
# I'll probably let the game handle that when the card is drawn as there's no real reason I need to do that internally.

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
    """
        Card Drawing Function (Generates Decks For You)

        @param decks: Number Of Decks You Want (52 Cards Each)
        @param shuffle: Whether Or Not To Shuffle The Cards For You
        @param jokers: Number Of Jokers To Add To Deck (Alternates Between Black and Red)
        @return: Generator To Return Deck Of Cards With Dictionaries
    """

    # Build My Deck Of Cards
    deck: list = []
    for i in range(1, decks+1):
        for suit in card_suits:
            for card in card_values:
                # print(f"{card} {suit['name']}")
                deck.append({
                    "suit": suit['name'],
                    "value": card,
                    "code": f"{card[0]}{suit['name'][0]}"  # 10 is fine as 1 because 1 is A for Ace (for card[0])
                })

    # Add Joker Cards
    for i in range(1, jokers+1):
        joker_color = joker_colors[0] if i % 2 == 1 else joker_colors[1]

        deck.append({
            "suit": joker_color,
            "value": "Joker",
            "code": f"O{joker_color[0]}"
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
    # This'll Most Likely Crash Around 25 Minutes On 8 Gigs Of RAM
    # cards = draw_cards(decks=6000000, jokers=6000000*2, shuffle=True)

    # This Part Handles Formatting, Printing, and Retrieving The Card/Metadata From The Generator
    header: str = "{:<16} | {:<2} | {:<15} | {:<6}".format("Card", "Code", "Cards Remaining", "Percentage Drawn")

    print(header)
    print("-"*len(header))
    for card in cards:
        suit = card["suit"]
        value = card["value"]
        remaining = card["remaining"]
        starting = card["starting"]
        code = card["code"]

        percentage = 100 - ((remaining/starting)*100)

        print("{:<16} | {:<4} | {:<15} | {:<6}".format(f"{value} of {suit}", code, remaining, f"{percentage:3.2f} %"))
