import datetime

from wordle_improved import Wordle, parse_args


def remaining_options(w):
    if len(w) == 0:
        print("ruh roh, there aren't any words left!")
    elif len(w) == 1:
        print(f"only one word left: {list(w)[0]}")
    elif len(w) <= 10:
        print("there aren't many possible words left. here are all the possible remaining words:")
        print(w)
    else:
        print(f"there are {len(w)} possible words remaining")


def valid_score(score, length):
    if len(score) != length:
        return False
    for i in range(length):
        if score[i] not in ["0", "1", "2"]:
            return False
    return True


def get_input(length, k, top_k_dict, scores_recorded):
    print(f"the best {k} options to guess are:")
    for key in sorted(top_k_dict, key=top_k_dict.get, reverse=True):
        print(f"'{key}' with entropy: {top_k_dict[key] : .4f} bits")

    word = input("enter a word:")
    while len(word) != length:
        print("the word you entered isn't the right length. try again.")
        word = input("enter a word:")

    score = input("enter the score for the word:")
    while not valid_score(score, length):
        print("that isn't a valid score. try again.")
        score = input("enter the score for the word:")
    return [word, score]


def main():
    args = parse_args()
    wordle = Wordle(
        compute_table=False,
        word_len=args.len,
        wordfile=args.wordfile,
        first_dict_file=args.first_dict_file,
        second_dict_file=args.second_dict_file,
        weight=None,
    )

    scores_recorded = []  # store guesses
    for i in range(6):
        if i == 0:
            if wordle.first_guess:
                top_k_dict = wordle.first_guess
            else:
                wordle.compute_guess_answer_table()
                top_k_dict = wordle.compute_best_guess()

            word, score = get_input(args.len, wordle.k, top_k_dict, scores_recorded)
            scores_recorded.append(score)
            if score == "2" * wordle.word_len:
                print("yahoo! you solved the wordle in 1 guess!")
                break

            wordle.restrict_wordset(word, score)
            remaining_options(wordle.wordset)
            if len(wordle.wordset) == 0:
                break

        elif i == 1:
            best_first = max(wordle.first_guess, key=wordle.first_guess.get)
            if word == best_first and wordle.second_guess:
                top_k_dict = wordle.second_guess[score]
            else:
                wordle.compute_guess_answer_table()
                top_k_dict = wordle.compute_best_guess()

            word, score = get_input(args.len, wordle.k, top_k_dict, scores_recorded)
            scores_recorded.append(score)
            if score == "2" * wordle.word_len:
                print("yahoo! you solved the wordle in 2 guesses!")
                break

            wordle.restrict_wordset(word, score)
            wordle.compute_guess_answer_table()
            remaining_options(wordle.wordset)
            if len(wordle.wordset) == 0:
                break

        else:
            if len(wordle.wordset) > 1:
                top_k_dict = wordle.compute_best_guess()
                word, score = get_input(args.len, wordle.k, top_k_dict, scores_recorded)
                scores_recorded.append(score)
                if i == 5 and score != "2" * wordle.word_len:
                    print("oh man! you ran out of guesses")
                if score == "2" * wordle.word_len:
                    print(f"yahoo! you solved the wordle in {i+1} guesses!")
                    break
                wordle.restrict_wordset(word, score)
                remaining_options(wordle.wordset)
                if len(wordle.wordset) == 0:
                    break
            elif len(wordle.wordset) == 1:
                word, score = get_input(args.len, wordle.k, top_k_dict, scores_recorded)
                scores_recorded.append(score)
                if i == 5 and score != "2" * wordle.word_len:
                    print("oh man! you ran out of guesses")
                    break
                elif score == "2" * wordle.word_len:
                    print(f"yahoo! you solved the wordle in {i+1} guesses!")
                    break
                wordle.restrict_wordset(word, score)
                remaining_options(wordle.wordset)
                if len(wordle.wordset) == 0:
                    break

    # copy wordle printing output
    guessess_taken = len(scores_recorded)
    wordle_number = (datetime.date.today() - datetime.date(year=2021, month=6, day=19)).days
    print(f"Wordle {wordle_number} {guessess_taken}/6")
    for score in scores_recorded:
        print(score.replace("2", "\U0001F7E9").replace("1", "\U0001F7E8").replace("0", "\U00002B1B"))


if __name__ == "__main__":
    main()
