from game_classes import Game, Player
import os

def main() -> None:
    run_game_loop()


def run_game_loop() -> None:
    end_game : bool = False 
    
    try:
        while(not end_game): 
            game : Game = Game()
            game.gamestate.set_game_mode(gamemode=Game.GameModeEnum.TWO_PLAYER)
            num_of_players : int = game.gamestate.set_players(player_names=["Player-1", "Player-2"])
            end_round : bool = False

            # Initial deal of two cards per player
            print("\nDealing initial cards...")
            print("-------------------------")
            for _ in range(num_of_players):
                for _ in range(2): 
                    end_round = game.gamecontroller.take_hit()
            print("-------------------------\n")

            while(not end_round):

                for player in game.gamestate.get_players():

                    if player.status == Player.PlayerStatusEnum.UNDER_21:
                        user_input : str = ""

                        while(user_input not in ("1","2")):
                            current_player_name : str = game.gamestate.get_current_player().name
                            current_player_hand_val: int = game.gamestate.get_current_player().hand_value

                            print(f"\n{current_player_name} your current hand: {current_player_hand_val}")
                            user_input = input(f"{current_player_name} what would you like to do: [1] Take a hit or [2] Stand ? ")

                            if user_input not in ("1","2"): print("Invalid selection, please select a valid option.\n")

                        if user_input == "1": 
                            end_round = game.gamecontroller.take_hit()
                        else: 
                            end_round = game.gamecontroller.stand()

                        if end_round: break

            user_input = input(f"\nWould you like to play another round? [1] To play again [Any other key] To quit ")

            if user_input != "1": end_game = True
            clear_terminal()

    except KeyboardInterrupt:
        print("closing game...")
        clear_terminal()


def clear_terminal() -> None:
    try:
        result = os.system("cls||clear)")
        if result != 0: print("\n"*100)
    except FileNotFoundError as e: print(f"Shell not found: {e}")
    except OSError as e: print(f"OS error occured: {e}")


if __name__ == "__main__": 
    main()