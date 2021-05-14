# Replace the title with the file basename in a .html file delimited by <open_tag>*<close_tag>

import argparse
import glob
from datetime import datetime
from itertools import islice


# -------------------
# data definitions
# -------------------
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

    # lines to skip
    parser.add_argument('--skip', '-s', default=10, type=int,
                        help='Number of lines to skip')

    args = parser.parse_args()
    return args


# -------------------
# get_sloc_lines
# -------------------
def get_sloc_lines(path, program, skip):
    # pre-pend each line with today's date and program name
    timestamp = datetime.now()

    # current day in yyyymmdd format
    yyyymmddDate = timestamp.strftime("%Y%m%d")

    log(f'{path} -> ', end='')
    # open file to read
    with open(path, 'r') as fpR:
        count = 0
        for line in islice(fpR, skip, None):
            # if this is a blank line we're done
            if line.strip() == "":
                break

            count += 1

            # prepend line with today's date and program name
            new_text = f"{yyyymmddDate},{program},{line}"

            # open file to append - TBD filename
            with open("new.csv", 'a') as fpA:
                # append line to
                fpA.write(new_text)

    log(f'{count} lines parsed')


# -------------------
# main
# -------------------
def main():
    # main function
    global QUIET

    # get & parse arguments
    args = get_args()  # read arguments
    QUIET = args.quiet

    # for files in the path - replace the title in the HTML file
    for path in glob.iglob(args.path):
        get_sloc_lines(path, args.program, args.skip)


if __name__ == '__main__':
    main()
