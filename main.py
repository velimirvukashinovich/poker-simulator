from classes import Player, Dealer

dealer = Dealer()

players = [Player() for i in range(6)]

for i in range(2):
    for player in players:
        player.add_card(dealer.deal_player_card())
        
dealer.deal_next()
dealer.deal_next()
dealer.deal_next()

# players[0].hand[0].value = '2'
# players[0].hand[1].value = '3'

# dealer.runout[0].value = '4'
# dealer.runout[1].value = '5'
# dealer.runout[2].value = 'Q'
# dealer.runout[3].value = 'K'
# dealer.runout[4].value = 'A'


# players[0].hand[0].suit = '♥'
# players[0].hand[1].suit = '♥'

# dealer.runout[0].suit = '♥'
# dealer.runout[1].suit = '♥'
# dealer.runout[2].suit = '♥'
# dealer.runout[3].suit = '♥'
# dealer.runout[4].suit = '♥'

for player in players:
    print(player.get_hand(to_print=True))
print(dealer.get_runout(to_print=True))

for player in players:
    value, best_hand = dealer.evaluate_hand(player.get_hand())
    print(value, [str(card) for card in best_hand])
    # print()