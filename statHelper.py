from collections import Counter
from matplotlib import pyplot as plt
import re

def getStats(txt, avoid_list):
    # return string of answer
    lines = txt.count("\n")
    sentences = txt.count(".")
    mostf = ""
    leastf = ""

    wordcount = Counter(txt.replace(".", " ").replace("\n", " ").replace(
        ",", " ").replace(";", " ").replace("_", " ").lower().split())

    sorted_words = wordcount.most_common()
    # most freq
    for x in range(len(sorted_words)):
        if(sorted_words[x][0] not in avoid_list):
            mostf = sorted_words[x][0]
            break

    # # least freq
    for x in range(len(sorted_words) - 1, -1, -1):
        if(sorted_words[x][0] not in avoid_list):
            leastf = sorted_words[x][0]
            break

    stats = "Number of words in file = " + str(sum(wordcount.values())) + "\nNumber of sentences in file = " + str(
        sentences) + "\nNumber of newlines in file = " + str(lines) + "\nMost frequent word in file = " + str(mostf) + "\nLeast frequent word in file = " + str(leastf)

    return stats, wordcount


def extractSentences(txt, keyTxt):
    __ret = ""
    for line in txt.split("."):
        for key in keyTxt.split("\n"):
            if( len(re.findall('\\b'+key+'\\b', line)) > 0 ):
                __ret += line.strip() + "\n"
                break
    return __ret


def plotFrequency(wordcount, fpath):
    # plot histogram and store at given fpath as png
    plt.figure(figsize=(12, 5))
    plt.bar(wordcount.keys(), wordcount.values(), color='g')
    plt.xticks(rotation=30, fontsize=5)
    plt.plot()
    plt.savefig(fpath)
    return
