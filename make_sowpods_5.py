five_letters = []
with open('sowpods.txt') as f:
    for line in f:
        word = line.split('\n')[0]
        if len(word) == 5:
            five_letters.append(word)
            # print(word)

with open('sow_pods_5.txt', 'w') as f:
    f.write('\n'.join(five_letters))