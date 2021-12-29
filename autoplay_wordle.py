from wordle_improved import Wordle
from collections import Counter
import time

def main():
    tic = time.perf_counter()
    solutions = []

    with open('sow_pods_5.txt') as f:
        for line in f:
            solutions.append(line[:5])

    solutions = solutions[:10]
    
    all_guesses = []
    for solution in solutions:
        wordle = Wordle(False)
        no_guesses = 0 # how many guesses have been made?
        guess = '-1' # guess for initial while check. a dumb and bad guess
        g_a_table_done = False # keep track of once the guess answer table has been computed.
        while guess != solution:
            no_guesses += 1
            if len(wordle.wordset) <= 0:
                print('uh oh, something went wrong')
                break

            elif len(wordle.wordset) == 1:
                guess = list(wordle.wordset)[0]

            elif no_guesses == 1: # first guess
                if wordle.first_guess_dict_exists:
                    guess = max(wordle.first_guess, key=wordle.first_guess.get)
                    # guess should be 'tares'
                else:
                    print('generate on first guess')
                    wordle.compute_guess_answer_table()
                    g_a_table_done = True
                    guess_dict = wordle.compute_best_guess()
                    guess = max(guess_dict, key=guess_dict.get)

                score = wordle.compute_score(guess, solution)
                wordle.restrict_wordset('tares', score)

            elif no_guesses == 2:
                if wordle.second_guess_dict_exists:
                    guess_dict = wordle.second_guess[score]
                    guess = max(guess_dict, key=guess_dict.get)
                else:
                    if not g_a_table_done:
                        print('generate on second guess')
                        wordle.compute_guess_answer_table()
                    guess_dict = wordle.compute_best_guess()
                    guess = max(guess_dict, key=guess_dict.get)
                    g_a_table_done = True
                    

                # guess_dict = wordle.second_guess[score]
                # guess = max(guess_dict, key=guess_dict.get)
                score = wordle.compute_score(guess, solution)
                wordle.restrict_wordset(guess, score)
                if not g_a_table_done:
                    print('generate on third guess')
                    wordle.compute_guess_answer_table()

            else:
                guess_dict = wordle.compute_best_guess()
                guess = max(guess_dict, key=guess_dict.get)
                score = wordle.compute_score(guess, solution)
                wordle.restrict_wordset(guess, score)

        all_guesses.append(no_guesses)
        if no_guesses > 6:
            print(f"{solution} -- {no_guesses} guesses")

    print(str(Counter(all_guesses)))
    print(f"time elapsed: {time.perf_counter() - tic}")

if __name__ == '__main__':
    main()