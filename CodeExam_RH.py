#!/usr/bin/env python
# CodeExam_RH by

"""
Search for a provided regex in the file received.
"""

__author__ = 'enavd'

import re
from argparse import ArgumentParser

# Set up arguments parsing:
parser = ArgumentParser(description=__doc__)
parser.add_argument('-p', '--pattern', help='RegEx pattern to look for in the file(s) provided')
parser.add_argument('-f', '--file', help='File(s) in which the RegEx pattern will be searched. '
                                       'Multiple files should be comma-delimited with NO SPACES')
group = parser.add_mutually_exclusive_group()
group.add_argument('-c', '--color', action='store_true', help='Matching text will be colored accordingly')
group.add_argument('-u', '--underline', action='store_true', help='Matching text will be marked with ^ underneath')
group.add_argument('-m', '--machine', action='store_true', help='Print machine readable format '
                                                                '(file_name:no_line:start_pos:matched_text)')
args = parser.parse_args()

# Handle user input where no arguments passed:
if not getattr(args, 'pattern'):
    setattr(args, 'pattern', raw_input('Please enter the RegEx pattern to search for: '))

if not getattr(args, 'file'):
    setattr(args, 'file', raw_input('Please enter the input file(s) to search through (comma-delimited list): '))

# Handle multiple files input:
files = args.file.split(',')


class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def pattern_finder():
    """

    :return:
    """
    # Iterate over all files provided, search for regex pattern in each file in turn
    for f in files:
        with open(f) as cf:
            line_number = 1
            name = cf.name
            for line in cf.readlines():
                if re.search(args.pattern, line):
                    if args.underline:
                        print '{0} {1}'.format(name, print_match_underline(line, args.pattern, line_number))
                    elif args.color:
                        print '{0}:{1} {2}'.format(name, line_number, print_match_color(line_number, line, args.pattern))
                    else:
                        matches = re.finditer(args.pattern, line)
                        for match in matches:
                            print '{0}:{1}:{2}'.format(name, line_number, print_match_machine(match))
                line_number += 1


def print_match_machine(match):
    """
    This function will receive a match object and will return the according format.

    :param match:
    :return: start position of the match:text of the match
    """
    startpos = int(match.start())
    matchtext = match.group()
    return '{0}:{1}'.format(startpos, matchtext)


def print_match_underline(line, pattern, line_number):
    """
    This function will receive
    :param line:
    :param pattern:
    :param line_number:
    :return:
    """

    line = line.rstrip()
    if re.search(pattern, line):
        matches = re.finditer(pattern, line)
        for match in matches:
            startpos = int(match.start()) + 1
            endpos = int(match.end()) + 1
            length = len(line)
            newline = "  "
            for i in range(length):
                if i in range(startpos, endpos):
                    newline += "^"
                else:
                    newline += " "
            print '{0} {1}'.format(str(line_number), ' ' + line)
            print newline


def print_match_color(line_number, line, pattern):
    """

    :param line_number:
    :param line:
    :param pattern:
    :return:
    """
    line_split = line.rstrip().split(' ')
    for word in line_split:
        if re.match(pattern, word):
            line_split[line_split.index(word)] = '{0}{1}{2}'.format(Color.RED, word, Color.END)
            print '{0} {1}'.format(str(line_number), ' '.join(line_split))



def main():
    pattern_finder()

if __name__ == '__main__':
    main()
