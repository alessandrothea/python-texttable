#!/usr/bin/env python

from click import style
from re import compile
import textwrap

asci_re = compile('(\033\[((?:\d|;)*)([a-zA-Z]))')
astring = (
    style('aa a', fg='red') +
    'bb   bb' +
    style('c cccc', fg='blue') +
    ' d  ddddd' +
    style('eeee e    ', fg='green') +
    ' k kk  k'
    )

ruler = '0123456789'

print '-'*80
print ruler*4
print astring
print '-'*80

print
print '-'*80
print ruler*8
print repr(astring)
print '-'*80

asci_pos = [(m.group(), m.start(), m.end()) for m in asci_re.finditer(astring)]

print asci_pos

wrap = 12


def findscreenpos(colortext, n):
    asci_pos = [(m.group(), m.start(), m.end()) for m in asci_re.finditer(colortext)]

    for g, s, e in asci_pos:
        # print repr(g), s, e, n, '-', n >= s, e-s
        if n >= s:
            n += e-s

    return n


def colortextwrap(text, width):
    plaintext = asci_re.sub('', text)
    # print len(plaintext), len(plaintext)//width

    # for k in range(len(plaintext)//width):
        # pos = findscreenpos(text, k*width)
        # print k*width, pos

    lines = []
    last = 0
    for pos in [findscreenpos(text, k*width) for k in range(1,len(plaintext)//width+1)]:
        print last, pos
        print text[last:pos]
        lines.append('aa')
        last = pos
    return []

# for i in xrange(5):
#     print 'i =', i, '-----'
#     k = findscreenpos(i)
#     print i, '--->', k
#     print astring
#     print '-'*i+'^'
#     print ruler*2
#     print repr(astring).replace(r'\x1b', 'E')[1:-1]
#     print '-'*k+'^'
#     print
#     print


print '-'*80
print (ruler*3)[:15]
print '\n'.join(textwrap.wrap(asci_re.sub('', astring), 15))
print '-'*80
print (ruler*3)[:15]
print '\n'.join(colortextwrap(astring, 15))
print
