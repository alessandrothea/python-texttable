#!/usr/bin/env python

from click import style
from re import compile
import textwrap

ansi_re = compile('(\033\[((?:\d|;)*)([a-zA-Z]))')
astring = (
    style('aaaa a', fg='red') +
    'bb   bb' + style('   ', bg='red') +
    style('c       cccc', fg='blue') +
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
print repr(astring).replace(r'\x1b','E')[1:-1]
print '-'*80

asci_pos = [(m.group(), m.start(), m.end()) for m in ansi_re.finditer(astring)]

print asci_pos

wrap = 12


def findscreenpos(colortext, n):
    asci_pos = [(m.group(), m.start(), m.end()) for m in ansi_re.finditer(colortext)]

    for g, s, e in asci_pos:
        # print repr(g), s, e, n, '-', n >= s, e-s
        if n >= s:
            n += e-s

    return n


def colortextwrap(text, width):
    plaintext = ansi_re.sub('', text)
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

astring = style('aaaa\na', fg='red')

all_codes = [ (m.start(), m.end(), m.group()) for m in ansi_re.finditer(astring)]

b=''
e=''
# Check for errors
if len(all_codes) == 0:
    pass
elif len(all_codes) == 1:
    if all_codes[0][0] == 0:
        b = all_codes[0][2][0]
    else:
        raise RuntimeError('Argh!!!')
elif len(all_codes) == 2:
    if not (all_codes[0][0] == 0 and all_codes[1][1] == len(astring)):
        raise RuntimeError('Argh!!!2')
    b = all_codes[0][2]
    e = all_codes[1][2]
else:
    raise RuntimeError('Argh!!!3')

print repr(b),repr(e)
raise SystemExit(0)


wrap = 15

# Calculate the linebreaks uwing textwrap
plainlines = textwrap.wrap(ansi_re.sub('', astring), wrap)
print '-'*80
print (ruler*3)[:wrap]
print '\n'.join(plainlines)
print '-'*80
# Get the first linebreak
lb = len(plainlines[0])

# And map it to the color string
clb = findscreenpos(astring, lb)

print lb,clb

# Save the rest of the string
cline =  astring[:clb]

print repr(cline)
print cline+'\x1b[0m'

cbuffer = astring[clb:]

idx = cbuffer.index(plainlines[1][0])

print 'index of ',plainlines[1][0], idx

print repr(cbuffer[:idx])

# Find color codes embedded in t
acii_col = ansi_re.findall(cbuffer[:idx])

# print repr(ansi_re.findall(cbuffer[:idx])[-1][0])


print cbuffer

raise SystemExit(0)

lengths = [len(l) for l in plainlines]
linebreaks = [ sum(lengths[:l+1]) for l in xrange(len(lengths))]
colorlinebreaks = [findscreenpos(astring, lb) for lb in linebreaks]

print zip(linebreaks, colorlinebreaks)

last = 0
for pos in colorlinebreaks:
    print astring[last:pos]
    last = pos
print '-'*80

# translated
print lengths, linebreaks, colorlinebreaks
print '-'*80
print (ruler*3)[:wrap]
print '\n'.join(plainlines)
print '-'*80
print (ruler*3)[:wrap]
print '\n'.join(colortextwrap(astring, wrap))
print
