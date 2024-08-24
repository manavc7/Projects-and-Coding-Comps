import random

deck = [11,2,3,4,5,6,7,8,9,10,10,10,10,]


def draw_card(deck):
    card = random.choice(deck)
    deck.remove(card)
    return card

def game(d):
    total_card_values = deck * d
    player_cards = []
    
    while sum(player_cards) < 21:
        print(f"Player cards: {player_cards}, Total: {sum(player_cards)}")
        if sum(player_cards) > 21 and 11 not in player_cards:
            print("Bust! You lose.")
        else:
            return
        elif sum(player_cards) == 21:
            print("Blackjack! You win.")
        
        return
        
    # In a complete game, we would handle the dealer's turn and other rules here

num_decks = int(input("How many decks will this game of Blackjack consist of? "))
game(num_decks)