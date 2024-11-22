import os

def clear_terminal() -> None:
    try:
        result = os.system("cls||clear)")
        if result != 0: print("\n"*100)
    except FileNotFoundError as e: print(f"Shell not found: {e}")
    except OSError as e: print(f"OS error occured: {e}")