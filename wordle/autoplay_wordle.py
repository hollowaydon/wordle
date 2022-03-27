import pickle
import random
import time
from collections import Counter, defaultdict

from wordle_improved import Wordle, parse_args


def get_best_guess(guess_dict, word_set):
    max_v = max(guess_dict.values())
    best_k = set()
    for k, v in guess_dict.items():
        if v == max_v:
            best_k.add(k)
    # if possible, choose an equally best word if it is also in the set of possible words.
    if word_set.intersection(best_k):
        guess = random.sample(word_set.intersection(best_k), 1)[0]
    else:
        guess = random.sample(best_k, 1)[0]
    return guess


def main():
    random.seed(123)
    args = parse_args()
    tic = time.perf_counter()
    solutions = []

    with open(args.play_file) as f:
        # TODO: can I just do solutions = f.split()???
        for line in f:
            solutions.append(line[: args.len])

    all_guesses = []
    weight_dict = dict()
    guesses_taken_dict = defaultdict(list)
    for solution in solutions:
        wordle = Wordle(
            compute_table=False,
            word_len=args.len,
            wordfile=args.wordfile,
            first_dict_file=args.first_dict_file,
            second_dict_file=args.second_dict_file,
            weight=None,
        )

        no_guesses = 0  # how many guesses have been made so far?
        guess = ""  # initalise an incorrect guess for initial while check
        g_a_table_done = False  # keep track of once the guess answer table has been computed.
        while guess != solution:
            no_guesses += 1
            if len(wordle.wordset) <= 0:
                print("uh oh, no remaining words to guess")
                break

            elif len(wordle.wordset) == 1:
                guess = list(wordle.wordset)[0]

            elif no_guesses == 1:  # first guess
                if wordle.first_guess:
                    guess = max(wordle.first_guess, key=wordle.first_guess.get)
                    # guess should be 'tares'
                else:
                    # print('generate on first guess')
                    wordle.compute_guess_answer_table()
                    g_a_table_done = True
                    guess_dict = wordle.compute_best_guess()
                    guess = max(guess_dict, key=guess_dict.get)

                score = wordle.compute_score(guess, solution)
                wordle.restrict_wordset(guess, score)

            elif no_guesses == 2:
                if wordle.second_guess:
                    guess_dict = wordle.second_guess[score]
                    guess = max(guess_dict, key=guess_dict.get)
                else:
                    if not g_a_table_done:
                        # print('generate on second guess')
                        wordle.compute_guess_answer_table()
                    guess_dict = wordle.compute_best_guess()
                    guess = max(guess_dict, key=guess_dict.get)
                    g_a_table_done = True

                # guess_dict = wordle.second_guess[score]
                # guess = max(guess_dict, key=guess_dict.get)
                score = wordle.compute_score(guess, solution)
                wordle.restrict_wordset(guess, score)
                if not g_a_table_done:
                    # print('generate on third guess')
                    wordle.compute_guess_answer_table()

            else:
                guess_dict = wordle.compute_best_guess()
                # guess = max(guess_dict, key=guess_dict.get)
                guess = get_best_guess(guess_dict, wordle.wordset)
                score = wordle.compute_score(guess, solution)
                wordle.restrict_wordset(guess, score)

        all_guesses.append(no_guesses)
        # print()

        guesses_taken_dict[no_guesses].append(solution)
        if no_guesses > 6:
            print(f"{solution} -- {no_guesses} guesses")
        # TODO: check if += is better here? maybe need to load separate file for loading and saving the weight dict.
        weight_dict[solution] = no_guesses

    # save dict of results
    with open("minimax_results.pickle", "wb") as f:
        pickle.dump(guesses_taken_dict, f)
    # save weight file.
    # if args.weight:
    #     with open(args.weight, 'wb') as f:
    #         pickle.dump(weight_dict, f)

    print(str(Counter(all_guesses)))
    print(f"time elapsed: {time.perf_counter() - tic}")


if __name__ == "__main__":
    main()
