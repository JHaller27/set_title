import argparse
import glob
import os
import re


# Regex to search for <title> HTML tags
# Pre-compile to avoid wasting cycles compiling on each loop iteration (for each file)
TITLE_REGEX = re.compile(r'(?P<open_tag><[^>\w]*title[^>]*>)(?P<old_title>[^<]*)(?P<close_tag><[^>]*/[^>]*title[^>]*>)')
"""
Break-down of each regex group from left-to-right:
    (?P<open_tag><[^>\w]*title[^>]*>)
        Name the capture-group "open_tag"
        Look for <title>
    (?P<old_title>[^<]*)
        Name the capture-group "old_title"
        Look for any # of chars that are not a right-angle-bracket
    (?P<close_tag><[^>]*/[^>]*title[^>]*>)
        Name the capture-group "close_tag"
        Lood for </title>
"""

# Flag to supress progress output
# Global so that it doesn't need to be passed around to every fn that wants to call log()
QUIET = False


def log(*args, **kwargs):
    """
    Simple pass-through to print(), but IFF global QUIET flag is False
    """

    if not QUIET:
        print(*args, **kwargs)


def get_args():
    """
    Set-up argparse and get cli arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str,
                        help='Path to file to replace (glob-patterns supported)')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Silence output')
    args = parser.parse_args()

    return args


def replace_title(path):
    # Print path name, get the file name (ie the new <title> value), then print the file name
    log(f'{path} -> ', end='')
    name = os.path.splitext(os.path.basename(path))[0]
    log(f'"{name}"')

    # Read the file and store as text for regex replacement
    with open(path, 'r') as fp:
        old_text = fp.read()

    # Substitute <title>filename</title> in the file's text
    new_text = TITLE_REGEX.sub(f'\\1{name}\\3', old_text)

    # Write substituted-text back to original file
    with open(path, 'w') as fp:
        fp.write(new_text)


def main():
    global QUIET

    args = get_args()

    QUIET = args.quiet

    # Loop over each path in the glob search pattern...
    for path in glob.iglob(args.path):
        replace_title(path)


if __name__ == '__main__':
    main()
