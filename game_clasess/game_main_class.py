from time import sleep

from game_clasess.game_state_manager_class import GameStateManager
from game_clasess.game_controller_class import GameController
from game_clasess.game_mode_enum import GameModeEnum
from game_clasess.player_status_enum import PlayerStatusEnum
from game_clasess.helper_functions import clear_terminal

class Game:
    
    def __init__(self):
        self.end_game : bool = False
        self.end_round : bool = False
        self.gamestate = GameStateManager()
        self.gamecontroller = GameController(_gamestate=self.gamestate)

    def run_game_loop(self) -> None:    
        user_input : str = ""
        gamemode : GameModeEnum = GameModeEnum.VS_COMPUTER # Default game mode
        while(user_input not in ("1","2")):
            user_input : str = input("Which game mode would you like to play: [1] Vs-Computer or [2] 2-Player ? ")
            
            if user_input not in ("1","2"): print("Invalid selection, please select a valid option.\n")
            elif user_input == "1": gamemode : GameModeEnum = GameModeEnum.VS_COMPUTER
            else: gamemode : GameModeEnum = GameModeEnum.TWO_PLAYER

        try:
            while(not self.end_game): 
                current_game : Game = Game()
                current_game.gamestate.set_game_mode(gamemode=gamemode)

                if gamemode == GameModeEnum.VS_COMPUTER:
                    num_of_players : int = current_game.gamestate.set_players(player_names=["User", "Computer"])
                else:
                    num_of_players : int = current_game.gamestate.set_players(player_names=["Player-1", "Player-2"])

                # Initial deal of two cards per player
                print("\nDealing initial cards...")
                print("-------------------------")
                for _ in range(num_of_players):
                    for _ in range(2): 
                        self.end_round = current_game.gamecontroller.take_hit()
                        if self.end_round: break
                print("-------------------------")

                while(not self.end_round):

                    for player in current_game.gamestate.get_players():
                        current_player_name : str = current_game.gamestate.get_current_player().name
                        current_player_hand_val: int = current_game.gamestate.get_current_player().hand_value
                        user_input : str = ""

                        if player.status == PlayerStatusEnum.UNDER_21:
                            
                            if current_player_name == "Computer":
                                
                                print(f"\n{current_player_name}'s current hand: {current_player_hand_val}")

                                if current_player_hand_val < 17:
                                    print(f"Taking a hit for the computer...")
                                    sleep(1)
                                    self.end_round = current_game.gamecontroller.take_hit()
                                else:
                                    print(f"Standing for the computer...")
                                    sleep(1)
                                    self.end_round = current_game.gamecontroller.stand()
                                
                            else:

                                while(user_input not in ("1","2")):
                                    print(f"\n{current_player_name} your current hand: {current_player_hand_val}")
                                    user_input = input(f"{current_player_name} what would you like to do: [1] Take a hit or [2] Stand ? ")

                                    if user_input not in ("1","2"): print("Invalid selection, please select a valid option.\n")
                                    elif user_input == "1": self.end_round = current_game.gamecontroller.take_hit()
                                    else: self.end_round = current_game.gamecontroller.stand()

                        if self.end_round : break

                user_input = input(f"\nWould you like to play another round? [1] To play again or [Any other key] To quit ")

                if user_input != "1": self.end_game = True
                clear_terminal()

        except KeyboardInterrupt:
            print("closing game...")
            clear_terminal()