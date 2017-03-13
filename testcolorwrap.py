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

class FormatError(Exception):
    """docstring for FormatError."""
    def __init__(self, *arg, **kwargs):
        super(FormatError, self).__init__(*arg, **kwargs)


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

def extract_color( line ):
    # Find all ansi color escapes in the current line
    col_escapes = [(m.start(), m.end(), m.group()) for m in ansi_re.finditer(astring)]
    n_escapes = len(col_escapes)
    # Check for errors
    # No escapes, plain text, all good.
    if n_escapes == 0:
        return None

    # 1 escape, ok if at the beginning of the line
    elif n_escapes == 1:
        s, e, g = col_escapes[0]

        if s != 0:
            raise FormatError('Color code fount at position %s when expected at 0' % s)

        return g

    elif n_escapes == 2:
        s0, e0, g0 = col_escapes[0]
        s1, e1, g1 = col_escapes[1]

        # But only if the codes are at the beginning and at the end
        if not (s0 == 0 and e1 == len(astring)):
            raise FormatError('Argh!!!2')

        # Note, should the second escape be ignored?
        if not g1 == '\x1b[0m':
            raise FormatError("Color escape found as enf of line while expecting none. " + repr(g1))

        # return the line color
        return g0

    else:
        raise FormatError('Found too many color escapes. Multi-color lines not expected.')


astring = style('aaaa\na', fg='red')

x = extract_color(astring)
print repr(x)
raise SystemExit(0)


# Find all ansi codes in the string
all_codes = [(m.start(), m.end(), m.group()) for m in ansi_re.finditer(astring)]

b=''
e=''

# Check for errors
# No codes, plain text
if len(all_codes) == 0:
    pass

# 1 codes, maybe OK
elif len(all_codes) == 1:

    # OK if the code start at pos 0
    if all_codes[0][0] == 0:
        b = all_codes[0][2][0]

    # Throw otherwise
    else:
        raise RuntimeError('Argh!!!')

# 2 codes, possibly very good.
elif len(all_codes) == 2:

    # But only if the codes are at the beginning and at the end
    if not (all_codes[0][0] == 0 and all_codes[1][1] == len(astring)):
        raise RuntimeError('Argh!!!2')

    # Store the codes for later
    b = all_codes[0][2]
    e = all_codes[1][2]
    # TODO: check that e is reset, i.e. \x1b[0m

# More than 2 codes, not good

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
