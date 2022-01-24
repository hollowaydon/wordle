import argparse
import pickle
from collections import Counter
from itertools import product

try:
    import numpy as np

    np_available = True
except ImportError:
    print("numpy couldn't be loaded. install numpy for improved performance.")
    np_available = False
    import math


class Wordle:
    def __init__(
        self,
        compute_table=True,
        word_len=5,
        wordfile="sow_pods_5.txt",
        first_dict_file="first_guess.pickle",
        second_dict_file="second_guess.pickle",
        weight=None,
    ):
        self.word_len = word_len
        self.k = 20  # top k words to recall
        # use entropy if false, use min expected remaining words if true.
        # self.min_words_remaining = min_words_remaining
        self.wordlist = []
        with open(wordfile) as f:
            for line in f:
                self.wordlist.append(line[: self.word_len])
        self.wordset = set(self.wordlist)
        self.wordlist = self.wordlist  # [:100]

        # generate weights for each word: all weights start at 1.
        if weight is None:
            self.weights = dict.fromkeys(self.wordlist, 1)
        else:
            with open(weight, "rb") as f:
                self.weights = pickle.load(f)

        # load dictionary of best first guesses.
        try:
            with open(first_dict_file, "rb") as f:
                self.first_guess = pickle.load(f)
        except:
            print("no first guess file found")

        # load dictionary of best second guesses for each score for first guess.
        try:
            with open(second_dict_file, "rb") as f:
                self.second_guess = pickle.load(f)
        except:
            print("no second guess file found")

        self.guess_answer = []
        if compute_table:
            self.compute_guess_answer_table()

    def compute_guess_answer_table(self):
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
        top_k_H = {"-1": 0}  # TODO: remove this I think? don't need this default value for testing any more, but check.
        for i, guess in enumerate(self.wordlist):
            score_frequencies = Counter()
            n_answers = 0
            for answer in self.wordset:
                if guess not in guess_dict.keys():
                    guess_dict[guess] = [self.guess_answer[i][answer]]
                else:
                    guess_dict[guess].append(self.guess_answer[i][answer])
                # add up each score by its weight according to the loaded weights for each answer.
                score_frequencies.update({self.guess_answer[i][answer]: self.weights[answer]})
                n_answers += self.weights[answer]

            score_frequencies = list(score_frequencies.values())
            # compute entropy sum_i p_i log(p_i)
            # score_frequencies = list(Counter(guess_dict[guess]).values())
            # n_answers = len(self.wordset)
            # if numpy is available, this will run faster.
            if np_available:
                probs = np.array(score_frequencies) / n_answers
                H = -1 * np.sum(np.log(probs) * probs) / np.log(2)
            else:
                H = -1 * sum([(x / n_answers) * math.log(x / n_answers) for x in score_frequencies]) / math.log(2)

            # store the top k words and entropies
            if len(top_k_H) < self.k:
                top_k_H[guess] = H
            else:
                if H >= min(top_k_H.values()):
                    del top_k_H[min(top_k_H, key=top_k_H.get)]
                    top_k_H[guess] = H
            try:
                del top_k_H[-1]
            except:
                pass
        return top_k_H

    def restrict_wordset(self, word, score) -> None:
        wordset_restricted = self.wordset
        for i in range(self.word_len):
            if score[i] == "0":
                wordset_restricted = {w for w in wordset_restricted if word[i] not in w}
            elif score[i] == "1":
                wordset_restricted = {w for w in wordset_restricted if ((w[i] != word[i]) & (word[i] in w))}
            elif score[i] == "2":
                wordset_restricted = {w for w in wordset_restricted if w[i] == word[i]}
            else:
                print("error in restrict wordset: invalid score")
        self.wordset = wordset_restricted


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-l", "--len", type=int, default=5, help="the length of the word that is being guessed.")
    parser.add_argument(
        "-w",
        "--wordfile",
        type=str,
        default="sow_pods_5.txt",
        help="file containing all possible words of appropriate length.",
    )
    parser.add_argument(
        "-f",
        "--first_dict_file",
        type=str,
        default="first_guess.pickle",
        help="filename for location to save dictionary of the best first words to guess",
    )
    parser.add_argument(
        "-s",
        "--second_dict_file",
        type=str,
        default="second_guess.pickle",
        help="filename for location to save dictionary of the best second words to guess",
    )
    parser.add_argument(
        "-p",
        "--play_file",
        type=str,
        default="sow_pods_5.txt",
        help="file with all words to use a solutions for autoplay",
    )
    parser.add_argument(
        "--weight",
        type=str,
        default=None,
        help="file with weights for each word. Generally, harder words should have higher weights.",
    )
    # parser.add_argument(
    #     "--min_words",
    #     action="store_true",
    #     default=False,
    #     help="minimise expected number of remaining words instead of maximising entropy"
    # )
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    # first, get the top 5 answers for the first guess. The best of these should be 'tares'
    wordle = Wordle(
        compute_table=True,
        word_len=args.len,
        wordfile=args.wordfile,
        first_dict_file=args.first_dict_file,
        second_dict_file=args.second_dict_file,
        weight=args.weight,
    )

    first_guess = wordle.compute_best_guess()

    # pickle the dictionary
    with open(args.first_dict_file, "wb") as f:
        pickle.dump(first_guess, f)

    # this program works out the best second guess after we have already guessed 'tares' for each of the 243 possible
    # scores we could get for 'tares'.
    scores = ["".join(x) for x in product("012", repeat=args.len)]
    second_guess = {}
    for i, score in enumerate(scores):
        wordle = Wordle(
            compute_table=False,
            word_len=args.len,
            wordfile=args.wordfile,
            first_dict_file=args.first_dict_file,
            second_dict_file=args.second_dict_file,
        )

        best_first = max(first_guess, key=first_guess.get)
        wordle.restrict_wordset(best_first, score)
        if not wordle.wordset:
            second_guess[score] = "no words match"
        elif len(wordle.wordset) == 1:
            second_guess[score] = {wordle.wordset.pop(): 0.0}
        else:
            wordle.compute_guess_answer_table()
            top_words = wordle.compute_best_guess()
            second_guess[score] = top_words
        # print(score)
        # print(str(second_guess[score]))

    # pickle the dictionary
    with open(args.second_dict_file, "wb") as f:
        pickle.dump(second_guess, f)


if __name__ == "__main__":
    main()
