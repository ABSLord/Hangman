import random
import json

language = 0  # default English

name_of_file_with_records = "records.json" # json file with records


HANGMAN = (
    """
       |----
       |   |
       |
       |
       |
       |
       |________
    """,
    """
       |----
       |   |
       |   O
       |
       |
       |
       |________
    """,
    """
       |----
       |   |
       |   O
       |   |
       |
       |
       |________
    """,
    """
       |----
       |   |
       |   O
       |  /|
       |
       |
       |________
    """,
    """
       |----
       |   |
       |   O
       |  /|\\
       |
       |
       |________
    """,
    """
       |----
       |   |
       |   O
       |  /|\\
       |  /
       |
       |________
    """,
    """
       |----
       |   |
       |   O
       |  /|\\
       |  / \\
       |
       |________
    """)


def list_as_word(lst):
    return "".join(lst)


def transform_lists_for_hangman(basic, current, ltr, sep="-"):
    while ltr in basic:
        i = basic.index(ltr)
        current[i] = ltr
        basic[i] = sep


def game():
    global language
    global name_of_file_with_records
    dfc = 0  # difficulty
    name = ""
    with open(name_of_file_with_records, "r") as f:
        lst = json.load(f)  # help-list for dictionary with records
    while True:
        name = str(input("Enter your name: "))
        if name in lst[0]:
            break
        nsw = input("Search failed, add this name?(enter 'yes' if you agree): ").upper()
        if nsw=="YES":
            lst[0][name] = [0, 0]
            break
    words_lst = list()  # all words
    if language == 0:
        language_file_name = "english_words.txt"
    else:
        language_file_name = "russian_words.txt"
    with open(language_file_name) as f:
        for line in f:
            words_lst.append(line.replace("\n", "").split(sep=", "))
    while True:
        dfc = int(input("Choose difficulty: \n"
              "0: Easy\n"
              "1: Medium\n"
              "2: Hard\nEnter a number: "))
        if dfc == 0 or dfc == 1 or dfc == 2:
            break
        else:
            print("Error, try again")

    basic_wrd = random.choice(words_lst[dfc])
    curr_wrd = basic_wrd[0] + "-" * (len(basic_wrd) - 2) + basic_wrd[len(basic_wrd) - 1]
    lst_of_basic_wrd = list(basic_wrd)
    lst_of_curr_wrd = list(curr_wrd)

    lst_of_wrong_ltrs = list()
    count_of_attempts = 6
    current_attempt = 0
    while True:
        print(HANGMAN[current_attempt])
        print("Current word: ", list_as_word(lst_of_curr_wrd))
        print("Wrong letters: ", lst_of_wrong_ltrs)
        while True:
            ltr = input("Enter any letter: ")
            if len(ltr) == 1 and (ord(ltr) in range(ord("a"), ord("z") + 1) or ord(ltr) in range(ord("а"), ord("я") + 1)):
                break
            else:
                print("Error, try again")
        if ltr in lst_of_curr_wrd or ltr in lst_of_wrong_ltrs:
            print("No, You already referred this letter.")  # The counter doesn't increase!
        elif ltr in basic_wrd:
            transform_lists_for_hangman(lst_of_basic_wrd, lst_of_curr_wrd, ltr)
            print("You right!")
        else:
            print("Mistake! There is no such letter in this word. :-(")
            current_attempt += 1
            if ltr not in lst_of_wrong_ltrs:  # Just in case:)
                lst_of_wrong_ltrs.append(ltr)
        if current_attempt == count_of_attempts:
            print(HANGMAN[current_attempt])
            break
        if basic_wrd == list_as_word(lst_of_curr_wrd):
            break

    lst[0][name][0] += 1  # game over
    if basic_wrd == list_as_word(lst_of_curr_wrd) and current_attempt < count_of_attempts:
        print("You win! This word is '", basic_wrd, "'")
        if dfc == 0:
            lst[0][name][1] += 3
        elif dfc == 1:
            lst[0][name][1] += 5
        else:
            lst[0][name][1] += 7
    else:
        print("You lose :-( This word is '", basic_wrd,"'")
    with open(name_of_file_with_records, "w") as f:
        json.dump(lst, f, indent=4, sort_keys=True)
    return


def pretty_print(lst):
    dct = lst[0]
    sorted(dct.values())
    len1 = len("name")
    len2 = len("count of games")
    for key in dct:
        if len(key) > len1:
            len1 = len(key)
        if len(str(dct[key][0])) > len2:
            len2 = len(str(dct[key][0]))
    print("name", end="")
    if len1 > len("name"):
        for i in range(0, len1 - len("name")):
            print(" ", end="")
    print(" ", "|", " ", "count of games", end="")
    if len2 > len("count of games"):
        for i in range(0, len2 - len("count of games")):
            print(" ", end="")
    print(" ", "|", " ", "scores")
    for key in dct:
        print(key, end="")
        if len1 > len(key):
            for i in range(0, len1 - len(key)):
                print(" ", end="")
        print(" ", "|", " ", dct[key][0], end="")
        if len2 > len(str(dct[key][0])):
            for i in range(0, len2 - len(str(dct[key][0]))):
                print(" ", end="")
        print(" ", "|", " ", dct[key][1])


def print_records():
    global name_of_file_with_records
    with open(name_of_file_with_records, "r") as f:
        lst = json.load(f)
    pretty_print(lst)
    while True:
        dlf = str(input("\nIf you want delete ALL records, press 'x', press 0 for exit: "))
        if dlf == "x":
            delete_records()
            print("name | count of games | scores")
        elif dlf == "0":
            return
        else:
            print("Error, try again")
    return


def delete_records():
    global name_of_file_with_records
    with open(name_of_file_with_records, "w") as f:
        json.dump([{}], f, indent=4, sort_keys=True)
    return


def settings():
    global language
    while True:
        lng = int(input("Choose language:\n"
                    "0: English(default)\n"
                    "1: Russian\nEnter a number: "))
        if lng == 0:
            break
        elif lng == 1:
            language = 1
            break
        else:
            print("Error, try again")




