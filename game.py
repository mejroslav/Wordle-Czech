from collections import defaultdict
import random

class Color:
    RESET = "\u001b[0m"
    GREEN = "\u001b[32m"
    YELLOW = "\u001b[33m"
    RED = "\u001b[31m"

def rnd_word() -> str:
    return "kočka".upper()

translation_table = {
    ord("Á"): ord("A"),
    ord("É"): ord("E"),
    ord("Ě"): ord("E"),
    ord("Í"): ord("I"),
    ord("Ó"): ord("O"),
    ord("Ú"): ord("U"),
    ord("Ů"): ord("U"),
    ord("Ý"): ord("Y"),
    ord("Č"): ord("C"),
    ord("Ď"): ord("D"),
    ord("Ň"): ord("N"),
    ord("Ř"): ord("R"),
    ord("Š"): ord("S"),
    ord("Ť"): ord("T"),
    ord("Ž"): ord("Z"),
}
def remove_diacritics(s: str) -> str:
    """Remove hooks and dashes from a word or letter."""
    return s.translate(translation_table)

def rnd_word() -> str:
    """Return random czech word for wordle."""
    with open("pouze5.txt", "r") as r:
        seznam = r.readlines()
        return random.choice(seznam).upper().strip()

def game(word: str, tries: int):
    correct_letters = [c for c in rnd_word()]
    used_words = [] # ukládání již použitých slov
    barvy = []
    pokusy = tries
    
    while True:
        print("Zbývá ještě {} pokusů".format(pokusy))
        print("".join(barvy))
        
        barvy = [None]*5
        player_word = input("Hádej pětipísmenné slovo: ").upper()
        
        if len(player_word) != 5:
            print("Zadané slovo musí obsahovat právě pět písmen!")
            continue
        if remove_diacritics(player_word) in [remove_diacritics(w) for w in used_words]:
            print("Toto slovo jsi již zkusil hádat.")
            continue     
        player_letters = [c for c in player_word]
        used_words.append(player_word)
               
        print("player_letters:", player_letters)
        print("letters_correct", correct_letters)
               
        # dictionary {letter: number of occurrences in word}
        letters_amount = defaultdict(int)
        for c in correct_letters:
            letters_amount[c] += 1
        
        for i in range(5):
            letter = player_letters[i]
            if letter == correct_letters[i]:
                    barvy[i] = Color.GREEN + letter + Color.RESET
                    letters_amount[letter] -= 1 # this character has been used
        for i in range(5):
            letter = player_letters[i]
            if letter in letters_amount.keys() and letters_amount[letter] >  0:
                barvy[i] = Color.YELLOW + letter + Color.RESET
                letters_amount[letter] -= 1 # this character has been used
            if not barvy[i]:
                barvy[i] = letter
        
        pokusy -= 1
            
def main():
    game(rnd_word(),20)


if __name__ == "__main__":
    main()