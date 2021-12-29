from wordle_improved import Wordle
import pickle

def remaining_options(w):
    if len(w) == 0:
        print("ruh roh, there aren't any words left!")
    elif len(w) == 1:
        print(f'only one word left: {list(w)[0]}')
    elif len(w) <= 10:
        print("there aren't many possible words left. here are all the possible remaining words:")
        print(w)
    else:
        print(f"there are {len(w)} possible words remaining")

def valid_score(score):
    if len(score) != 5:
        return False
    for i in range(5):
        if score[i] not in ['0', '1', '2']:
            return False
    return True

def get_input():
    word = input('enter a word:')
    while len(word) != 5:
        print("the word you entered isn't the right length. try again.")
        word = input('enter a word:')

    score = input('enter the score for the word:')
    while not valid_score(score):
        print("that isn't a valid score. try again.")
        score = input('enter the score for the word:')


    return [word, score]

def main():
    print("are you playing on sowpods with word length 5?")
    print("If you aren't, we'll have to do some computations. takes about 10 mins on my lapop.")
    speedup = input("play on sowpods len 5? (y/n)")
    if speedup == 'y' or speedup == "Y":
        wordle = Wordle(False)
    else:
        wordle = Wordle(True)
        # TODO: IS THIS RIGHT? IS THERE SOMETHIGN ELSE I HAVE TO DO TO GET THIS BIT CORRECT???????

    # wordle = Wordle(False)
    for i in range(6):
        if i == 0:
            if wordle.first_guess_dict_exists:
                top_k_dict = wordle.first_dict
            else:
                wordle.compute_guess_answer_table()
                top_k_dict = wordle.compute_best_guess()
            # print("the best first word is tares")
            print(f"the best {wordle.k} options to guess are:")
            for key in sorted(top_k_dict, key = top_k_dict.get, reverse=True):
                print(f"'{key}' with entropy: {top_k_dict[key] : .4f} bits")
            word, score = get_input()
            
            if score == '2' * wordle.word_len:
                print(f'yahoo! you solved the wordle in 1 guess!')
                break
            wordle.restrict_wordset(word, score)
            remaining_options(wordle.wordset)
            if len(wordle.wordset) == 0:
                break

        elif i == 1:
            if word == 'tares' and wordle.second_guess_dict_exists:
                top_k_dict = wordle.second_dict[score]
            else:
                wordle.compute_guess_answer_table()
                top_k_dict = wordle.compute_best_guess()
            print(f"the best {wordle.k} options to guess are:")
            for key in sorted(top_k_dict, key = top_k_dict.get, reverse=True):
                print(f"'{key}' with entropy: {top_k_dict[key] : .4f} bits")
            
            word, score = get_input()
            # word = input('enter a word:')
            # score = input('enter the score for the word:')
            
            if score == '2' * wordle.word_len:
                print(f'yahoo! you solved the wordle in 2 guesses!')
                break
            
            wordle.restrict_wordset(word, score)
            wordle.compute_guess_answer_table()
            remaining_options(wordle.wordset)
            if len(wordle.wordset) == 0:
                break

        else:
            if len(wordle.wordset) > 1:
                top_k_dict = wordle.compute_best_guess()
                print(f"the best {wordle.k} options to guess are:")
                for key in sorted(top_k_dict, key = top_k_dict.get, reverse=True):
                    print(f"'{key}' with entropy: {top_k_dict[key] : .4f} bits")
                word, score = get_input()
                if i == 5 and score != '2' * wordle.word_len:
                    print('oh man! you ran out of guesses')
                if score == '2' * wordle.word_len:
                    print(f'yahoo! you solved the wordle in {i+1} guesses!')
                    break
                wordle.restrict_wordset(word, score)
                remaining_options(wordle.wordset)
                if len(wordle.wordset) == 0:
                    break
            elif len(wordle.wordset) == 1:
                # print(f"Only word left is: {wordle.wordset}")
                word, score = get_input()
                if i == 5 and score != '2' * wordle.word_len:
                    print('oh man! you ran out of guesses')
                    break
                elif score == '2' * wordle.word_len:
                    print(f'yahoo! you solved the wordle in {i+1} guesses!')
                    break
                wordle.restrict_wordset(word, score)
                remaining_options(wordle.wordset)
                if len(wordle.wordset) == 0:
                    break

                

            
            
    # recompute_yn = input('(y/n)')
    # # if recompute_yn == 'y' or recompute_yn == 'Y':
    # #     [best_word, entropy] = wordle.compute_best_guess()
    # for i in range(6):
    #     if i >= 1 or recompute_yn == "Y" or recompute_yn == 'y':
    #         top_k = wordle.compute_best_guess()
    #         print(f"the best {wordle.k} options to guess are:")
    #         for key in sorted(top_k, key = top_k.get, reverse=True):
    #             print(f"'{key}' with entropy: {top_k[key] : .4f} bits")
    #         # print(f"best option is {best_word} with {entropy : .4f} bits of information")
    #     word = input('enter a word:')
    #     score = input('enter the score for the word:')
    #     if i == 5 and score != '22222':
    #         print('oh man! you ran out of guesses')
    #     if score == '22222':
    #         if i == 0:
    #             print(f'yahoo! you solved the wordle in 1 guess!')
    #         else:
    #             print(f'yahoo! you solved the wordle in {i+1} guesses!')
    #         break
    #     wordle.restrict_wordset(word, score)
    #     if len(wordle.wordset) == 0:
    #         print("ruh roh, there aren't any words left!")
    #         break
    #     elif len(wordle.wordset) == 1:
    #         print(f'only one word left: {list(wordle.wordset)[0]}')
    #     elif len(wordle.wordset) <= 10:
    #         print("there aren't many possible words left. here are all the possible remaining words:")
    #         print(wordle.wordset)
    #     else:
    #         print(f"there are {len(wordle.wordset)} possible words remaining")




if __name__ == '__main__':
    main()