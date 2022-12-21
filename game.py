import os
import time
import random
from collections import defaultdict

from insensitivedict import *
class Color:
    RESET = "\u001b[0m"
    GREEN = "\u001b[32m"
    YELLOW = "\u001b[33m"
    RED = "\u001b[31m"


def rnd_word() -> str:
    """Return random czech word for wordle."""
    with open("pouze5.txt", "r") as r:
        seznam = r.readlines()
        return random.choice(seznam).upper().strip()


def print_intro():
    print("""                                          ▄▄    ▄▄          
                                        ▀███  ▀███          
                                          ██    ██          
▀██▀    ▄█    ▀██▀ ▄██▀██▄▀███▄███   ▄█▀▀███    ██   ▄▄█▀██ 
  ██   ▄███   ▄█  ██▀   ▀██ ██▀ ▀▀ ▄██    ██    ██  ▄█▀   ██
   ██ ▄█  ██ ▄█   ██     ██ ██     ███    ██    ██  ██▀▀▀▀▀▀
    ███    ███    ██▄   ▄██ ██     ▀██    ██    ██  ██▄    ▄
     █      █      ▀█████▀▄████▄    ▀████▀███▄▄████▄ ▀█████▀ """)
    print("Created by Mejroslav")


def game(word: str, tries: int):
    word = word.upper()
    correct_letters = [c for c in word]
    used_words = [] # ukládání již použitých slov
    used_letters = set() # ukládání již použitých písmen
    barvy = []
    pokusy = tries
    
    while pokusy>0:
        time.sleep(1)
        os.system("clear")
        print("".join(barvy))
        print("Zbývá ti ještě {} pokusů.".format(pokusy))
        print("Použitá slova:", ", ".join(used_letters))
        barvy = [None]*5
        player_word = input("Hádej pětipísmenné slovo: ").upper()
        
        if len(player_word) != 5:
            print("Zadané slovo musí obsahovat právě pět písmen!")
            continue
        if remove_diacritics(player_word) in [remove_diacritics(w) for w in used_words]:
            print("Toto slovo jsi již zkusil hádat.")
            continue
        if remove_diacritics(player_word) == remove_diacritics(word):
            break
        
        player_letters = [c for c in player_word]
        used_words.append(player_word)
        used_letters.add(remove_diacritics(player_word))
        # dictionary {letter: number of occurrences in word}
        letters_amount = defaultdict(int)
        for c in correct_letters:
            letters_amount[remove_diacritics(c)] += 1
        
        for i in range(5):
            plr_ltr = player_letters[i]
            cr_ltr = correct_letters[i]
            
            if remove_diacritics(plr_ltr) == remove_diacritics(cr_ltr) :
                    barvy[i] = Color.GREEN + cr_ltr + Color.RESET # se správnou diakritikou
                    letters_amount[remove_diacritics(plr_ltr)] -= 1 # this character has been used
                    
        for i in range(5):
            plr_ltr = player_letters[i]
            cr_ltr = correct_letters[i]
            
            if remove_diacritics(plr_ltr) in letters_amount.keys() and letters_amount[remove_diacritics(plr_ltr)] >  0:
                barvy[i] = Color.YELLOW + plr_ltr + Color.RESET
                letters_amount[remove_diacritics(plr_ltr)] -= 1 # this character has been used
            if not barvy[i]:
                barvy[i] = plr_ltr
        pokusy -= 1
        
    #prohra
    if pokusy == 0:
        print("Bohužel jsi prohrál. Hledané slovo bylo: {}".format(word))
    #výhra
    if remove_diacritics(player_word) == remove_diacritics(word):
        print("Vyhrál jsi! Hledané slovo bylo {}".format(word))
            
def main():
    print_intro()
    pocet = 20
    print("Počet pokusů: {}".format(pocet))
    a = input("Pro spuštění stiskni libovolnou klávesu.")
    game(rnd_word(), pocet)


if __name__ == "__main__":
    main()