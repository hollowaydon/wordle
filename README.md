# Wordle

## arguments you can pass to wordle:
**Length option**

    --len / -l

The length of the word you are trying to guess. By default 5.

**Wordfile option**

    --wordfile / -w

Filename for the file that contains all possible words, one per row. sow_pods_5.txt by default.
sowpods_4.txt contains all 4 letter words if you want to play on that instead.

**Best first word options file**

    --first_dict_file / -f

Filename for where to save/load the pickle file that contains the best first guess (since that is always the same, and takes the longest to compute). first_guess.pickle by default.
first_4.pickle is precomputed for sowpods_4.txt.

**Best second word options file**

    --second_dict_file / -s
    
Filename for where to save/load the pickle file that contains the best second guess, given that the first guess was the best first guess in first_dict_file. second_guess.pickle by default.
second_4.pickle is precomputed for sowpods_4.txt.

**Autoplay word list file**

    --play_file / -p
    
Only used by autoplay_wordle. list of words like wordfile that contains all the words you want autoplay_wordle to play. sow_pods_5.txt by default.

## wordle_improved.py
This file contains the wordle class. Running this file will precompute some options for the best first and second words to guess. Note: the best second word is only based on you guessing the best first word as your first guess.

If you guess something else, the code will have to manually compute the best options, which can take a few minutes for the second guess.

Working out the first guess takes around 15 minutes on my laptop, so precomputing ans saving the first two guesses saves a fair chunk of time, especially if you are running autoplay_wordle.

## play_wordle.py
Will ask you for the words and results you get from wordle, and provides the top 5 best next guesses you can make. Provides top 5 incase the top word isn't accepted as a word by wordle. I haven't had that happen to me yet.

## autoplay_wordle.py
Automatically plays every word that you provide with the following strategy:
- If there is only one possible word left, guess it.
- otherwise, guess the word with maximum entropy.

This strategy isn't optimal. E.g. if multiple words have the same entropy, I think its slightly better to guess whichever also happens to be a possible solution.
