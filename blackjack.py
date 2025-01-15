import random
import time
import carte_jeu
from carte_jeu import Deck, Card, Hand, hit, hit_or_stand, show_some, show_all, player_busts, player_wins, dealer_busts, dealer_wins, push

# GAMEPLAY!

while True:
    print("\n----------------------------------------------------------------")
    print("                ♠♣♥♦ WELCOME TO BLACKJACK! ♠♣♥♦")
    print("                          Lets Play!")
    print("----------------------------------------------------------------")
    print(
        "Game Rules:  Get as close to 21 as you can without going over!\n\
        Dealer hits until he/she reaches 17.\n\
        Aces count as 1 or 11."
    )

    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Show the cards:
    show_some(player_hand, dealer_hand)

        # Prompt for Player to Hit or Stand
    hit_or_stand(deck, player_hand)
    show_some(player_hand, dealer_hand)

    if player_hand.value > 21:
        player_busts(player_hand, dealer_hand)
        break

    # If Player hasn't busted, play Dealer's hand
    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        # Show all cards
        time.sleep(1)
        print("\n----------------------------------------------------------------")
        print("                     ★ Final Results ★")
        print("----------------------------------------------------------------")

        show_all(player_hand, dealer_hand)

        # Test different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand)

        else:
            push(player_hand, dealer_hand)

    # Ask to play again
    new_game = input("\nPlay another hand? [Y/N] ")
    while new_game.lower() not in ["y", "n"]:
        new_game = input("Invalid Input. Please enter 'y' or 'n' ")
    if new_game[0].lower() == "y":
        playing = True
        continue
    else:
        print("\n------------------------Thanks for playing!---------------------\n")
        break