# TODO:
#   work out how to make this more efficient for 12.5k size file.
#   fix printing:
#       when 1 option left
#       when a few options left, print them out, otherwise dont
#       print top (3? 5?) words and their entropies.
#       when 0 possible words

import time
from collections import Counter

import numpy as np

tic = time.perf_counter()


class Wordle:
    def __init__(self):
        self.wordlist = []
        i = 0
        with open("sow_pods_5.txt") as f:
            for line in f:
                i += 1
                # if i > 500:
                # break
                self.wordlist.append(line[:5])
        self.wordset = set(self.wordlist)
        self.wordlist = self.wordlist[:100]

        self.word_len = 5

        self.guess_answer = dict()
        for guess in self.wordlist:
            for answer in self.wordset:
                self.guess_answer[(guess, answer)] = self.compute_score(guess, answer)

    def compute_score(self, guess, answer):
        score = ""
        num = 0
        for i in range(self.word_len):
            if guess[i] not in answer:
                score += "0"
                num += 0 * (3 ** (4 - i))
            elif guess[i] == answer[i]:
                score += "2"
                num += 2 * (3 ** (4 - i))
            else:
                score += "1"
                num += 1 * (3 ** (4 - i))
        return score

    def compute_best_guess(self):
        # for each guess, loop over possible solutions to work out which guess gives the most information
        guess_dict = dict()
        best_H = 0
        best_guess = -1
        for guess in self.wordlist:
            for answer in self.wordset:
                if guess not in guess_dict.keys():
                    guess_dict[guess] = [self.guess_answer[(guess, answer)]]
                else:
                    guess_dict[guess].append(self.guess_answer[(guess, answer)])

            # compute entropy sum_i p_i log(p_i)
            probs = np.array(list(Counter(guess_dict[guess]).values())) / len(self.wordset)
            # print(probs)
            H = -1 * np.sum(np.log(probs) * probs)
            if H > best_H:
                best_H = H
                best_guess = guess
        return [best_guess, best_H]

    def restrict_wordset(self, word, score):
        wordset_restricted = self.wordset
        for i in range(self.word_len):
            if score[i] == "0":
                wordset_restricted = {w for w in wordset_restricted if word[i] not in w}
            elif score[i] == "1":
                # print(i)
                # print(word[i])
                wordset_restricted = {w for w in wordset_restricted if ((w[i] != word[i]) & (word[i] in w))}
            elif score[i] == "2":
                wordset_restricted = {w for w in wordset_restricted if w[i] == word[i]}
            else:
                print("invalid score")
        self.wordset = wordset_restricted


def main():
    wordle = Wordle()
    for i in range(6):
        [best_word, entropy] = wordle.compute_best_guess()
        print(f"best option is {best_word} with {entropy : .4f} bits of information")
        word = input("enter a word:")
        score = input("enter the score for the word:")
        wordle.restrict_wordset(word, score)
        if len(wordle.wordset) == 0:
            print("ruh roh, there aren't any words left!")
            break
        elif len(wordle.wordset) == 1:
            print(f"only one word left: {wordle.wordset}")
        elif len(wordle.wordset) <= 10:
            print(wordle.wordset)


if __name__ == "__main__":
    main()


# print(best_guess)
# print(best_H)

toc = time.perf_counter()

print(f"time elapsed: {toc - tic : .2f} s")
