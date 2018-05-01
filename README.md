# Excercise instructions:

Implement a script in Python that 
1. searches one or more named input files (standard input if no files are specified, or the file name '-' is given) 
for lines containing a match to a regular expression pattern (given on command line as well).
2. Assume that input is ascii, you don't need to deal with different encoding.

3. If a line matches, print it. 
Please print the file name and the linenumber for every match.

4. Script accept list optional parameters which are mutually exclusive:
-u ( --underscore ) which prints '^' under the matching text
-c ( --color ) which highlight matching text [1]
-m ( --machine ) which generate machine readable output
                  format: file_name:no_line:start_pos:matched_text

5. Multiple matches on single line are allowed, without overlapping.

6. The script should be compatible in line with PEP8 coding guidelines. 

7. Please add proper documentation and error handling.

Hint: It is recommended to use a module for parsing the command line
arguments and the "re" module for matching the pattern.

Try to use OOP in order to encapsulate differences  between output
formats. Please put into comments what design pattern it follows.
