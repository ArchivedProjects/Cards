from typing import Generator

import humanize
import random
import math


# TODO: Note, this is still very broken. Jokers break everything!!!


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

    # This should contain 54 Card Keys Max When It's Finished (Including The Jokers)
    card_tracker: dict = {}
    for suit in card_suits:
        for card in card_values:
            key = f"{card} {suit['name']}"
            card_tracker[key] = {
                "count": 0,
                "max_count": decks,
                "metadata": {
                    "suit": suit['name'],
                    "value": card,
                    "code": f"{card[0]}{suit['name'][0]}"  # 10 is fine as 1 because 1 is A for Ace (for card[0])
                }
            }

    # Add Joker Cards (2 Jokers Currently)
    # for color in joker_colors:
    #     key = f"{special_cards[0]} {color}"
    #     card_tracker[key] = {
    #         "count": 0,
    #         "max_count": math.ceil(jokers/len(joker_colors)),  # TODO: This may need some work for the latter card
    #         "metadata": {
    #             "suit": color,
    #             "value": special_cards[0],
    #             "code": f"O{suit['name'][0]}"
    #         }
    #     }

    # Yield Cards For Program
    # total_cards: int = (decks*len(card_tracker))+(jokers-(2*decks))  # For Inclusion Of Jokers
    total_cards: int = (decks*len(card_tracker))
    cards_remaining: int = total_cards
    # print(f"Total Cards: {total_cards} - Cards Remaining: {cards_remaining}")

    while cards_remaining > 0:
        current_card_number: int = -1
        if shuffle:
            current_card_number = random.randint(0, len(card_tracker)-1)
        else:
            current_card_number = (total_cards - cards_remaining) % len(card_tracker)  # Returns 0 - 53 In Order
            # print(current_card_number)

        # TODO: Figure out if I can toss this in favor of using the max_count system
        # if jokers == 0 and current_card_number >= 52:
        #     continue
        # elif jokers == 1 and current_card_number == 53:
        #     continue

        card_meta = list(card_tracker.values())[current_card_number]
        # print(card_meta)

        # Keep Track Of Drawn Cards
        card_meta["count"] += 1
        if card_meta["count"] > card_meta["max_count"]:
            continue

        cards_remaining -= 1

        card = card_meta["metadata"].copy()  # The .copy() prevents from editing the original dictionary
        card["remaining"] = cards_remaining
        card["starting"] = total_cards

        yield card


if __name__ == "__main__":
    # Original Showcase Example
    # cards = draw_cards(decks=1, jokers=2, shuffle=True)

    # Debug Showcase Example
    # cards = draw_cards(decks=1, jokers=3, shuffle=False)

    # True Experiment
    # cards = draw_cards(decks=6000000, jokers=6000000*2, shuffle=False)

    # Debug True Experiment
    cards = draw_cards(decks=6000000, jokers=0, shuffle=True)

    # This Part Handles Formatting, Printing, and Retrieving The Card/Metadata From The Generator
    header: str = "{:<16} | {:<15} | {:<6}".format("Card", "Cards Remaining", "Percentage Drawn")

    print(header)
    print("-"*len(header))
    for card in cards:
        suit = card["suit"]
        value = card["value"]
        remaining = card["remaining"]
        starting = card["starting"]

        percentage = 100 - ((remaining/starting)*100)

        print("{:<16} | {:<15} | {:<6}".format(f"{value} of {suit}", humanize.intcomma(remaining), f"{percentage:3.2f} %"))
