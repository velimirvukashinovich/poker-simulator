from classes import Player, Dealer, Game

dealer = Dealer()

players = [Player(i+1) for i in range(8)]

for i in range(2):
    for player in players:
        player.add_card(dealer.deal_player_card())

engine = Game(players, dealer)

engine.start_game()
        
# dealer.deal_next()
# dealer.deal_next()
# dealer.deal_next()

# players[0].hand[0].value = "A"
# players[0].hand[1].value = "2"
# players[1].hand[0].value = "7"
# players[1].hand[1].value = "6"

# players[0].hand[0].suit = "♣"
# players[0].hand[1].suit = "♣"
# players[1].hand[0].suit = "♣"
# players[1].hand[1].suit = "♣"

# dealer.runout[0].value = "3"
# dealer.runout[1].value = "Q"
# dealer.runout[2].value = "5"
# dealer.runout[3].value = "K"
# dealer.runout[4].value = "T"

# dealer.runout[0].suit = "♣"
# dealer.runout[1].suit = "♣"
# dealer.runout[2].suit = "♣"
# dealer.runout[3].suit = "♣"
# dealer.runout[4].suit = "♣"


# for player in players:
#     print(player.get_hand(to_print=True))
# print(dealer.get_runout(to_print=True))

# max_rank = -1
# tied_players = []
# for player in players:
#     value, best_hand = dealer.evaluate_hand(player.get_hand())
#     player.set_best_hand(value, best_hand)
#     print(value, [str(card) for card in best_hand])
#     if value > max_rank:
#         max_rank = value
#         tied_players = [player]
#     elif value == max_rank:
#         tied_players.append(player)
        
# if len(tied_players) == 1:
#     print("We have a winner!")
#     print(f"Player {tied_players[0].get_id()}, {dealer.name_hand(tied_players[0].get_hand_value())}, {[str(card) for card in tied_players[0].get_best_hand()]}")
# else:
#     winning_players = dealer.break_tie(tied_players)
#     if len(winning_players) == 1:
#         print("We have a winner!")
#         print(f"Player {winning_players[0].get_id()}, {dealer.name_hand(winning_players[0].get_hand_value())}, {[str(card) for card in winning_players[0].get_best_hand()]}")
#     elif len(winning_players) > 1:
#         print("We have multiple winners!")
#         for winning_player in winning_players:
#             print(f" Player {winning_players[0].get_id()}, {dealer.name_hand(winning_player.get_hand_value())}, {[str(card) for card in winning_player.get_best_hand()]}")
#     else:
#         print("other")
