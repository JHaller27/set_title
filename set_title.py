# Replace the title with the file basename in a .html file delimited by <open_tag>*<close_tag>

import argparse
import glob
import os
import re
from datetime import datetime

# -------------------
# data definitions
# -------------------
# regular expression to identify title line
TITLE_REGEX = re.compile(
    r'(?P<open_tag><[^>\w]*title[^>]*>)(?P<old_title>[^<]*)(?P<close_tag><[^>]*/[^>]*title[^>]*>)')
QUIET = False


# -------------------
# log
# -------------------
def log(*args, **kwargs):
    # show arguments
    if not QUIET:
        print(*args, **kwargs)


# -------------------
# get_args
# -------------------
def get_args():
    # read arguments
    parser = argparse.ArgumentParser()

    # input file (eg "path\file.ext")
    parser.add_argument('path', type=str,
                        help='Path to file to replace (glob-patterns supported)')

    # program name (eg "737MAX_SCE")
    parser.add_argument('program', type=str,
                        help='Program name (eg 737MAX_SCE)')

    # quiet mode - optional
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Silence output')

    args = parser.parse_args()
    return args


# -------------------
# get_sloc_lines
# -------------------
def get_sloc_lines(path_glob, program):
    # pre-pend each line with today's date and program name
    timestamp = datetime.now()

    # current day in yyyymmdd format
    yyyymmddDate = timestamp.strftime("%Y%m%d")

    for path in glob.iglob(path_glob):
        log(f'{path} -> ', end='')

        # open file to read
        fpR = open(path, 'r')

        # open file to append - TBD filename
        fpA = open("new.csv", 'a')

        count = 0
        while True:
            count += 1
            line = fpR.readline()

            # if line is empty - end of file; get out of loop
            if not line:
                break

            # SLOC lines start at line 10
            if count < 10:
                continue

            # if this is a blank line we're done
            if line.find(",") < 0:
                break

            # prepend line with today's date and program name
            new_text = yyyymmddDate + "," + program + "," + line

            # append line to
            fpA.write(new_text)

    log(f'{count} lines read')

# -------------------
# main
# -------------------


def main():
    # main function
    global QUIET

    # get & parse arguments
    args = get_args()  # read arguments - not currently used
    QUIET = args.quiet

    # for files in the path - replace the title in the HTML file
    for path in glob.iglob(args.path):
        get_sloc_lines(path, args.program)


if __name__ == '__main__':
    main()
