#!/bin/env python3
'transforms a text file that has been wrapped to a fixed with to no longer be wrapped'

# This code was ported from the perl implementation in this project:
#    https://github.com/gbenison/Line-unwrap
# Given that it did not have any kind of license, I'm assuming that it is
# public domain. However, if the original author, Gregory C Benison
# wishes me to not use his code, I'm happy to discuss alternatives.

import fileinput
import re

def early_indent(first_line, next_line):
    'determine if lines are early indented'

    words = next_line.split(' ')
    return (len(first_line + ' ' + words[0]) < len(next_line))

def unwrap(lines):
    'unwrap and print given lines'

    result = []
    previous_line = ''
    sentinel = False
    for line in lines:
        line = line.strip()
        if sentinel:
            if (
                line == '' or
                previous_line == '' or
                re.match(r'^[^A-Za-z0-9]', line) or
                early_indent(previous_line, line)
            ):
                result.extend([previous_line, "\n"])
            else:
                result.extend([previous_line, ' '])
        previous_line = line
        sentinel = True
    result.append(previous_line)
    print(''.join(result))

if __name__ == '__main__':
    unwrap(fileinput.input())
