#!/usr/bin/env python
# CodeExam_RH by

__author__ = 'Enav Hidekel'
__date__ = 'May 02, 2018'

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


def pattern_finder(f):
    """
    This function would receive a file and search for a RegEx pattern given in advance.


    :return: It will print it according to the format selected by the user (--color, --machine-code, --underline).
    """
    # Iterate over each file provided, search for regex pattern in each file in turn
    with open(f) as current:
        line_number = 1
        name = current.name
        for line in current.readlines():
            if re.search(args.pattern, line):
                if args.underline:
                    print_match_underline(name, line, args.pattern, line_number)
                elif args.color:
                    print '{0}:{1} {2}'.format(name, line_number, print_match_color(line, args.pattern))
                else:
                    matches = re.finditer(args.pattern, line)
                    for match in matches:
                        print_match_machine(match, name, line_number)
            line_number += 1


def print_match_machine(match, name, line_number):
    """
    This function receives a match object, named file and a line number within that file.
    it's purpose is to manipulate output into this format:

    :param match: object of type match
    :param name: file name corresponding to the match
    :param line_number: line number corresponding to the match
    :return: returns the matching text in this format: file_name:no_line:start_pos:matched_text
    """
    startpos = int(match.start())
    matchtext = match.group()
    print '{0}:{1}:{2}:{3}'.format(name, line_number, startpos, matchtext)


def print_match_underline(name, line, pattern, line_number):
    """
    This function receives a named file and, line number within that file,
    RegEx expression to match within that line and the line number.

    :param name:file name corresponding to the match.
    :param line: line text corresponding to the match.
    :param pattern: RegEx expression to match.
    :param line_number: line number corresponding to the match.
    :return: returns the same line with matches underlined with the '^' sign.
    """

    line = line.rstrip()
    lengthoffilename = len(name)
    if re.search(pattern, line):
        matches = re.finditer(pattern, line)
        for match in matches:
            startpos = int(match.start()) + lengthoffilename + 1
            endpos = int(match.end()) + lengthoffilename + 1
            length = len(line) + lengthoffilename
            newline = "  "
            for i in range(length):
                if i in range(startpos, endpos):
                    newline += "^"
                else:
                    newline += " "
            print '{0} {1} {2}'.format(name, str(line_number), ' ' + line)
            print '{0}'.format(' ' + newline)



def print_match_color(line, pattern):
    """
    This function receives a named file and, line number within that file,
    RegEx expression to match within that line and the line number.

    :param line: line text corresponding to the match.
    :param pattern: RegEx expression to match.
    :return: returns the same line with matches colored Red.
    """
    line_split = line.rstrip().split(' ')
    for word in line_split:
        if re.match(pattern, word):
            line_split[line_split.index(word)] = '{0}{1}{2}'.format(Color.RED, word, Color.END)
        else :
            line_split[line_split.index(word)] = '{0}'.format(word)
    return ' '.join(line_split)


def main():

    for f in files:
        pattern_finder(f)

if __name__ == '__main__':
    main()
