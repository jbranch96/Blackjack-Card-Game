from dataclasses import dataclass
from enum import Enum, auto
from random import shuffle
import copy

@dataclass
class Card:
    
    class CardSuitEnum(Enum):

        def _generate_next_value_(name, start, count, last_values) -> str:
            return name.lower() # Sets each value to the lowercase version of the name

        CLUBS = auto()
        DIAMONDS = auto()
        HEARTS = auto()
        SPADES = auto()

    class CardTypeEnum(Enum):

        ACE = auto() # Making Ace have a default of 1, will handle logic externally for if user wants the value to be 11
        _2 = auto()
        _3 = auto()
        _4 = auto()
        _5 = auto()
        _6 = auto()
        _7 = auto()
        _8 = auto()
        _9 = auto()
        _10 = auto()
        JOKER = 10
        QUEEN = 10
        KING = 10

    type  : CardTypeEnum # Type also contains card value as enum value
    suit  : CardSuitEnum

    def __post_init__(self):
        if self.type.value < 1:
            raise ValueError("Card value cannot be less than 1.")
        if self.type.value > 11:
            raise ValueError("Card value cannot be greater than 11.")
        if self.suit not in (self.CardSuitEnum.__members__.values()):
            raise ValueError("Invalid specification for card suit.")


class Deck:

    def __init__(self):
        self.cards = [
            Card(c_type, c_suit) for c_type in Card.CardTypeEnum.__members__.values() for c_suit in Card.CardSuitEnum.__members__.values()
        ]
        self.shuffle()

    def deal(self) -> Card:
        if len(self.cards) > 0:
            return self.cards.pop(0)
        else:
            raise IndexError("Cannot pop from a deck without any cards.")
    
    def shuffle(self) -> None:
        shuffle(self.cards)


class Player:
        
    class PlayerStatusEnum(Enum):

        UNDER_21 = auto()
        BLACKJACK = auto()
        BUST = auto()
        STANDING = auto()

    def __init__(self, name):
        
        self.name : str = name
        self.cards : list[Card] = []
        self.hand_value : int = 0
        self.status : self.PlayerStatusEnum = self.PlayerStatusEnum.UNDER_21 

    def show_cards(self) -> None:
        card_list : list[tuple]= []
        for card in self.cards: card_list.append((card.type.name, card.suit.value))
        print(card_list)


class Game:
    
    def __init__(self):
        self.gamestate = self.GameState()
        self.gamecontroller = self.GameController(_gamestate=self.gamestate)

    class GameModeEnum(Enum):
            
            TWO_PLAYER = auto()
            VS_COMPUTER = auto()

    class GameState:

        def __init__(self):
            self.current_player : Player
            self.deck : Deck = Deck()
            self.gamemode: Game.GameModeEnum = Game.GameModeEnum.TWO_PLAYER # Default game mode
            self.players : list[Player] = []
        
        def get_current_player(self) -> Player:
            return self.current_player
        
        def get_next_player(self) -> Player:
            current_idx = self.players.index(self.current_player)
            next_idx = (current_idx + 1) % len(self.players)
            return self.players[next_idx]

        def set_current_player(self, selected_player : Player) -> None:
            if selected_player in (self.players):
                self.current_player = selected_player
                print(f"Currently {self.current_player.name} turn to go.")
            else:
                raise ValueError("Invalid selection for current Player.")
            
        def switch_current_player(self) -> None:
            current_idx = self.players.index(self.current_player)
            next_idx = (current_idx + 1) % len(self.players)
            self.current_player = self.players[next_idx]

        def get_game_mode(self) -> "Game.GameModeEnum":
            return self.gamemode

        def set_game_mode(self, gamemode : "Game.GameModeEnum") -> None:
            if gamemode in (Game.GameModeEnum.__members__.values()):
                self.gamemode = gamemode
            else:
                raise ValueError("Invalid selection for game mode.")
        
        def get_players(self) -> list[Player]:
            return self.players

        def set_players(self, player_names : list[str]) -> int:
            previous_size : int = len(self.players)
            player_objs = [Player(name=name) for name in player_names if (name is not None and name != "")]
            self.players.extend(player_objs)
            current_size : int = len(self.players)
            if previous_size == 0: self.set_current_player(self.players[0])
            return current_size - previous_size

    class GameController:

        def __init__(self, _gamestate : "Game.GameState"):
            self._gamestate = _gamestate 

        def evaluate_game_state(self) -> bool:
            """
            Evaluates the current gamestate for blackjack, win, bust, or tie, should be called after every player action.
            Returns True if the game should be over, otherwise returns False.
            """
            current_player : Player = self._gamestate.get_current_player()
            current_players : list[Player] = self._gamestate.get_players()
            player_statuses : list[Player.PlayerStatusEnum] = [player.status for player in current_players]
            tie_status : bool = False

            # Check for a tie status
            if len(set(player_statuses)) == 1: tie_status = True
            else: tie_status = False

            if self._gamestate.get_game_mode() == Game.GameModeEnum.TWO_PLAYER:
                
                if current_player.status == Player.PlayerStatusEnum.BLACKJACK:
                
                    # If player statuses is not a tie, then the current user wins
                    if not tie_status: print(f"\n{current_player.name} has BlackJack (hand={current_player.hand_value}) and wins!")
                    else: print("\nIt'a tie game!")
                    self._gamestate.switch_current_player()
                    return True # Game should end in this state, so return True
                
                elif current_player.status == Player.PlayerStatusEnum.BUST:
                
                    # If player statuses is not a tie, then the current user loses
                    if not tie_status: print(f"\n{current_player.name} has Bust (hand={current_player.hand_value}) and loses!")
                    else: print("\nIt'a tie game!")
                    return True # Game should end in this state, so return True
                
                elif current_player.status == Player.PlayerStatusEnum.STANDING:
                    
                    if not tie_status: self._gamestate.switch_current_player()
                    
                    else:
                        current_players = sorted(current_players, key=lambda x: x.hand_value, reverse=True) 
                        
                        if current_players[0].hand_value == current_players[1].hand_value:
                            print("\nIt's a tie game.")
                        else:
                            print(f"\n{current_players[0].name} has Won (hand={current_players[0].hand_value})!")

                        return True # Game should end in this state, so return True
                
                elif current_player.status == Player.PlayerStatusEnum.UNDER_21:
                    
                    # Check if opponent status is also "UNDER_21", if so switch user, otherwise keep current user until terminal state reached
                    other_player_statuses = copy.deepcopy(player_statuses)
                    other_player_statuses.remove(Player.PlayerStatusEnum.UNDER_21)
                    
                    if Player.PlayerStatusEnum.UNDER_21 in other_player_statuses:
                        self._gamestate.switch_current_player()
                        return False # Game should continue in this state, so return False
                    else:
                        opponent_player = self._gamestate.get_next_player()
                        
                        if current_player.hand_value > opponent_player.hand_value:
                            print(f"\n{current_player.name} has Won (hand={current_player.hand_value})!")
                            return True # Game should end in this state, so return True
                        else:
                            return False # Game should continue in this state, so return False
                       
        def set_player_status(self) -> None:
            """Evalutes the current player's hand and sets the appropriate player status enum for the current player."""
            current_player : Player = self._gamestate.get_current_player()

            if current_player.hand_value == 21: current_player.status = Player.PlayerStatusEnum.BLACKJACK
            elif current_player.hand_value < 21: current_player.status = Player.PlayerStatusEnum.UNDER_21
            else: current_player.status = Player.PlayerStatusEnum.BUST

        def stand(self) -> bool:
            """Ends the current player's turn calls the set_current_player method from the GameState class."""
            current_player = self._gamestate.get_current_player()
            current_player.status = Player.PlayerStatusEnum.STANDING
            return self.evaluate_game_state()    

        def take_hit(self) -> bool:
            """Calls Deal method on the Deck obj, which returns the card popped from the top(front) of the Deck and add to the current player's hand."""
            hit_card : Card = self._gamestate.deck.deal()

            current_player : Player = self._gamestate.get_current_player()
            current_player.cards.append(hit_card)

            if hit_card.type == Card.CardTypeEnum.ACE:
                if current_player.hand_value + 11 > 21:
                    current_player.hand_value += 1
                else:
                    user_input : str = ""
                    while(user_input not in ("1","11")):
                        user_input = input(f"{current_player.name} enter the value would you like to take for the Ace card: [1] or [11]? ")
                    if user_input == "1": current_player.hand_value += 1
                    else: current_player.hand_value += 11
            else:
                current_player.hand_value += hit_card.type.value

            print(f"{current_player.name} your new hand: {current_player.hand_value}", end=" ")
            current_player.show_cards()
            self.set_player_status()
            return self.evaluate_game_state()