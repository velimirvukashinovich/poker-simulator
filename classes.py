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
    def __init__(self):
        self.hand = []
        self.hand_rank = []
        self.best_hand = []
        
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
        self.runout = []
        self.burn_pile = []
        self.pot = 0
        self.deck = Deck()
        
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
            straight_values = {14, 5, 4, 3, 2}
            straight_cards = [card for card in hand if self.valuation[card.get_value()] in straight_values]
    
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
        
        
        
        