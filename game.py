import os
import time
import random
from collections import defaultdict

from insensitivedict import remove_diacritics


class Color:
    RESET = "\u001b[0m"
    GREEN = "\u001b[32m"
    YELLOW = "\u001b[33m"
    RED = "\u001b[31m"


class Game:
    def __init__(self) -> None:
        self.print_intro()
        self.setInitValues()
        self.runGame()

    def print_intro(self):
        print(
            """                                          ▄▄    ▄▄          
                                        ▀███  ▀███          
                                          ██    ██          
▀██▀    ▄█    ▀██▀ ▄██▀██▄▀███▄███   ▄█▀▀███    ██   ▄▄█▀██ 
  ██   ▄███   ▄█  ██▀   ▀██ ██▀ ▀▀ ▄██    ██    ██  ▄█▀   ██
   ██ ▄█  ██ ▄█   ██     ██ ██     ███    ██    ██  ██▀▀▀▀▀▀
    ███    ███    ██▄   ▄██ ██     ▀██    ██    ██  ██▄    ▄
     █      █      ▀█████▀▄████▄    ▀████▀███▄▄████▄ ▀█████▀ """
        )
        print("Created by Mejroslav")

    def setInitValues(self):
        self.dict = self.loadDictionary()
        self.correctWord = self.rnd_word()
        self.correctLetters = [c for c in self.correctWord]
        self.usedWords = []  # ukládání již použitých slov
        self.usedLetters = set()  # ukládání již použitých písmen
        self.coloredLetters = []
        self.attempts = 20

    def loadDictionary(self) -> dict[str]:
        slovnik = set()
        with open("pouze5.txt", "r") as r:
            for line in r.readlines():
                slovnik.add(remove_diacritics(line.strip().upper()))
        return slovnik

    def showStatistics(self):
        print("".join(self.coloredLetters))
        print("Zbývá ti ještě {} pokusů.".format(self.attempts))
        print("Použitá slova:", ", ".join(self.usedLetters))

    def getUserWord(self):
        while True:
            userWord: str = str(input("Hádej pětipísmenné slovo: ")).upper()

            if len(userWord) != 5:
                print("Zadané slovo musí obsahovat právě pět písmen!")
                continue
            if remove_diacritics(userWord) not in self.dict:
                print("Slovník tohle slovo nezná.")
                continue
            if self.alreadyGuessed(userWord):
                print("Toto slovo jsi již zkusil hádat.")
                continue
            break
        return userWord

    def alreadyGuessed(self, guess: str) -> bool:
        return remove_diacritics(guess) in [
            remove_diacritics(w) for w in self.usedWords
        ]

    def update(self):
        self.player_letters = [c for c in self.playerGuess]
        self.usedWords.append(self.playerGuess)
        self.usedLetters.add(remove_diacritics(self.playerGuess))

    def updateColoredLetters(self):
        self.coloredLetters = [" "] * 5

        letters_amount = defaultdict(int)
        for c in self.correctLetters:
            letters_amount[remove_diacritics(c)] += 1

        for i in range(5):
            plr_ltr = self.player_letters[i]
            cr_ltr = self.correctLetters[i]

            if remove_diacritics(plr_ltr) == remove_diacritics(cr_ltr):
                self.coloredLetters[i] = (
                    Color.GREEN + cr_ltr + Color.RESET
                )  # se správnou diakritikou
                letters_amount[
                    remove_diacritics(plr_ltr)
                ] -= 1  # this character has been used

        for i in range(5):
            plr_ltr = self.player_letters[i]
            cr_ltr = self.correctLetters[i]

            if (
                remove_diacritics(plr_ltr) in letters_amount.keys()
                and letters_amount[remove_diacritics(plr_ltr)] > 0
            ):
                self.coloredLetters[i] = Color.YELLOW + plr_ltr + Color.RESET
                letters_amount[
                    remove_diacritics(plr_ltr)
                ] -= 1  # this character has been used
            if self.coloredLetters[i] == " ":
                self.coloredLetters[i] = plr_ltr

    def runGame(self):
        while True:
            time.sleep(1)
            os.system("clear")
            self.showStatistics()

            self.playerGuess = self.getUserWord()

            if self.winningCondition(self.playerGuess):
                print("Vyhrál jsi!")
                break

            self.update()
            self.updateColoredLetters()

            self.attempts -= 1
            if self.loseCondition():
                print("Prohrál jsi!")

    def rnd_word(self) -> str:
        """Return a random czech word with 5 letters."""
        with open("pouze5.txt", "r") as r:
            seznam = r.readlines()
            return random.choice(seznam).upper().strip()

    def loseCondition(self) -> bool:
        return self.attempts == 0

    def winningCondition(self, guess: str) -> bool:
        return remove_diacritics(guess) == remove_diacritics(self.correctWord)

    def checkForWin(self):
        if self.loseCondition():
            print(
                "Bohužel jsi prohrál. Hledané slovo bylo: {}".format(self.correctWord)
            )
        if self.winningCondition(self.playerGuess):
            print("Vyhrál jsi! Hledané slovo bylo {}".format(self.correctWord))
