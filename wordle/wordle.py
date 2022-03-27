from collections import Counter

import numpy as np


class Wordle:
    def __init__(self):
        self.word_len = 5
        self.k = 5  # top k words to recall
        self.save_dest = "data/guess_answer.pickle"
        self.wordlist = []
        i = 0
        with open("data/sow_pods_5.txt") as f:
            for line in f:
                i += 1
                # if i > 500:
                # break
                self.wordlist.append(line[:5])
        self.wordset = set(self.wordlist)
        self.wordlist = self.wordlist  # [:100]
        self.guess_answer = []
        for i, guess in enumerate(self.wordlist):
            self.guess_answer.append(dict())
            for answer in self.wordset:
                self.guess_answer[i][answer] = self.compute_score(guess, answer)

    def compute_score(self, guess, answer) -> str:
        score = ""
        # num = 0
        for i in range(self.word_len):
            if guess[i] not in answer:
                score += "0"
                # num += 0 * (3**(4 - i))
            elif guess[i] == answer[i]:
                score += "2"
                # num += 2 * (3**(4 - i))
            else:
                score += "1"
                # num += 1 * (3**(4 - i))
        return score

    def compute_best_guess(self) -> dict:
        # for each guess, loop over possible solutions to work out which guess gives the most information
        guess_dict = dict()
        top_k_H = {"-1": 0}
        # best_H = 0
        # best_guess = -1
        for i, guess in enumerate(self.wordlist):
            for answer in self.wordset:
                if guess not in guess_dict.keys():
                    guess_dict[guess] = [self.guess_answer[i][answer]]
                else:
                    guess_dict[guess].append(self.guess_answer[i][answer])

            # compute entropy sum_i p_i log(p_i)
            probs = np.array(list(Counter(guess_dict[guess]).values())) / len(self.wordset)
            H = -1 * np.sum(np.log(probs) * probs)

            # store the top k words and entropies
            if len(top_k_H) < self.k:
                top_k_H[guess] = H
            else:
                if H > min(top_k_H.values()):
                    del top_k_H[min(top_k_H, key=top_k_H.get)]
                    top_k_H[guess] = H
        return top_k_H

    def restrict_wordset(self, word, score) -> None:
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
    print("by default, the best first word is 'tares', do you want to recompute to check? (this can take a while)")
    recompute_yn = input("(y/n)")
    # if recompute_yn == 'y' or recompute_yn == 'Y':
    #     [best_word, entropy] = wordle.compute_best_guess()
    for i in range(6):
        if i >= 1 or recompute_yn == "Y" or recompute_yn == "y":
            top_k = wordle.compute_best_guess()
            print(f"the best {wordle.k} options to guess are:")
            for key in sorted(top_k, key=top_k.get, reverse=True):
                print(f"'{key}' with entropy: {top_k[key] : .4f} bits")
            # print(f"best option is {best_word} with {entropy : .4f} bits of information")
        word = input("enter a word:")
        score = input("enter the score for the word:")
        if i == 5 and score != "22222":
            print("oh man! you ran out of guesses")
        if score == "22222":
            if i == 0:
                print("yahoo! you solved the wordle in 1 guess!")
            else:
                print(f"yahoo! you solved the wordle in {i+1} guesses!")
            break
        wordle.restrict_wordset(word, score)
        if len(wordle.wordset) == 0:
            print("ruh roh, there aren't any words left!")
            break
        elif len(wordle.wordset) == 1:
            print(f"only one word left: {wordle.wordset}")
        elif len(wordle.wordset) <= 10:
            print("there aren't many possible words left. here are all the possible remaining words:")
            print(wordle.wordset)
        else:
            print(f"there are {len(wordle.wordset)} possible words remaining")


if __name__ == "__main__":
    main()
