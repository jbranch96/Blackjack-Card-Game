from game_clasess.game_main_class import Game


def main() -> None:
    game_instance : Game = Game()
    game_instance.run_game_loop()


if __name__ == "__main__": 
    main()