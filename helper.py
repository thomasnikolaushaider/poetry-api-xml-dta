#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, string
import pyphen
from lxml import etree
from lxml.etree import tostring
#from itertools import chain


pyphen.language_fallback('de_DE_variant1')
syllable_dict = pyphen.Pyphen(lang='de_DE')

# exclude = set(string.punctuation)
#regex = re.compile('[%s]' % re.escape(string.punctuation + '.' + ',' + '—' + '-' + '--' + '–' +
#                                          '!' + '?' + '"' + '“' + '”' + "'" + ")" + "(" + "/" + "\\"))
regex = re.compile('[%s]' % re.escape("""1234567890!"#$%&\'()*+,-–./:;<=>?@[\\]^_`{|}~“”"""))

def find_ngrams(input_list, n):
    return zip(*[input_list[i:] for i in range(n)])

def get_vowels():
    vowels = set(u'aeiouäöüyauͤͤoͤ')
    return vowels

def get_diphtongs():
    diphtonge = []
    for v in get_vowels():
        for w in get_vowels():
            diphtonge.append(str(v+w))
            diphtonge.append(str(w+v))
    diphtonge = set(diphtonge)
    return diphtonge


def remove_punct(s):  # From Vinko's solution, with fix.
    newstr = regex.sub('', str(s))
    #if newstr2.endswith("/"):
    #    newstr2 = newstr2[:-1]
    return newstr

def syllabify_sonori(a_word):
    return sp(a_word)

def syllabify(a_word):
    return syllable_dict.inserted(str(a_word))

def strip_text_from_xml(node):
    etree.strip_tags(node, "*")
    stringparts = etree.tostring(node)
    #parts = ([node.text] +
    #        list(chain(*([c.text, tostring(c), c.tail] for c in node.getchildren()))) +
    #        [node.tail])
    #newparts = [i for i in filter(None, parts)]
    # filter removes possible Nones in texts and tails
    #print (''.join(newparts))
    #return ''.join(newparts)
    return stringparts

def get_nucleus(syllable):
    for d in diphtonge:
        if d in syllable:
            return d
    for v in get_vowels():
        if v in syllable:
            return v
