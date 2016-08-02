from source import game
from source import print_records
from source import settings


def start():
    while True:
        print("MENU")
        print()
        print("1: New game")
        print("2: Records")
        print("3: Settings")
        print("4: Exit")
        act = input("Enter a number: ")
        if act == "1":
            game()
        elif act == "2":
            print_records()
        elif act == "3":
            settings()
        elif act == "4":
            break
        else:
            print("Error, try again")
