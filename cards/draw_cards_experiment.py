from typing import Generator

import importlib
import random
import math

# Check For Humanize Module Before Importing
# This is so you don't have to install humanize
#   to test this demo, but it will be supported
#   in order to make reading nicer.
humanize = importlib.util.find_spec("humanize")
if humanize is not None:
    import humanize


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
    if decks > 0:
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
    for color in joker_colors:
        # This ensures that Jokers are spread across colors
        # TODO: Note, this only works with 2 colors due to `len(joker_colors)-1` and `jokers % 2`.
        # This can be modified for an arbitrary number of colors, but that adds extra complexity
        #   for a feature I currently have no intention of implementing at the moment.
        max_count: int = math.ceil(jokers / len(joker_colors))
        if joker_colors.index(color) == len(joker_colors)-1 and jokers % 2 != 0:
            max_count: int = max_count-1

        # print(f"{color}: {max_count} - Total: {jokers}")

        key = f"{special_cards[0]} {color}"
        card_tracker[key] = {
            "count": 0,
            "max_count": int(max_count),
            "metadata": {
                "suit": color,
                "value": special_cards[0],
                "code": f"O{color[0]}"
            }
        }

    # Yield Cards For Program
    total_cards: int = (decks*len(card_tracker))+(jokers-(2*decks))  # For Inclusion Of Jokers
    cards_remaining: int = total_cards

    while cards_remaining > 0:
        current_card_number: int = -1
        if shuffle:
            current_card_number = random.randint(0, len(card_tracker)-1)
        else:
            # 3+ Jokers Without Shuffling Freezes The Generator Without
            #   The Below Mentioned Hack. The formula is in the line below.
            # 0 = (55 - 1) % 54 | 3rd Joker Card Number (Aka Ace of Spade)
            current_card_number = (total_cards - cards_remaining) % len(card_tracker)  # Returns 0 - 53 In Order
            # print(current_card_number)

        # Card Metadata For Tracking Drawn Cards (And To Retrieve Card Info)
        card_meta = list(card_tracker.values())[current_card_number]

        # Keep Track Of Drawn Cards
        card_meta["count"] += 1
        if card_meta["count"] > card_meta["max_count"]:
            # This is a hack that moves the non-shuffle current card count
            #   up to allow for all Jokers to be placed in a non-shuffled deck.
            if not shuffle:
                total_cards += 52

            continue

        cards_remaining -= 1

        card = card_meta["metadata"].copy()  # The .copy() prevents from editing the original dictionary
        card["remaining"] = cards_remaining

        # This gets reset to the proper value for some reason unknown to me.
        # This comment is in reference to the Joker hack fix.
        # TODO: I'll need to investigate more to learn more about generators.
        card["starting"] = total_cards

        yield card


if __name__ == "__main__":
    # Original Showcase Example
    cards = draw_cards(decks=1, jokers=2, shuffle=True)

    # Debug Randomizer - The Randomizer Is Not Realistic Enough
    # I'll often get between 4 and 6 of the same card in a row at the end of the drawing.
    # The problem only gets worse as more decks are added.
    # cards = draw_cards(decks=50, jokers=100, shuffle=True)

    # True Experiment
    # cards = draw_cards(decks=6000000, jokers=6000000*2, shuffle=True)

    # Jokers Only
    # cards = draw_cards(decks=0, jokers=147, shuffle=False)

    # This Part Handles Formatting, Printing, and Retrieving The Card/Metadata From The Generator
    header: str = "{:<16} | {:<2} | {:<15} | {:<6}".format("Card", "Code", "Cards Remaining", "Percentage Drawn")

    print(header)
    print("-"*len(header))
    try:
        for card in cards:
            suit = card["suit"]
            value = card["value"]
            remaining = card["remaining"]
            starting = card["starting"]
            code = card["code"]

            percentage = 100 - ((remaining/starting)*100)

            remaining_formatted = humanize.intcomma(remaining) if humanize is not None else remaining
            print("{:<16} | {:<4} | {:<15} | {:<6}".format(f"{value} of {suit}", code, remaining_formatted, f"{percentage:3.2f} %"))
    except KeyboardInterrupt:
        print("Exiting...")
        exit(0)
