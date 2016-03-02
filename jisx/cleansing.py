#! /usr/bin/env python
# -*- coding: utf-8 -*-

import codecs, sys
import mojimoji

sys.stdout = codecs.getwriter('cp932')(sys.stdout)
sys.stdin = codecs.getreader('cp932')(sys.stdin)

argvs=sys.argv
argc=len(argvs)

if argc != 2:
    print('Usage: python cleansing.py [kiffile]')
    exit(1)

jisx_list=[]
with open('jisx/JIS0208.TXT', 'r') as f:
    for l in f:
        if l[0] != '#':
            c = l.split("\t")[2]
            jisx_list.append(unichr(int(c, 16)))

repl_map={}
repl_str_map={}
with codecs.open('jisx/replace', 'r', 'utf-8') as f:
    for l in f:
        rep_array = l.split(':')
        if rep_array[0] == 'c':
            repl_map[rep_array[1]] = unichr(int(rep_array[2], 16))
        elif rep_array[0] == 's':
            repl_str_map[rep_array[1]] = rep_array[2]

with codecs.open(argvs[1], 'r', 'cp932') as f:
    for l in f:
        line = l.rstrip()
        if line.startswith('&'):
            continue
        if not(line.startswith('*')):
            print(line)
            continue
        line_com = line[1:]
        for k, v in repl_str_map.items():
            line_com = line_com.replace(k, v)
        line_zen = mojimoji.han_to_zen(line_com)
        line_char = list(line_zen)
        line_clean = '*'
        for c in line_char:
            if c == '\n' or c == '\r':
                continue
            elif c in repl_map:
                if not(repl_map[c] in jisx_list):
                    sys.stderr.write('Replace map error:', c, '->', repl_map[c])
                else:
                    line_clean += repl_map[c]
                continue
            elif c in jisx_list:
                line_clean += c
                continue
            else:
                sys.stderr.write((c+':'+line+'\n').encode('utf-8'))
                #line_clean += c
        print(line_clean)
