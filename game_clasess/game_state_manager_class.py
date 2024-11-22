from game_clasess.deck_class import Deck
from game_clasess.game_mode_enum import GameModeEnum
from game_clasess.player_class import Player

class GameStateManager:
    def __init__(self):
        self.current_player : Player
        self.deck : Deck = Deck()
        self.gamemode: GameModeEnum = GameModeEnum.VS_COMPUTER # Default game mode
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
    
    def get_game_mode(self) -> GameModeEnum:
        return self.gamemode
    
    def set_game_mode(self, gamemode : GameModeEnum) -> None:
        if gamemode in (GameModeEnum.__members__.values()):
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