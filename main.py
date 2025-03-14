from classes import Player, Dealer

dealer = Dealer()

players = [Player() for i in range(6)]

for i in range(2):
    for player in players:
        player.add_card(dealer.deal_player_card())
        
dealer.deal_next()
dealer.deal_next()
dealer.deal_next()

for player in players:
    print(player.get_hand(to_print=True))
print(dealer.get_runout(to_print=True))

max_rank = -1
tied_players = []
for player in players:
    value, best_hand = dealer.evaluate_hand(player.get_hand())
    player.set_best_hand(value, best_hand)
    print(value, [str(card) for card in best_hand])
    if value > max_rank:
        max_rank = value
        tied_players = [player]
    elif value == max_rank:
        tied_players.append(player)
        
if len(tied_players) == 1:
    print("We have a winner!")
    print(tied_players[0].get_hand_value(), [str(card) for card in tied_players[0].get_best_hand()])
else:
    winning_players = dealer.break_tie(tied_players)
    if len(winning_players) == 1:
        print("We have a winner!")
        print(winning_players[0].get_hand_value(), [str(card) for card in winning_players[0].get_best_hand()])
    elif len(winning_players) > 1:
        print("We have multiple winners!")
        for winning_player in winning_players:
            print(winning_player.get_hand_value(), [str(card) for card in winning_player.get_best_hand()])
    else:
        print("other")
