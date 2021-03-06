# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

import re
import collections
from nltk.corpus import brown


def words(text):
    return re.findall('[a-z]+', text.lower())


def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(brown.words())
alphabet = 'abcdefghijklmnopqrstuvwxyz'


def edits1(word):
    s = [(word[:i], word[i:]) for i in range(len(word) + 1)]#依次删除字符进行鉴定，构建不同单词类型
    deletes = [a + b[1:] for a, b in s if b]#依次删除字符看是否会构成重构
    transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b) > 1]
    replaces = [a + c + b[1:] for a, b in s for c in alphabet if b]#用字符原始单词代替
    inserts = [a + c + b for a, b in s for c in alphabet]
    return set(deletes + transposes + replaces + inserts)


def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)


def known(words):
    return set(w for w in words if w in NWORDS)


def correct(word):
    candidates = (known([word]) or
                  known(edits1(word)) or
                  known_edits2(word) or
                  [word])
    return max(candidates, key=NWORDS.get)
