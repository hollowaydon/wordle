from collections import Counter
import numpy as np
import pickle

class Wordle:
    def __init__(self, compute_table = True):
        self.word_len = 5
        self.k = 5 # top k words to recall
        # self.save_dest = r"guess_answer.pickle"
        self.wordlist = []
        i = 0
        with open('sow_pods_5.txt') as f:
            for line in f:
                i += 1
                # if i > 500:
                    # break
                self.wordlist.append(line[:5])
        self.wordset = set(self.wordlist)
        self.wordlist = self.wordlist # [:100]

        # load dictionary of best first guesses.
        self.first_guess_dict_exists = True
        try:
            with open('first_guess.pickle', 'rb') as f:
                self.first_guess = pickle.load(f)
        except:
            print('no first guess file found')
            self.first_guess_dict_exists = False

        # load dictionary of best second guesses for each score for first guess.
        self.second_guess_dict_exists = True
        try:
            with open('second_guess.pickle', 'rb') as f:
                self.second_guess = pickle.load(f)
        except:
            print('no second guess file found')
            self.second_guess_dict_exists = False

        self.guess_answer = []
        if compute_table:
            self.compute_guess_answer_table()
    

    def compute_guess_answer_table(self):
        for i, guess in enumerate(self.wordlist):
            self.guess_answer.append(dict())
            for answer in self.wordset:
                self.guess_answer[i][answer] = self.compute_score(guess, answer)
    

    def compute_score(self, guess, answer) -> str:
        score = ''
        # num = 0
        for i in range(self.word_len):
            if guess[i] not in answer:
                score += '0'
                # num += 0 * (3**(4 - i))
            elif guess[i] == answer[i]:
                score += '2'
                # num += 2 * (3**(4 - i))
            else:
                score += '1'
                # num += 1 * (3**(4 - i))
        return score


    def compute_best_guess(self) -> dict:
        # for each guess, loop over possible solutions to work out which guess gives the most information
        guess_dict = dict()
        top_k_H = {'-1':0}
        # best_H = 0
        # best_guess = -1
        for i, guess in enumerate(self.wordlist):
            for answer in self.wordset:
                if guess not in guess_dict.keys():
                    guess_dict[guess] = [self.guess_answer[i][answer]]
                else:
                    guess_dict[guess].append(self.guess_answer[i][answer])

            # compute entropy sum_i p_i log(p_i)
            probs = np.array(list(Counter(guess_dict[guess]).values()))  / len(self.wordset)
            H = -1 * np.sum(np.log(probs) * probs)

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
            if score[i] == '0':
                wordset_restricted = {w for w in wordset_restricted if word[i] not in w}
            elif score[i] == '1':
                # print(i)
                # print(word[i])
                wordset_restricted = {w for w in wordset_restricted if ((w[i] != word[i]) & (word[i] in w))}
            elif score[i] == '2':
                wordset_restricted = {w for w in wordset_restricted if w[i] == word[i]}
            else:
                print('invalid score')
        self.wordset =  wordset_restricted


def main():
    # first, get the top 5 answers for the first guess. The best of these should be 'tares'
    wordle = Wordle(True)
    first_guess = wordle.compute_best_guess()

    # pickle the dictionary
    with open('first_guess.pickle', 'wb') as f:
        pickle.dump(first_guess, f)

    # this program works out the best second guess after we have already guessed 'tares' for each of the 243 possible scores we could get for 'tares'.
    score_vals = ['0', '1', '2']
    scores = []
    for a in score_vals:
        for b in score_vals:
            for c in score_vals:
                for d in score_vals:
                    for e in score_vals:
                        scores.append(f"{a}{b}{c}{d}{e}")
    second_guess = {}
    for i, score in enumerate(scores):
        wordle = Wordle(False)
        wordle.restrict_wordset('tares', score)
        if not wordle.wordset:
            second_guess[score] = "no words match"
        elif len(wordle.wordset) == 1:
            second_guess[score] = {wordle.wordset.pop() : 0.0}
        else:
            wordle.compute_guess_answer_table()
            top_words = wordle.compute_best_guess()
            second_guess[score] = top_words
        print(score)
        print(str(second_guess[score]))
    # pickle the dictionary
    with open('second_guess.pickle', 'wb') as f:
        pickle.dump(second_guess, f)
 


if __name__ == '__main__':
    main()