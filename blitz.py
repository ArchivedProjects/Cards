from cards import draw_cards

players: list = []
discard_pile: list = []

# This'll throw StopIteration on 18 Players Because Of Running Out Of Cards With 1 Deck
minimum_number_of_players: int = 2
maximum_number_of_players: int = 12

# Blitz Rules
# Video Form: https://www.youtube.com/watch?v=c2V6U3MbbaY
# Text Form: https://playingcarddecks.com/blogs/how-to-play/thirty-one-game-rules
# Normally, the player with the lowest card is the dealer, but the computer does it here.
# The same applies to the player left of the dealer, we just start with player 0.
# For Simplicity Sake, I'm Allowing All Face Cards To Count, Instead Of Just 2+ Of The Same Face
# Not much is mentioned about exceeding 31, so I'm taking from the Banking 31 game and making the player lose.
# See https://www.pagat.com/banking/31.html about the Greek Banking Game, Greek 31.
card_values: list = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
card_scores: list = [11,     2,   3,   4,   5,   6,   7,   8,   9,   10,   10,     10,      10]
desired_score: int = 31


def create_player_decks(number_of_players: int, deck: draw_cards):
    number_of_starting_cards: int = 3
    players: list = []

    for x in range(0, number_of_starting_cards):
        for i in range(0, number_of_players):
            card = next(deck)
            card_score: int = card_scores[card_values.index(card['value'])]

            if len(players)-1 < i:
                players.append({
                    "has_knocked": False,
                    "score": card_score,
                    "cards": [card]
                })
            else:
                players[i]["cards"].append(card)
                players[i]["score"] += card_score

    return players


if __name__ == "__main__":
    print("This game is not fully implemented at the moment!!!")

    number_of_players: int = 2
    deck = draw_cards(decks=1, jokers=0, shuffle=True)

    players = create_player_decks(number_of_players=number_of_players, deck=deck)

    # As Per Rules, The Top Card Is Placed Into The Discard Pile After The Cards Are Dealt
    discard_pile.append(next(deck))

    game_running: bool = True
    while game_running:
        for player in players:
            for card in player["cards"]:
                print(f"Player {players.index(player)} - {card['value']} of {card['suit']} - {player['score']}")

        # For Debugging
        game_running: bool = False

    for card in discard_pile:
        print(f"Discard Pile - {card['value']} of {card['suit']}")
