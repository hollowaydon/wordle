# wordle

## arguments you can pass to wordle:
**--len / -l**

    The length of the word you are trying to guess. By default 5.

**--wordfile / -w**

    filename for the file that contains all possible words, one per row. sow_pods_5.txt by default.

**--first_dict_file / -f**

    filename for where to save/load the pickle file that contains the best first guess. first_guess.pickle by default.

**--second_dict_file / -s**

    filename for where to save/load the pickle file that contains the best second guess, given that the first guess was the best first guess in first_dict_file. second_guess.pickle by default.

**--play_file / -p**

    Only used by autoplay_wordle. list of words like wordfile that contains all the words you want autoplay_wordle to play. sow_pods_5.txt by default.

## wordle_imporoved
This file contains the wordle class. Running this file will precompute some options for the best first and second words to guess. Note: the best second word is only based on you guessing the best first word as your first guess.

If you guess something else, the code will have to manually compute the best options, which can take a few minutes for the second guess.

Working out the first guess takes around 15 minutes on my laptop, so precomputing ans saving the first two guesses saves a fair chunk of time, especially if you are running autoplay_wordle.

## play_wordle
Will ask you for the words and results you get from wordle, and provides the top 5 best next guesses you can make. Provides top 5 incase the top word isn't accepted as a word by wordle. I haven't had that happen to me yet.

## autoplay_wordle
Automatically plays every word that you provide with the following strategy:
- If there is only one possible word left, guess it.
- otherwise, guess the word with maximum entropy.

This strategy isn't optimal. E.g. if multiple words have the same entropy, I think its slightly better to guess whichever also happens to be a possible solution.
