from typing import Generator

import requests
import json


def draw_cards() -> Generator:
    new_deck_url: str = "https://www.deckofcardsapi.com/api/deck/new/shuffle/"
    draw_card_base_url: str = "https://www.deckofcardsapi.com/api/deck/{deck_id}/draw/"

    headers: dict = {
        "User-Agent": "Alexis' Python Generator Test"
    }

    deck_results = json.loads(requests.get(url=new_deck_url, headers=headers).text)
    deck_id: str = deck_results["deck_id"]

    cards_remaining: int = deck_results["remaining"]
    while cards_remaining > 0:
        response = requests.get(url=draw_card_base_url.replace("{deck_id}", deck_id), headers=headers)

        if response.status_code == 200:
            results = json.loads(response.text)

            cards_remaining: int = results["remaining"]
            yield results["cards"][0], cards_remaining


if __name__ == "__main__":
    for card, remaining in draw_cards():
        if remaining == 1:
            word = "card"
        else:
            word = "cards"

        print(f"{card['value'].capitalize()} of {card['suit'].capitalize()} - {remaining} {word} remaining")
