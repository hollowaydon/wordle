# for 6 guesses:
#     for each word:
#         for each of 273 options:
#             how many words are removed from _current_ acceptable word list?
#     pick best word
#     ask what the actual word entered and result were
import numpy as np


class Wordle:
    def __init__(self):
        self.word_len = 5
        self.wordlist = []
        with open("sow_pods_5.txt") as f:
            for line in f:
                self.wordlist.append(line[:5])
        self.wordset = set(self.wordlist)
        self.indiv_scores = ["0", "1", "2"]
        self.all_scores = []
        for i in self.indiv_scores:
            for j in self.indiv_scores:
                for k in self.indiv_scores:
                    for l in self.indiv_scores:
                        for m in self.indiv_scores:
                            self.all_scores.append(f"{i}{j}{k}{l}{m}")

    def compute_wordset(self, word, score):
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
        return wordset_restricted

    def restrict_wordset(self, word, score):
        self.wordset_restricted = compute_wordset(word, score)
        self.wordset = wordset_restricted

    def get_best(self):
        improvement = []
        for i, word in enumerate(self.wordlist):
            improvement.append(0)
            for score in self.all_scores:
                cmp_wordset = self.compute_wordset(word, score)
                improvement[i] += len(self.wordset) - len(cmp_wordset)
        improv_np = np.array(improvement)
        best_i = np.argmax(improv_np)
        return [self.wordlist[best_i], improvement[best_i]]


def main():
    print("hello")
    wordle = Wordle()
    for i in range(6):
        [best_word, entropy] = wordle.get_best()
        print(f"best option is {best_word} with {entropy} bits of information")
        word = input("enter a word:")
        score = input("enter the score for the word:")
        wordle.restrict(word, score)


if __name__ == "__main__":
    main()


print(len(wordset))

wordset_2 = restrict_wordset("tonal", "00010", wordset)
print(len(wordset_2))

wordset_3 = restrict_wordset("gripe", "01001", wordset_2)
print(len(wordset_3))

wordset_4 = restrict_wordset("scuba", "00001", wordset_3)
print(len(wordset_4))

wordset_5 = restrict_wordset("fared", "01110", wordset_4)
print(wordset_5)


# weary
# reamy
# rearm
