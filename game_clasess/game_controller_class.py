import copy

from game_clasess.card_class import Card
from game_clasess.card_type_enum import CardTypeEnum
from game_clasess.game_state_manager_class import GameStateManager
from game_clasess.player_class import Player
from game_clasess.player_status_enum import PlayerStatusEnum

class GameController:
    def __init__(self, _gamestate : GameStateManager):
        self._gamestate = _gamestate 
    
    def evaluate_game_status(self) -> bool:
        """
        Wrapper around update_game_staus method, in case additional logic is needed.
        Should be called after every player action.
        """
        return self.update_game_status()

    def update_game_status(self) -> bool:
        """
        Evaluates the current gamestate for blackjack, win, bust, or tie, and updates both the game and player status.
        Returns True if the game should be over, otherwise returns False.
        """
        current_player : Player = self._gamestate.get_current_player()
        current_players : list[Player] = self._gamestate.get_players()
        player_statuses : list[PlayerStatusEnum] = [player.status for player in current_players]
        tie_status : bool = False
        # Check for a tie status
        if len(set(player_statuses)) == 1: tie_status = True
        else: tie_status = False
        
        if current_player.status == PlayerStatusEnum.BLACKJACK:
    
            # If player statuses is not a tie, then the current user wins
            if not tie_status: print(f"\n{current_player.name} has BlackJack (hand={current_player.hand_value}) and wins!")
            else: print("\nIt'a tie game!")
            return True # Game should end in this state, so return True
            
        elif current_player.status == PlayerStatusEnum.BUST:
        
            # If player statuses is not a tie, then the current user loses
            if not tie_status: print(f"\n{current_player.name} has Bust (hand={current_player.hand_value}) and loses!")
            else: print("\nIt'a tie game!")
            return True # Game should end in this state, so return True
        
        elif current_player.status == PlayerStatusEnum.STANDING:
            
            if not tie_status: 
                self._gamestate.switch_current_player()
                return False # Game should continue in this state, so return False
            else:
                current_players = sorted(current_players, key=lambda x: x.hand_value, reverse=True) 
                if current_players[0].hand_value == current_players[1].hand_value:
                    print("\nIt's a tie game.")
                else:
                    print(f"\n{current_players[0].name} has Won (hand={current_players[0].hand_value})!")
                return True # Game should end in this state, so return True
        
        elif current_player.status == PlayerStatusEnum.UNDER_21:
            
            # Check if opponent status is also "UNDER_21", if so switch user, otherwise keep current user until terminal state reached
            other_player_statuses = copy.deepcopy(player_statuses)
            other_player_statuses.remove(PlayerStatusEnum.UNDER_21)
            
            if PlayerStatusEnum.UNDER_21 in other_player_statuses:
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
        if current_player.hand_value == 21: current_player.status = PlayerStatusEnum.BLACKJACK
        elif current_player.hand_value < 21: current_player.status = PlayerStatusEnum.UNDER_21
        else: current_player.status = PlayerStatusEnum.BUST
    
    def stand(self) -> bool:
        """Ends the current player's turn calls the set_current_player method from the GameState class."""
        current_player = self._gamestate.get_current_player()
        current_player.status = PlayerStatusEnum.STANDING
        return self.evaluate_game_status()    
    
    def take_hit(self) -> bool:
        """Calls Deal method on the Deck obj, which returns the card popped from the top(front) of the Deck and add to the current player's hand."""
        hit_card : Card = self._gamestate.deck.deal()
        current_player : Player = self._gamestate.get_current_player()
        current_player.cards.append(hit_card)

        if hit_card.type == CardTypeEnum.ACE:
            if current_player.hand_value + 11 > 21:
                current_player.hand_value += 1
            else:
                if current_player.name != "Computer":
                    user_input : str = ""
                    while(user_input not in ("1","11")):
                        user_input = input(f"{current_player.name} enter the value would you like to take for the Ace card: [1] or [11]? ")
                    if user_input == "1": current_player.hand_value += 1
                    else: current_player.hand_value += 11
                else:
                    current_player.hand_value += 11 #Always have the computer select 11 for aces, if ace + computer hand <= 21
        else:
            current_player.hand_value += hit_card.type.value
        print(f"{current_player.name} your new hand: {current_player.hand_value}", end=" ")
        current_player.show_cards()
        self.set_player_status()
        return self.evaluate_game_status()