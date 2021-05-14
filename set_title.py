# Prepend a date and program name to each line of a csv, and output to a new file

import glob
from datetime import datetime
from itertools import islice
import typer


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
def main(
    input_path: str = typer.Argument(..., help="Path to file to replace (glob-patterns supported)"),
    output_path: str = typer.Argument(..., help="Path to new file to write to"),
    program: str = typer.Argument(..., help="Program name (eg 737MAX_SCE)"),
    skip: int = typer.Option(10, "--skip", "-s", help="Number of lines to skip"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Silence output"),
):
    # main function
    global QUIET

    # get & parse arguments
    QUIET = quiet

    # with a progress bar...
    # for files in the path - rewrite SLOC lines to new csv file
    with typer.progressbar(glob.iglob(input_path)) as all_paths:
        for in_path in all_paths:
            get_sloc_lines(in_path, output_path, program, skip)


if __name__ == '__main__':
    typer.run(main)
