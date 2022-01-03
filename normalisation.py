# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

import pickle
from io import open

from nltk.corpus import names

from normalise.detect import create_NSW_dict, mod_path
from normalise.tagger import is_alpha, tagify, is_digbased
from normalise.splitter import split, retagify
from normalise.class_ALPHA import run_clfALPHA
from normalise.class_NUMB import run_clfNUMB, gen_frame
from normalise.tag_MISC import tag_MISC
# from tag import tag_MISC
from normalise.expand_all import expand_all
from normalise.expand_NUMB import bmoney
import re

with open('{}/data/wordlist.pickle'.format(mod_path), mode='rb') as file:
    wordlist = pickle.load(file)

with open('{}/data/names.pickle'.format(mod_path), mode='rb') as file:
    names_lower = pickle.load(file)


def list_NSWs(text, verbose=True, variety='BrE', user_abbrevs={}):
    if verbose:
        print("\nCREATING NSW DICTIONARY")
        print("-----------------------\n")

    NSWs = create_NSW_dict(text, verbose=verbose)#提取出不能直接翻译的文本或者缩写等，同时字典将其位置与标签确定了，能够在标记的位置显示
    if verbose:
        print("{} NSWs found\n".format(len(NSWs)))
        print("TAGGING NSWs")
        print("------------\n")
    tagged = tagify(NSWs, verbose=verbose)#为缩写或者无法识别的内容打上标签，确定缩写类型，即字母/数字/MISC还不知道是啥
    ALPHA_dict = {}
    NUMB_dict = {}
    MISC_dict = {}
    SPLT_dict = {}
    for item in tagged.items():#选择其中的元素，挨个进行更新或者细化标签，创建单独类型的标签
        tag = item[1][1]
        if tag == 'ALPHA':
            ALPHA_dict.update((item,))
        elif tag == 'NUMB':
            NUMB_dict.update((item,))
        elif tag == 'MISC':
            MISC_dict.update((item,))#杂项
        elif tag == 'SPLT':
            SPLT_dict.update((item,))
    if verbose:
        print("SPLITTING NSWs")
        print("--------------\n")
    splitted = split(SPLT_dict, verbose=verbose)#找到原始单词中需要split出来单独进行SFW的，对应标签为前缀，之后为其中的后缀，不带上缩写
    if verbose:
        print("RETAGGING SPLIT NSWs")
        print("--------------------\n")
    retagged = retagify(splitted, verbose=verbose)#重新给定标签
    for item in retagged.items():
        tag = item[1][1]
        if tag == 'SPLT-ALPHA':
            ALPHA_dict.update((item,))
        elif tag == 'SPLT-NUMB':
            NUMB_dict.update((item,))
        elif tag == 'SPLT-MISC':
            MISC_dict.update((item,))
    if verbose:
        print("CLASSIFYING ALPHABETIC NSWs")
        print("---------------------------\n")
    tagged_ALPHA = run_clfALPHA(ALPHA_dict, text, verbose=verbose, user_abbrevs=user_abbrevs)#利用训练的网络，来预测出所要采用标签
    if verbose:
        print("CLASSIFYING NUMERIC NSWs")
        print("------------------------\n")
    tagged_NUMB = run_clfNUMB(NUMB_dict, text, verbose=verbose)#利用分类网络，预测出所确定的标签
    if verbose:
        print("CLASSIFYING MISCELLANEOUS NSWs")
        print("------------------------------\n")
    tagged_MISC = tag_MISC(MISC_dict, verbose=verbose)
    if verbose:
        print("EXPANDING ALPHABETIC NSWs")
        print("-------------------------\n")
    expanded_ALPHA = expand_all(tagged_ALPHA, text, verbose=verbose, variety=variety, user_abbrevs=user_abbrevs)##Fork，此句关键即根据标签和实体确定实际文本内容###
    if verbose:
        print("EXPANDING NUMERIC NSWs")
        print("----------------------\n")
    expanded_NUMB = expand_all(tagged_NUMB, text, verbose=verbose, variety=variety, user_abbrevs=user_abbrevs)
    if verbose:
        print("EXPANDING MISCELLANEOUS NSWs")
        print("----------------------------\n")
    expanded_MISC = expand_all(tagged_MISC, text, verbose=verbose, variety=variety, user_abbrevs=user_abbrevs)
    return expanded_ALPHA, expanded_NUMB, expanded_MISC


def tokenize_basic(text):
    guess = [d.replace(u'\xa0', u'') for w in text.split(' ') for d in w.split('\n')]#按照换行符进行更换中按照空格进行分词,去除其中分隔符不标准的问题
    out = []
    stop_lib=['.',',','!','?',';']
    for i in range(len(guess) - 1):
        cur=re.sub("[A-Za-z0-9]",'',guess[i])
        res=[j for j in cur if j in stop_lib]
        if not guess[i]:
            pass
        elif guess[i].isalpha():
            out.append(guess[i])
        elif len(guess[i])==1: out.append(guess[i])
        elif guess[i][0] in ['(', '[', '{','“','\'','‘','”']:#修改，暂时在分词中增加了中文的一个双引号识别，之后看是否还会有其它的
            if guess[i][1] in [')', ']', '}','”','\'','‘'] or guess[i][-1] in [')', ']', '}','”','\'','’'] :
                out.extend([guess[i][0], guess[i][1:-1], guess[i][-1]])
            else:
                out.extend([guess[i][0], guess[i][1:]])
        elif guess[i][-1] in [')', ']', '}','”','\'','’']:
            for j in range (len(guess[i])):
                if not (guess[i][j].isalpha() or guess[i][j].isdigit()):
                    out.extend([guess[i][:j],guess[i][j]])
                    break
            for x in range(j,len(guess[i])):
                out.append(guess[i][x])
        elif guess[i][-1] in ['!', '?',';'] and guess[i][:-1].isalpha():
            out.extend([guess[i][:-1], guess[i][-1]])
        elif guess[i][-1] == '.' :
            following = guess[i + 1]
            if guess[i][:-1].isalpha():
                if following.istitle() and following.lower() in wordlist:#检查开头是否为大写，同时检查全部小写后是否在字典库中
                    if following.lower() in names_lower:
                        if guess[i][:-1] in wordlist:
                            out.extend([guess[i][:-1], '.'])
                        else:
                            out.append(guess[i])
                    else:
                        out.extend([guess[i][:-1], '.'])
                elif guess[i][-1] == '.' and is_digbased(guess[i][:-1]):#筛选围绕数字的th/数字型的内容
                    out.extend([guess[i][:-1], '.'])
                else:
                    out.append(guess[i])
            elif is_digbased(guess[i][:-2]):
                out.extend([guess[i][:-2], guess[i][-2],'.'])
            else:#判定倒数第二个是不是字符
                out.extend([guess[i][:-1],guess[i][-1]])      
        elif guess[i].endswith((',', ':', ';')):
            out.extend([guess[i][:-1], guess[i][-1]])
        elif guess[i].find(cur[-1]) ==len(guess[i])-1: #将符号为结尾的混合的字符串单独提出来
            out.extend([strstay.match(guess[i]).group(),cur])
       #--------------*--------------------
        #解决之前单词中间.!?等号无空格的问题
        elif res and res.count('.') <= 1:##对URL链接类型的词汇需要进行选择不分级
            # if not guess[i][guess[i].find(res[-1])+1].isalpha():
            #     out.extend([guess[i][:guess[i].find(res[-1])],res[-1]])
            #     for j in range(guess[i].find(res[-1])+1,len(guess[i])):
            #         if guess[i][j].isalpha():
            #             break
            #         else:
            #             out.append(guess[i][j])
            #         del j
            #     # out.append(guess[i][index:])
            # else:
            out.extend([guess[i][:guess[i].find(res[0])],''.join(res),guess[i][guess[i].find(res[-1])+1:]])
            ####-----------------------------*---------
            del res
        else:
            out.append(guess[i])
            
    if not guess[-1]:
        pass
    elif guess[-1].isalpha():
        out.append(guess[-1])
    elif guess[-1][-1] in ['!', '?'] and guess[-1][:-1].isalpha():
        out.extend([guess[-1][:-1], guess[-1][-1]])
    elif guess[-1][-1] == '.' and guess[-1][:-1] in wordlist:#用的给定的wordlist的字典中的值
        out.extend([guess[-1][:-1], '.'])
    elif guess[-1][-1] == '.' and is_digbased(guess[-1][:-1]):
        out.extend([guess[-1][:-1], '.'])
    elif guess[-1].endswith((',', ':', ';')):
        out.extend([guess[-1][:-1], guess[-1][-1]])
    else:
        out.append(guess[-1])
    del stop_lib
    return out


def normalise(text, tokenizer=tokenize_basic, verbose=True, variety='BrE', user_abbrevs={}):
    if type(text) == str:
        if tokenizer == tokenize_basic and verbose:
            print("NOTE: using basic tokenizer.\n"
                  "For better results, input tokenized text,"
                  " or use a custom tokenizer")
            return insert(tokenizer(text), verbose=verbose, variety=variety, user_abbrevs=user_abbrevs)
        else:
            return insert(tokenizer(text), verbose=verbose, variety=variety, user_abbrevs=user_abbrevs)
    else:
        return insert(text, verbose=verbose, variety=variety, user_abbrevs=user_abbrevs)


def insert(text, verbose=True, variety='BrE', user_abbrevs={}):
    (expanded_ALPHA,
    expanded_NUMB,
    expanded_MISC) = list_NSWs(text, verbose=verbose, variety=variety, user_abbrevs=user_abbrevs)
    out = text[:]#用之后选定的原来的单词替换对应索引的单词
    split_dict = {}
    for item in (expanded_ALPHA, expanded_NUMB, expanded_MISC):
        for nsw in item.items():
            if isinstance(nsw[0], int):
                out[nsw[0]] = nsw[1][3]
                if nsw[1][2] == 'MONEY' and gen_frame(nsw, text)[3] in bmoney:
                    out[nsw[0] + 1] = ''
            else:
                rind = int(nsw[0])
                if rind in split_dict:
                    split_dict[rind][100 * (nsw[0] - rind)] = nsw[1][3]
                else:
                    split_dict[rind] = {(100 * (nsw[0] - rind)): nsw[1][3]}
                if out[rind] == text[rind]:
                    out[rind] = nsw[1][3]
                else:
                    final = ''
                    for it in sorted(split_dict[rind]):
                        final += ' '
                        final += split_dict[rind][it]
                    final = final[1:]
                    out[rind] = final
    return out


def rejoin(tokenized_text):
    out = ''
    for word in tokenized_text:
        if word:
            out += word
            out += ' '
    return out[:-1]


strstay = re.compile('''
[A-Za-z0-9]*
''', re.VERBOSE)
