


# generate sowpods words that only have 5 letters.
five_letters = []
with open('sowpods.txt') as f:
    for word in f:
        if len(word) == 6:
            five_letters.append(word[:-1])
            # print(word[:-1])


with open('sow_pods_5.txt', 'w') as f:
    f.write('\n'.join(five_letters))



