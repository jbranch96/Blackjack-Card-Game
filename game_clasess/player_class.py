from game_clasess.card_class import Card

from game_clasess.player_status_enum import PlayerStatusEnum

class Player:
        
    def __init__(self, name):
        
        self.name : str = name
        self.cards : list[Card] = []
        self.hand_value : int = 0
        self.status : PlayerStatusEnum = PlayerStatusEnum.UNDER_21 

    def show_all_cards_full(self) -> None:
        card_list : list[tuple]= []
        for card in self.cards: card_list.append((card.type.name, card.suit.value))
        print(card_list)

    def show_all_cards_values(self) -> None:
        card_list : list = []
        for card in self.cards: card_list.append(card.type.name)
        print("hand:", card_list)