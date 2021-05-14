# Prepend a date and program name to each line of a csv, and output to a new file

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
    parser.add_argument('input_path', type=str,
                        help='Path to file to replace (glob-patterns supported)')

    # output file (eg "path\newfile.ext")
    parser.add_argument('output_path', type=str,
                        help='Path to new file to write to')

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
def get_sloc_lines(in_path, out_path, program, skip):
    # pre-pend each line with today's date and program name
    timestamp = datetime.now()

    # current day in yyyymmdd format
    yyyymmddDate = timestamp.strftime("%Y%m%d")

    log(f'{in_path} -> ', end='')
    # open file to read and file to append - TBD filename
    with open(in_path, 'r') as fpR, open(out_path, "a") as fpA:
        count = 0
        for line in islice(fpR, skip, None):
            # if this is a blank line we're done
            if line.strip() == "":
                break

            count += 1

            # prepend line with today's date and program name
            new_text = f"{yyyymmddDate},{program},{line}"

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

    # for files in the path - rewrite SLOC lines to new csv file
    for in_path in glob.iglob(args.input_path):
        get_sloc_lines(in_path, args.output_path, args.program, args.skip)


if __name__ == '__main__':
    main()
