# To Help Aid With Improving The Randomization Of The Next Drawn Card
# As this file is for debugging and is not a demo, I just required humanize.

from draw_cards_experiment import draw_cards

import humanize
import csv
import os

working_dir: str = "working"
output_csv: str = os.path.join(working_dir, "debug_export.csv")

if __name__ == "__main__":
    # We Are Testing With 6 Million Decks and 12 Million Jokers
    decks: int = 6000000

    if not os.path.exists(working_dir):
        os.makedirs(working_dir)

    output_handle = open(output_csv, mode="w")
    output_writer = csv.writer(output_handle)

    output_writer.writerow(["suit", "value", "code", "remaining", "starting", "times_seen"])
    output_handle.flush()

    drawn_cards: dict = {}
    for card in draw_cards(decks=decks, jokers=decks*2):
        suit = card["suit"]
        value = card["value"]
        code = card["code"]
        remaining = card["remaining"]
        starting = card["starting"]

        if code in drawn_cards:
            drawn_cards[code] += 1
        else:
            drawn_cards[code] = 1

        print(f"{humanize.intcomma(starting-remaining)}/{humanize.intcomma(starting)} - {humanize.intcomma(drawn_cards[code])} - {value} of {suit}")
        output_writer.writerow([suit, value, code, remaining, starting, drawn_cards[code]])
        output_handle.flush()
