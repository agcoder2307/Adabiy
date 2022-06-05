import re
from collections import Counter
import os

def words(text): return re.findall(r"[а-я|ў|қ|ҳ|ғ|ёА-Я|Ў|Қ|Ҳ|Ғ|Ё]+", text.lower())
#def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open(os.path.join(os.getcwd(), 'base\\lemmas_uz.txt'),encoding='utf-8').read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    #print(max(candidates(word), key=P))
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    options = list((known([word]) or known(edits1(word)) or known(edits2(word)) or [word]))
    if len(options)>5:
        options = options[:5]
    return options

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'абвгдеёжзийклмнопрстуфхцчшъьэюяўқғҳАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЪЬЭЮЯЎҚҒҲ'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


if __name__ == '__main__':
    print(candidates("калей ищлар"))
