import random as rnd

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    
    def __str__(self):
        return f"{self.value} {self.suit}"
    
    def get_value(self):
        return self.value
    
    def get_suit(self):
        return self.suit

class Deck:
    def __init__(self):
        self.suits = ["♣", "♦", "♥", "♠"]
        self.values = [str(i) for i in range(2, 10)]
        self.values.extend(["T", "J", "Q", "K", "A"])
        self.cards = []
        self.generate_deck()
        
    def shuffle_deck(self):
        if len(self.cards) > 1:
            rnd.shuffle(self.cards)
        
    def generate_deck(self):
        for value in self.values:
            for suit in self.suits:
                card = Card(value, suit)
                self.cards.append(card)
        self.shuffle_deck()
                
    def get_cards(self):
        return self.cards
    
    def deal_card(self, amount):
        cards_dealt = []
        for i in range(amount):
            if len(self.cards) > 0:
                dealt_card = self.cards.pop()
                cards_dealt.append(dealt_card)
            else:
                raise ValueError("No more cards in deck.")
        return cards_dealt
            
class Player():
    def __init__(self, id):
        self.id = id
        self.hand = []
        self.hand_rank = []
        self.best_hand = []
        self.stack = 1000
        
    def get_id(self):
        return self.id
        
    def add_card(self, cards):
        if len(cards) == 1:
            if len(self.hand) == 2:
                raise ValueError("Too many cards in hand!")
            else:
                self.hand.append(cards[0])
        else:
            raise ValueError("You can only deal 1 card to a player at a time.")
        
    def get_hand(self, to_print=False):
        if to_print:
            return f"Your hand: {[str(card) for card in self.hand]}"
        else:
            return self.hand
        
    def get_stack(self, to_print=False):
        if to_print:
            return f"${self.stack}"
        else:
            return self.stack
        
    def bet(self, amount):
        if amount <= self.stack:
            self.stack -= amount
        else:
            raise ValueError("You can't bet more than your stack!")
        
    def win(self, amount):
        self.stack += amount
    
    def set_best_hand(self, value, best_hand):
        self.hand_rank = value
        self.best_hand = best_hand
        
    def get_best_hand(self, to_print=False):
        if to_print:
            return f"Your best hand: {[str(card) for card in self.best_hand]}"
        else:
            return self.best_hand
        
    def get_hand_value(self):
        return self.hand_rank

class Dealer():
    def __init__(self):
        self.valuation = {
            '2' : 2,
            '3' : 3,
            '4' : 4,
            '5' : 5,
            '6' : 6,
            '7' : 7,
            '8' : 8,
            '9' : 9,
            'T' : 10,
            'J' : 11,
            'Q' : 12,
            'K' : 13,
            'A' : 14
        }

        self.hand_name = {
            0 : "High Card",
            1 : "One Pair",
            2 : "Two Pair",
            3 : "Three of a Kind",
            4 : "Straight",
            5 : "Flush",
            6 : "Full House",
            7 : "Four of a Kind",
            8 : "Straight Flush",
            9 : "Royal Flush"
        }
        self.runout = []
        self.burn_pile = []
        self.pot = 0
        self.deck = Deck()
        self.bet = 0

    def name_hand(self, value):
        return self.hand_name[value]
    
    def get_bet(self, to_print=False):
        if to_print:
            return f"Current bet is: ${self.bet}."
        else:
            return self.bet
        
    def get_pot(self, to_print):
        if to_print:
            return f"The pot is: ${self.pot}."
        else:
            return self.pot
        
    def set_bet(self, amount):
        self.pot += amount
        self.bet = amount
        
    def deal_next(self):
        if len(self.runout) == 5:
            raise ValueError("Board full, can't deal any more cards!")
        self.burn_pile.append(self.deck.deal_card(1)[0])
        if len(self.runout) == 0:
            for card in self.deck.deal_card(3):
                self.runout.append(card)
        else:
            self.runout.append(self.deck.deal_card(1)[0])
            
    def get_runout(self, to_print=False):
        if to_print:
            return f"Runout: {[str(card) for card in self.runout]}"
        else:
            return self.runout
        
    def deal_player_card(self):
        return self.deck.deal_card(1)
    
    def get_highest_cards(self, hand, n, cards_present=[]):
        return [card for card in hand if card not in cards_present][:n]
    
    def find_first_difference_in_hands(self, *hands):
        for i, values in enumerate(zip(*hands)):
            if len(set([card.value for card in values])) > 1:
                return i
        return -1
    
    def evaluate_hand(self, hand):
        hand.extend(self.runout)
        hand = sorted(hand, key=lambda card: self.valuation[card.get_value()], reverse=True)
        values = [self.valuation[card.get_value()] for card in hand]
        suits = [card.get_suit() for card in hand]
        pairs = []
        pairs_present = False
        four_of_a_kind = False
        three_of_a_kind = False
        three_value = four_value = None
        
        for v in set(values):
            if values.count(v) == 4:
                four_value = v
                four_of_a_kind = True
            if values.count(v) == 3:
                three_value = v
                three_of_a_kind = True
            if values.count(v) == 2:
                pairs_present = True
                pairs.append(v)

            
        flush = False
        straight = False
        straight_cards = []
        high_card = None
        values = sorted(set(values), reverse=True)
        for i in range(len(values) - 4):
            if values[i:i+5] == list(range(values[i], values[i] - 5, -1)):  # Found a straight
                straight = True
                high_card = values[i]  # The highest card in the straight
                break
            
        if straight:
            straight_values = set(range(high_card, high_card - 5, -1))  
            straight_cards = []
            seen_values = set()

            # Collect only the first occurrence of each value (to ensure 5 cards)
            for card in hand:
                if self.valuation[card.get_value()] in straight_values and card.get_value() not in seen_values:
                    straight_cards.append(card)
                    seen_values.add(card.get_value())
                    if len(straight_cards) == 5:  # Stop once we have exactly 5 cards
                        break
        elif {14, 5, 4, 3, 2}.issubset(values):
            straight = True
            straight_values = {5, 4, 3, 2, 14}
            straight_cards = [card for card in hand if self.valuation[card.get_value()] in straight_values]
            straight_cards.append(straight_cards.pop(0))
    
        flush_suit = None
        flush_cards = []
        for v in set(suits):
            if suits.count(v) >= 5:
                flush = True
                flush_suit = v
                break
            
        if flush:
            all_flush_cards = [card for card in hand if card.get_suit() == flush_suit]
            all_flush_cards.sort(key=lambda card: self.valuation[card.get_value()], reverse=True)
            flush_cards = all_flush_cards[:5]

        best_hand = []
        if straight and flush and high_card == 14:
            return 9, straight_cards
        if straight and flush:
            # TODO: add logic for ditinguishing straight flush from 7 card hand that has only straight and only flush.
            return 8, straight_cards
        if four_of_a_kind:
            best_hand = [card for card in hand if self.valuation[card.get_value()] == four_value]
            best_hand.extend(self.get_highest_cards(hand, 1, best_hand))
            return 7, best_hand
        if three_of_a_kind and pairs_present:
            best_hand = [card for card in hand if self.valuation[card.get_value()] == three_value]
            best_hand.extend([card for card in hand if self.valuation[card.get_value()] == max(pairs)][:2])
            return 6, best_hand
        if flush:
            return 5, flush_cards
        if straight: 
            return 4, straight_cards
        if three_of_a_kind:
            best_hand = [card for card in hand if self.valuation[card.get_value()] == three_value]
            best_hand.extend(self.get_highest_cards(hand, 2, best_hand))
            return 3, best_hand
        if len(pairs) >= 2:
            for pair_card in sorted(pairs, reverse=True)[:2]:
                best_hand.extend([card for card in hand if self.valuation[card.get_value()] == pair_card])
            best_hand.extend(self.get_highest_cards(hand, 1, best_hand))
            return 2, best_hand
        if len(pairs) == 1:
            best_hand = [card for card in hand if self.valuation[card.get_value()] == pairs[0]]
            best_hand.extend(self.get_highest_cards(hand, 3, best_hand))
            return 1, best_hand
        
        return 0, self.get_highest_cards(hand, 5)
        
    def break_tie(self, players):
        differing_index = self.find_first_difference_in_hands(*[player.get_best_hand() for player in players])
        max_val = max([self.valuation[player.get_best_hand()[differing_index].get_value()] for player in players])
        winners = [player for player in players if self.valuation[player.get_best_hand()[differing_index].get_value()] == max_val]
        if len(winners) == 1:
            return winners
        else:
            differing_index = self.find_first_difference_in_hands(*[player.get_best_hand() for player in winners])
            max_val = max([self.valuation[player.get_best_hand()[differing_index].get_value()] for player in winners])
            winners_retied = [player for player in winners if self.valuation[player.get_best_hand()[differing_index].get_value()] == max_val]
            return winners_retied
        
class Game:
    def __init__(self, players, dealer):
        self.players = players
        self.dealer = dealer

    def do_round(self, round_number):
        for i in range(len(self.players)):
            player = self.players[i]
            print(f"Player {player.get_id()}:")
            print(player.get_hand(to_print=True))
            print(f"Your stack is: {player.get_stack(to_print=True)}.\n")

            all_good = False
            if round_number == 1:
                if i == 0:
                    print("You are the small blind. You automatically bet $1.\n---------------------------")
                    player.bet(1)
                    self.dealer.set_bet(1)
                    all_good = True
                if i == 1:
                    print("You are the big blind. You automatically bet $2.\n---------------------------")
                    player.bet(2)
                    self.dealer.set_bet(2)
                    all_good = True
            else:
                print(self.dealer.get_runout(to_print=True))

            while all_good == False:
                player_bet = input(f"{self.dealer.get_pot(to_print=True)}\n{self.dealer.get_bet(to_print=True)}\nHow much do you want to bet?\n")
                if player_bet.upper() == "C":
                    if self.dealer.get_bet() == 0:
                        print("You checked.")
                    else:
                        print("You called.")
                        player.bet(self.dealer.get_bet())
                        self.dealer.set_bet(self.dealer.get_bet())

                    all_good = True
                elif player_bet.upper() == "A":
                    print("You went all in!")
                    bet_amount = player.get_stack()
                    self.dealer.set_bet(bet_amount)
                    player.bet(bet_amount)
                    all_good = True
                else:
                    try:
                        player_bet = int(player_bet)
                        print(f"You bet ${player_bet}.\n")
                        print("---------------------------")
                        player.bet(player_bet)
                        self.dealer.set_bet(player_bet)
                        all_good = True
                    except ValueError:
                        print("Illegal bet. Please type a legal bet.")

    def start_game(self):
        self.do_round(1)
        self.dealer.deal_next()
        self.do_round(2)
        self.dealer.deal_next()
        self.do_round(3)
        self.dealer.deal_next()
        self.do_round(4)
